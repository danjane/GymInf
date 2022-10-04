import numpy as np


def sum_by_student(df, column):
    df2 = df.pivot(columns="Student")[column]
    sums = {}
    for student in df2.columns:
        sums[student] = np.nansum(df2[student])
    return sums


def weight_comments(df):
    date_diffs = (df['Date'] - max(df['Date'])).apply(lambda x: x.days)
    df['Weight'] = date_diffs.apply(lambda x: np.exp(x / 10.))
    return df


def dnf_count(df):
    return sum_by_student(df, "DNF")


def dnf_count_positives(df):
    df = dnf_count(df)
    return df


def sum_weights(df, students):
    sums = dict.fromkeys(students, 0)
    non_zero_sums = sum_by_student(df, "Weight")
    for student, v in non_zero_sums.items():
        sums[student] = v
    return sums


def students_by_least_weight(weights):
    return [k for k, v in sorted(weights.items(), key=lambda item: item[1])]
