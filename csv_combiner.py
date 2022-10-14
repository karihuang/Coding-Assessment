import sys
import os
import re
import pandas as pd

def combine(argv):
    # total arguments get from the command line
    n = len(argv)
    if n == 1:
        raise Exception("No input provided")

    # create an empty dataframe to store input from each csv file
    df = []
    for i in range(1, n):
        try:
            temp = pd.read_csv(argv[i])
        except:
            raise Exception("Invalid file(s)")

        # use regex to get the file name end with .csv
        file = re.search(r'[^\/]*\.csv', argv[i])
        temp["filename"] = file.group()
        df.append(temp)

    # combine inputs together and autogenerate new index
    df = pd.concat(df, axis=0, ignore_index=True)
    return df

def output():
    print(combine(sys.argv).to_string())

if __name__ == "__main__":
    output()

