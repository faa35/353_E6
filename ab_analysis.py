import sys

import pandas as pd
from scipy import stats


# {"uid":6061521,"is_instructor":true,"login_count":1,"search_count":2}
# Users with an odd-numbered uid were shown a new-and-improved search box. Others were shown the original design.
# odd uid = new
# even uid = old



OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)




# source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
def contingency_p(data):

    
    # print(data['uid'])  # total: 681

    odd = (data['uid'] % 2) == 1  # if odd(new) then true
    #print(odd)
    #print(odd.sum())  #odd uid =348

    
    searched = data['search_count'] > 0
    #print(searched)
    #print(searched.sum())  # 209 user searched at least once
                            # 681-209= 472 user never searched

    table = pd.crosstab(odd, searched)
    # print(table)

#    search_count  False  True 
#uid                       
#False           222    111
#True            250     98

# so,
# Old search box:
# 222 did not search
# 111 searched
# new search box:
# 250 did not search
# 98 searched


    return stats.chi2_contingency(table).pvalue


# source: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
def mannwhitneyu_p(data):

    is_odd = (data['uid'] % 2) == 1 # classifying which are odds(new)
    odd_users = data[is_odd]        #table only for odds
    odd = odd_users['search_count'] #only the search_count column for odds

    is_even = (data['uid'] % 2) == 0
    even_users = data[is_even]
    even = even_users['search_count']

    return stats.mannwhitneyu(odd, even).pvalue


def main():
    searchdata_file = sys.argv[1]

    searchdata = pd.read_json(searchdata_file, orient='records', lines=True)
    instructors = searchdata[searchdata['is_instructor']]


    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p=contingency_p(searchdata),
        more_searches_p=mannwhitneyu_p(searchdata),
        more_instr_p=contingency_p(instructors),
        more_instr_searches_p=mannwhitneyu_p(instructors),
    ))


if __name__ == '__main__':
    main()
