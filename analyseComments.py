import numpy as np
import pandas as pd
from typing import Dict, List


def sum_by_student(df: pd.DataFrame, column: str) -> Dict[str, float]:
    df2 = df.pivot(columns="Student")[column]
    sums: Dict[str, float] = {}
    for student in df2.columns:
        sums[student] = np.nansum(df2[student])
    return sums


def weight_comments(df: pd.DataFrame) -> pd.DataFrame:
    date_diffs = (df['Date'] - max(df['Date'])).apply(lambda x: x.days)
    df['Weight'] = date_diffs.apply(lambda x: np.exp(x / 10.))
    return df


def count_dnf_by_student(df: pd.DataFrame) -> Dict[str, float]:
    return sum_by_student(df, "DNF")


def count_dnf_greater_than(df: pd.DataFrame, cut_off: float = 0) -> Dict[str, float]:
    df = count_dnf_by_student(df)
    df_positive: Dict[str, float] = {}
    for k, v in df.items():
        if v > cut_off:
            df_positive[k] = v
    return df_positive


def sum_weights_by_student(df: pd.DataFrame, students: List[str]) -> Dict[str, float]:
    weights = dict.fromkeys(students, 0)
    non_zero_weights = sum_by_student(df, "Weight")
    v: int
    for student, v in non_zero_weights.items():
        if student in students:
            weights[student] = v
    return weights


def students_by_least_weight(weights: Dict[str, float]) -> List[str]:
    return [k for k, v in sorted(weights.items(), key=lambda item: item[1])]


def comments_needed(df: pd.DataFrame, students: List[str]) -> List[str]:
    if "Weight" not in df:
        df = weight_comments(df)
    weights = sum_weights_by_student(df, students)
    return students_by_least_weight(weights)


def latex_comments(df: pd.DataFrame, student: str) -> str:
    df = df[df['Student'].isin([student])]
    if len(df) == 0:
        return "No comments yet\n"
    df = df[["Date", "Info"]]
    df['Date'] = df['Date'].dt.strftime('%d%b%Y').astype(str)
    return df.style.hide(axis="index").to_latex()


def latex_student_page(outline: str, student: str, name: str, course: str, comments: str) -> str:
    text = outline
    keywords = ["STUDENTCODE", "STUDENTNAME", "COURSE", "STUDENTCOMMENTS"]
    for (before, after) in zip(keywords, [student, name, course, comments]):
        text = text.replace(before, after)
    return text


def latex_student_pages(df: pd.DataFrame, outline: str, students: List[str], 
                        given_names: List[str], courses: List[str]) -> str:
    pages = []
    for student, name, course in zip(students, given_names, courses):
        comments = latex_comments(df, student)
        this_student_latex_page = latex_student_page(outline, student, name, course, comments)
        pages.append(this_student_latex_page)
    return "\\newpage\n\n".join(pages)
