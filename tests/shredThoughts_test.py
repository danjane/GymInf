import datetime
from shredComments import *


def test_chkOneStudentTrue():
    assert is_student("Albert good question", "Albert")


def test_chkOneStudentFalse():
    assert not is_student("Albert good question", "Gabs")


def test_findOneStudent():
    assert find_students("Albert good question", ["Albert"]) == ["Albert"]


def test_findStudents():
    assert find_students("Albert, Gabs good question", ["Albert", "Gabs"]) == ["Albert", "Gabs"]


def test_findSubsetStudents():
    assert find_students("Marie, Gabs good question", ["Albert", "Gabs"]) == ["Gabs"]


def test_newDate():
    # current_info a dictionary with Date, Class, Student and Comment
    current_info = {}
    current_info = update(current_info, "d13Jan1982")
    assert current_info["Date"] == datetime.date(1982, 1, 13)

