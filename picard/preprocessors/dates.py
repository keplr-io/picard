import pandas as pd
def process_date(df):

    print('parsing dates...')
    def to_hour(x):
        return x.hour

    return pd.to_datetime(df).apply(to_hour).as_matrix()