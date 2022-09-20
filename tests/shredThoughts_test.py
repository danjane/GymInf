from shredComments import *


def test_chkOneStudentTrue():
    assert is_student("Albert good question", "Albert")


def test_chkOneStudentFalse():
    assert not is_student("Albert good question", "Gabs")


def test_findOneStudent():
    assert find_students("Albert good question", ["Albert"]) == ["Albert"]


def test_findStudents():
    assert find_students("Albert, Gabs good question", ["Albert", "Gabs"]) == ["Albert", "Gabs"]

