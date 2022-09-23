from analyseComments import *
import pandas as pd
import datetime

def test_rv():
    d = {'Student': ["Albert"]*2, 'DNF': [1, 0]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 1


def test_rv2():
    d = {'Student': ["Albert"]*2, 'DNF': [1, 1]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 2


def test_rvTwoStudents():
    d = {'Student': ["Albert", "Gabs"]*2, 'DNF': [1, 1, 1, 0]}
    df = pd.DataFrame(d)
    assert dnf_count(df)["Albert"] == 2
    assert dnf_count(df)["Gabs"] == 1


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
    assert sum_weights(df)["Albert"] == 2
