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


def dnf_count_greater_than(df, cut_off=0):
    df = dnf_count(df)
    df_positive = {}
    for k, v in df.items():
        if v > cut_off:
            df_positive[k] = v
    return df_positive


def sum_weights(df, students):
    weights = dict.fromkeys(students, 0)
    non_zero_weights = sum_by_student(df, "Weight")
    for student, v in non_zero_weights.items():
        if student in students:
            weights[student] = v
    return weights


def students_by_least_weight(weights):
    return [k for k, v in sorted(weights.items(), key=lambda item: item[1])]


def comments_needed(df, students):
    if "Weight" not in df:
        df = weight_comments(df)
    weights = sum_weights(df, students)
    return students_by_least_weight(weights)


def latex_comments(df, student):
    df = df[df['Student'].isin([student])]
    if len(df) == 0:
        return "No comments yet\n"
    df = df[["Date", "Info"]]
    df.isetitem(0, df['Date'].dt.strftime('%d%b%Y').astype(str))
    return df.style.hide(axis="index").to_latex()


def latex_student_page(outline, student, name, course, comments):
    text = outline
    keywords = ["STUDENTCODE", "STUDENTNAME", "COURSE", "STUDENTCOMMENTS"]
    for (before, after) in zip(keywords, [student, name, course, comments]):
        text = text.replace(before, after)
    return text


def latex_student_pages(df, outline, students, given_names, courses):
    pages = []
    for student, name, course in zip(students, given_names, courses):
        comments = latex_comments(df, student)
        this_student_latex_page = latex_student_page(outline, student, name, course, comments)
        pages.append(this_student_latex_page)
    return "\\newpage\n\n".join(pages)
