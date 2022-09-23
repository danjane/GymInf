import numpy as np


def dnf_count(df):
    df2 = df.pivot(columns="Student")["DNF"]
    dnfs = {}
    for student in df2.columns:
        dnfs[student] = np.nansum(df2[student])
    return dnfs


def weight_comments(df):
    df["Weight"] = 1
    return df
