from config import TRAIN_CSV_PATH

import pandas as pd


def load_data(path, parse_dates=True, index_col=None):
    """
    Load the data from the specified CSV file and parse the 'date' column.

    Returns:
        pandas.DataFrame: The training data.
    """
    parse_dates_cols = ['date']
    if not parse_dates:
        parse_dates_cols = []

    df = pd.read_csv(path, parse_dates=parse_dates_cols, index_col=index_col)
    return df


if __name__ == "__main__":
    train_df = load_data(TRAIN_CSV_PATH)

    print(train_df.head())


