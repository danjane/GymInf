from analyseComments import *
import pandas as pd


def test_rv():
    d = {'Student': ["Albert"]*2, 'DNF': [1, 1]}
    df = pd.DataFrame(data=d)
    assert dnf_count(df)["Albert"] == 2
