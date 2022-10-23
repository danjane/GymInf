from createSeatingPlan import *


def test_seatingListTwoStudentsToLatexDesks():
    students = ["albert", "gabs"]
    output = r"""\node[desk] at (0, 0) {albert};
\node[desk] at (2, 0) {gabs};"""
    assert seatingListToLatexDesks(students) == output


def test_seatingListEightStudentsToLatexDesks():
    students = list("abcdefgh")
    output = r"""\node[desk] at (0, 0) {a};
\node[desk] at (2, 0) {b};
\node[desk] at (5, 0) {c};
\node[desk] at (7, 0) {d};
\node[desk] at (10, 0) {e};
\node[desk] at (12, 0) {f};
\node[desk] at (0, 4) {g};
\node[desk] at (2, 4) {h};"""
    assert seatingListToLatexDesks(students) == output
