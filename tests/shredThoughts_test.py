from shredComments import *


def test_chkOneStudent():
    assert is_student("Albert good question", "Albert")


def test_findOneStudent():
    assert find_students("Albert good question", ["Albert"]) == ["Albert"]


def test_findStudents():
    assert find_students("Albert, Gabs good question", ["Albert", "Gabs"]) == ["Albert", "Gabs"]

