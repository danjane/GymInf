import numpy as np


def dnf_count(df):
    df2 = df.pivot(columns="Student")["DNF"]
    dnfs = {}
    for student in df2.columns:
        dnfs[student] = np.nansum(df2[student])
    return dnfs


def weight_comments(df):
    date_diffs = (df['Date'] - max(df['Date'])).apply(lambda x: x.days)
    df['Weight'] = date_diffs.apply(lambda x: np.exp(x / 10.))
    return df


def sum_weights(df):
    pass