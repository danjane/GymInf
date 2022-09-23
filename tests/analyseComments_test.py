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
    d = {'Student': ["Albert"], 'Date': [datetime.date(2023, 9, 8)]}
    df = pd.DataFrame(d)
    assert "Weight" in weight_comments(df)


def test_positiveWeightInComments():
    d = {'Student': ["Albert"], 'Date': [datetime.date(2023, 9, 8)]}
    df = pd.DataFrame(d)
    assert weight_comments(df)["Weight"][0] > 0
