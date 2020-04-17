import pandas as pd

def get_dfa_str():
    df = pd.read_csv('source/FA_INPUT.csv', index_col=0)
    pd.set_option('max_rows', None)
    pd.set_option('max_columns', None)
    pd.set_option('display.width', None)
    s = str(df)
    return s

def main():
    df = pd.read_csv('source/FA_INPUT.csv', index_col=0)
    pd.set_option('max_rows', None)
    pd.set_option('max_columns', None)
    pd.set_option('display.width', None)
    s = str(df)
    print(s)

if __name__ == '__main__':
    main()