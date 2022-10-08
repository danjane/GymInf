from analyseComments import *
import pandas as pd
import datetime


def test_rv():
    d = {'Student': ["Albert"] * 2, 'DNF': [1, 0]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 1


def test_rv2():
    d = {'Student': ["Albert"] * 2, 'DNF': [1, 1]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 2


def test_rvTwoStudents():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [1, 1, 1, 0]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 2
    assert dnf_count(df)["Gabs"] == 1


def test_rvPositiveCount():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [0, 0, 1, 0]}
    df = pd.DataFrame(d)
    p = dnf_count_greater_than(df)
    assert p["Albert"] == 1
    assert "Gabs" not in p


def test_rvCountCutOff():
    d = {'Student': ["Albert", "Gabs"] * 2, 'DNF': [1, 1, 1, 0]}
    df = pd.DataFrame(d)
    p = dnf_count_greater_than(df, 1)
    assert p["Albert"] == 2
    assert "Gabs" not in p


def test_weightInComments():
    d = {'Date': [datetime.date(2023, 9, 8)]}
    df = pd.DataFrame(d)
    assert "Weight" in weight_comments(df)


def test_positiveWeightInComments():
    d = {'Date': [datetime.date(2023, 9, 8)]}
    df = pd.DataFrame(d)
    assert weight_comments(df)["Weight"][0] > 0


def test_recentCommentsMoreWeight():
    d = {'Date': [datetime.date(1990, 9, 8), datetime.date(2023, 9, 8)]}
    df = pd.DataFrame(d)
    df = weight_comments(df)
    assert df["Weight"][1] > df["Weight"][0]


def test_sumWeights():
    d = {'Student': ["Albert"] * 2, 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert sum_weights(df, ["Albert"])["Albert"] == 2


def test_studentWithNoComments():
    d = {'Student': ["Albert"] * 2, 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert sum_weights(df, ["Albert", "Gabs"])["Gabs"] == 0


def test_subsetStudentsForWeights():
    d = {'Student': ["Albert", "Gabs"], 'Weight': [1, 1]}
    df = pd.DataFrame(d)
    assert "Gabs" not in sum_weights(df, ["Albert"])


def test_linksForWeights():
    d = {'Student': ["Albert", "Gabs"] * 2,
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist()}
    df = pd.DataFrame(d)
    df = weight_comments(df)
    weights = sum_weights(df, ["Albert", "Gabs"])
    assert weights["Albert"] < weights["Gabs"]


def test_studentsToComment():
    weights = {"Albert": 2, "Gabs": 1}
    assert students_by_least_weight(weights) == ["Gabs", "Albert"]


def test_studentsToCommentThree():
    weights = {"Albert": 2, "Gabs": 1, "Marie": 0}
    assert students_by_least_weight(weights) == ["Marie", "Gabs", "Albert"]


def test_commentsNeeded():
    students = ["Albert", "Gabs", "Marie", "Dick"]
    d = {'Student': students,
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist()}
    df = pd.DataFrame(d)
    assert comments_needed(df, students) == students


def test_commentsDoubledNeeded():
    d = {'Student': ["Albert"]*3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist()}
    df = pd.DataFrame(d)
    assert comments_needed(df, ["Albert", "Gabs"]) == ["Gabs", "Albert"]


def test_oneStudentLatexComments():
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


def test_missingStudentLatexComments():
    d = {'Student': ["Albert"] * 3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Info': ["Happy", "Sad"] * 2}
    df = pd.DataFrame(d)
    assert latex_comments(df, "Marie") == r"""No comments yet
"""


def test_buildLatexReport():

    d = {'Student': ["Albert"] * 3 + ["Gabs"],
         'Date': pd.date_range(datetime.date(2023, 9, 8), periods=4).tolist(),
         'Info': ["Happy", "Sad"] * 2}
    df = pd.DataFrame(d)
    students = ["Marie", "Albert", "Gabs"]
    assert latex_report(df, students, students, "1ma1df01") == r"""Marie \hfill 1ma1df01
No comments yet
\newpage

Albert \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
08Sep2023 & Happy \\
09Sep2023 & Sad \\
10Sep2023 & Happy \\
\end{tabular}
\newpage

Gabs \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
11Sep2023 & Sad \\
\end{tabular}
"""
