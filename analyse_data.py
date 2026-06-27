import sys

import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def main():
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    else:
        data_file = 'data.csv'

    data = pd.read_csv(data_file)
    #print(data.head())

    
    print('summary (seconds):  ')
    print(data.groupby('algorithm')['time'].describe())

    print('-----------------------------')
    print()
    print()

    # ANOVA for any of the implementation mean running times different?
    g = data.groupby('algorithm')['time']

    anova = stats.f_oneway(
        g.get_group('qs1'), g.get_group('qs2'), g.get_group('qs3'),
        g.get_group('qs4'), g.get_group('qs5'), g.get_group('merge1'),
        g.get_group('partition_sort'),
    )
    print('ANOVA p value:', anova.pvalue)
    print('-----------------------------')
    print()
    print()

    # Post-hoc Tukey HSD
    posthoc = pairwise_tukeyhsd(data['time'], data['algorithm'], alpha=0.05)
    print(posthoc)
    
    print()
    print()

    #mean running time,fastest is at first
    print('Mean time by algorithm (ascending):')
    print(data.groupby('algorithm')['time'].mean().sort_values())


if __name__ == '__main__':
    main()
