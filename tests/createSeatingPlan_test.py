from createSeatingPlan import *


def test_seatingListToLatexDesks():
    students = ["albert", "gabs"]
    output = r"""\node[desk] at (0, 0) {albert};
\node[desk] at (2.5, 0) {gabs};"""
    assert seatingListToLatexDesks(students) == output
