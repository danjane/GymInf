import numpy as np


def sum_by_student(df, column):
    df2 = df.pivot(columns="Student")[column]
    dnfs = {}
    for student in df2.columns:
        dnfs[student] = np.nansum(df2[student])
    return dnfs


def weight_comments(df):
    date_diffs = (df['Date'] - max(df['Date'])).apply(lambda x: x.days)
    df['Weight'] = date_diffs.apply(lambda x: np.exp(x / 10.))
    return df


def dnf_count(df):
    return sum_by_student(df, "DNF")


def sum_weights(df):
    return sum_by_student(df, "Weight")
