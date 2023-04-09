from analyseComments import *
import pandas as pd
import datetime


def test_count_dnf_with_name_repetition():
    d = {'Student': ["Albert"] * 2, 'DNF': [1, 0]}
    df = pd.DataFrame(d)
    assert count_dnf_by_student(df)["Albert"] == 1


def test_count_dnf_with_full_name_repetition():
    d = {'Student': ["Albert"] * 2, 'DNF': [1, 1]}
    df = pd.DataFrame(d)
    assert count_dnf_by_student(df)["Albert"] == 2


def test_count_dnf_with_two_students():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [1, 1, 1, 0]}
    df = pd.DataFrame(d)
    assert count_dnf_by_student(df)["Albert"] == 2
    assert count_dnf_by_student(df)["Gabs"] == 1


def test_count_positive_dnf_with_name_repetition():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [0, 0, 1, 0]}
    df = pd.DataFrame(d)
    p = count_dnf_greater_than(df)
    assert p["Albert"] == 1
    assert "Gabs" not in p


def test_count_dnf_with_cutoff():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [1, 1, 1, 0]}
    df = pd.DataFrame(d)
    p = count_dnf_greater_than(df, 1)
    assert p["Albert"] == 2
    assert "Gabs" not in p


def test_find_weight_comment():
    d = {'Date': [datetime.date(2023, 9, 8)], 'Sentiment': 1}
    df = pd.DataFrame(d)
    assert "Weight" in weight_comments(df)


def test_positive_weight_in_comments():
    d = {'Date': [datetime.date(2023, 9, 8)], 'Sentiment': 1}
    df = pd.DataFrame(d)
    assert weight_comments(df)["Weight"][0] > 0


def test_recent_comments_more_weight():
    d = {'Date': [datetime.date(1990, 9, 8), datetime.date(2023, 9, 8)], 'Sentiment': 1}
    df = pd.DataFrame(d)
    df = weight_comments(df)
    assert df["Weight"][1] > df["Weight"][0]


def test_sum_weights():
    d = {'Student': ["Albert"] * 2, 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert sum_weights_by_student(df, ["Albert"])["Albert"] == 2


def test_student_with_no_comments():
    d = {'Student': ["Albert"] * 2, 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert sum_weights_by_student(df, ["Albert", "Gabs"])["Gabs"] == 0


def test_subset_students_for_weights():
    d = {'Student': ["Albert", "Gabs"], 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert "Gabs" not in sum_weights_by_student(df, ["Albert"])


def test_student_order_by_weight():
    d = {'Student': ["Albert", "Gabs"] * 2,
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Sentiment': 1}
    df = pd.DataFrame(d)
    df = weight_comments(df)
    weights = sum_weights_by_student(df, ["Albert", "Gabs"])
    assert weights["Albert"] < weights["Gabs"]


def test_students_that_need_comments():
    weights = {"Albert": 2, "Gabs": 1}
    assert students_by_least_weight(weights) == ["Gabs", "Albert"]


def test_three_students_that_need_comments():
    weights = {"Albert": 2, "Gabs": 1, "Marie": 0}
    assert students_by_least_weight(weights) == ["Marie", "Gabs", "Albert"]


def test_comments_needed():
    students = ["Albert", "Gabs", "Marie", "Dick"]
    d = {'Student': students,
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Sentiment': 1}
    df = pd.DataFrame(d)
    assert comments_needed(df, students) == students


def test_double_comments_needed():
    d = {'Student': ["Albert"]*3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Sentiment': 1}
    df = pd.DataFrame(d)
    assert comments_needed(df, ["Albert", "Gabs"]) == ["Gabs", "Albert"]


def test_create_latex_comments():
    d = {'Student': ["Albert"] * 3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Info': ["Happy", "Sad"] * 2}
    df = pd.DataFrame(d)
    outputAlbert = r"""\begin{tabular}{ll}
Date & Info \\
08Sep2023 & Happy \\
09Sep2023 & Sad \\
10Sep2023 & Happy \\
\end{tabular}
"""
    outputGabs = r"""\begin{tabular}{ll}
Date & Info \\
11Sep2023 & Sad \\
\end{tabular}
"""
    assert latex_comments(df, "Albert") == outputAlbert
    assert latex_comments(df, "Gabs") == outputGabs


def test_create_latex_comments_containing_student_with_no_comments():
    d = {'Student': ["Albert"] * 3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Info': ["Happy", "Sad"] * 2}
    df = pd.DataFrame(d)
    assert latex_comments(df, "Marie") == r"""No comments yet
"""


def test_build_latex_report():
    d = {'Student': ["Albert"] * 3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Info': ["Happy", "Sad"] * 2}
    df = pd.DataFrame(d)
    students = ["Marie", "Albert", "Gabs"]

    student_report_outline = r"""STUDENTNAME (STUDENTCODE) \hfill COURSE \\
STUDENTCOMMENTS"""

    assert latex_student_pages(df, student_report_outline, students, students, ["1ma1df01"] * 4) == r"""Marie (Marie) \hfill 1ma1df01 \\
No comments yet
\newpage

Albert (Albert) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
08Sep2023 & Happy \\
09Sep2023 & Sad \\
10Sep2023 & Happy \\
\end{tabular}
\newpage

Gabs (Gabs) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
11Sep2023 & Sad \\
\end{tabular}
"""
