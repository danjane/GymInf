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
    # current_info a dictionary with Date, Course, Students and Comment
    current_info = {}
    current_info = update(current_info, "d13Jan1982", ["Albert", "Gabs"])
    assert current_info["Date"] == datetime.date(1982, 1, 13)


def test_newCourse():
    current_info = {}
    current_info = update(current_info, "c1ma1df01", ["Albert", "Gabs"])
    assert current_info["Course"] == "1ma1df01"


def test_newInfoForOneStudent():
    current_info = {}
    current_info = update(current_info, "+Albert good question", ["Albert", "Gabs"])
    assert current_info["Students"] == ["Albert"]


def test_newInfoForTwoStudent():
    current_info = {}
    current_info = update(current_info, "+Albert, Gabs good question", ["Albert", "Gabs"])
    assert current_info["Students"] == ["Albert", "Gabs"]
