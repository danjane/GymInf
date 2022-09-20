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
    # current_info a dictionary with Date, Course, Students, Sentiment and Comment
    current_info = {"Students": ["this" "is not", "good"]}
    current_info = update(current_info, "d13Jan1982", ["Albert", "Gabs"])
    assert current_info["Date"] == datetime.date(1982, 1, 13)
    assert current_info["Students"] == []


def test_newCourse():
    current_info = {"Students": ["this" "is not", "good"]}
    current_info = update(current_info, "c1ma1df01", ["Albert", "Gabs"])
    assert current_info["Course"] == "1ma1df01"
    assert current_info["Students"] == []


def test_newInfoForOneStudent():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    current_info = update(current_info, "+Albert good question", courses)
    assert current_info["Students"] == ["Albert"]
    assert current_info["Sentiment"] == 1


def test_dnfForOneStudent():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    current_info = update(current_info, "DNF Albert", courses)
    assert current_info["Students"] == ["Albert"]
    assert current_info["Sentiment"] == -1
    assert current_info["DNF"] == 1


def test_resetDnfForOneStudent():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    current_info = update(current_info, "reset Albert", courses)
    assert current_info["Students"] == ["Albert"]
    assert current_info["DNF"] == -2


def test_newInfoForTwoStudents():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    current_info = update(current_info, "+Albert, Gabs good question", courses)
    assert current_info["Students"] == ["Albert", "Gabs"]
    assert current_info["Sentiment"] == 1


def test_newInfoForBadStudent():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    current_info = update(current_info, "-Albert faster than c", courses)
    assert current_info["Students"] == ["Albert"]
    assert current_info["Sentiment"] == -1


def test_updatesForDateClassOneStudent():
    strings = \
        """d25Dec2022
        c1ma1df01
        +Albert great question""".split("\n")
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    infos = shredder(strings, courses)
    assert len(infos) == 1

    current_info = infos[0]
    assert current_info["Students"] == ["Albert"]
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1


def test_updatesForDateClassTwoStudents():
    strings = \
        """d25Dec2022
        c1ma1df01
        +Albert, Gabs great question""".split("\n")
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    infos = shredder(strings, courses)
    assert len(infos) == 2

    current_info = infos[0]
    assert current_info["Student"] == "Albert"
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1

    current_info = infos[1]
    assert current_info["Student"] == "Gabs"
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1


def test_currentStudentsNone():
    current_info = {}
    courses = {}
    assert current_students(current_info, courses) == []


def test_currentStudentsNotFound():
    current_info = {"Course": "Def not good"}
    courses = {}
    assert current_students(current_info, courses) == []


def test_currentStudentsInCourse():
    current_info = {"Course": "1ma1df01"}
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    assert current_students(current_info, courses) == ["Albert", "Gabs"]


def test_panderizeTwoStudents():
    strings = \
        """d25Dec2022
        c1ma1df01
        +Albert, Gabs great question""".split("\n")
    courses = {"1ma1df01": ["Albert", "Gabs"]}
    infos = shredder(strings, courses)
    table = panderize(infos)
    assert table.size == 10
    assert "Course" in table.columns
    assert "Student" in table.columns
    assert "Date" in table.columns
    assert "Sentiment" in table.columns
    assert "Info" in table.columns
    assert table["Course"][0] == "1ma1df01"
    assert table["Info"][1] == "+Albert, Gabs great question"
    assert list(table["Student"]) == ["Albert", "Gabs"]
