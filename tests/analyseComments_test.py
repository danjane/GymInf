from analyseComments import *
import shredComments


def test_links():
    strings = """
        d25Dec2022
        c1ma1df01
        +Albert, Gabs great question
    """.split("\n")
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    infos = shredComments.shredder(strings, courses)
    table = shredComments.panderize(infos)
    assert table.size == 12
