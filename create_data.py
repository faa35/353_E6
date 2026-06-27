import time
from implementations import all_implementations

#all_implementations = [qs1, qs2, qs3, qs4, qs5, merge1, partition_sort]


import numpy as np
import pandas as pd


ARRAY_SIZE = 5000 #for random arrays
RUN_COUNT = 100      # Restriction #2: run count

def main():
    random_number_generator = np.random.default_rng()

    rows = []

    for _ in range(RUN_COUNT):
        random_array = random_number_generator.integers(0, 2**31, size=ARRAY_SIZE)

        for sort in all_implementations:           #taken from assignmetn description
            st = time.time()
            sort(random_array)
            en = time.time()
            rows.append({'algorithm': sort.__name__, 'time': en - st})



    data = pd.DataFrame(rows)

    #create a DataFrame in a format that makes sense, and save it as data.csv, something like this:
    data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
