from shredComments import *
import datetime
from typing import Dict, List, Union

Courses = Dict[str, Dict[str, str]]
DateInfo = Dict[str, Union[datetime.date, str, List[str], int]]

courses: Courses = {"1ma1df01": {"albert.enstn": "Albert", "gabriel.crmr": "Gabs"}}


def test_check_one_student_true() -> None:
    assert is_student("Albert good question", "Albert")


def test_check_one_student_false() -> None:
    assert not is_student("Albert good question", "Gabs")


def test_find_one_student() -> None:
    assert find_students("Albert good question", courses["1ma1df01"]) == ["albert.enstn"]


def test_find_students() -> None:
    assert find_students("Albert, Gabs good question", courses["1ma1df01"]) == ["albert.enstn", "gabriel.crmr"]


def test_find_subset_students() -> None:
    assert find_students("Marie, Gabs good question", courses["1ma1df01"]) == ["gabriel.crmr"]


def test_new_date() -> None:
    current_info: DateInfo = {"Students": ["this" "is not", "good"]}
    current_info = update(current_info, "d13Jan1982", courses)
    assert current_info["Date"] == datetime.date(1982, 1, 13)
    assert current_info["Students"] == []


def test_new_course() -> None:
    current_info: DateInfo = {"Students": ["this" "is not", "good"]}
    current_info = update(current_info, "c1ma1df01", courses)
    assert current_info["Course"] == "1ma1df01"
    assert current_info["Students"] == []


def test_new_info_for_one_student() -> None:
    current_info: DateInfo = {"Course": "1ma1df01"}
    current_info = update(current_info, "+Albert good question", courses)
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["Sentiment"] == 1


def test_dnf_for_one_student() -> None:
    current_info: DateInfo = {"Course": "1ma1df01"}
    current_info = update(current_info, "DNF Albert", courses)
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["Sentiment"] == -1
    assert current_info["DNF"] == 1


def test_dnf_then_good_for_one_student() -> None:
    current_info: Dict[str, any] = {"Course": "1ma1df01"}
    current_info = update(current_info, "DNF Albert", courses)
    current_info = update(current_info, "+Albert bonne réponse", courses)
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["Sentiment"] == 1
    assert current_info["DNF"] == 0


def test_reduce_dnf_for_one_student() -> None:
    current_info: Dict[str, any] = {"Course": "1ma1df01"}
    current_info = update(current_info, "reset Albert", courses)
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["DNF"] == -2


def test_new_info_for_two_students() -> None:
    current_info: Dict[str, any] = {"Course": "1ma1df01"}
    current_info = update(current_info, "+Albert, Gabs good question", courses)
    assert current_info["Students"] == ["albert.enstn", "gabriel.crmr"]
    assert current_info["Sentiment"] == 1


def test_new_info_for_bad_student() -> None:
    current_info: Dict[str, any] = {"Course": "1ma1df01"}
    current_info = update(current_info, "-Albert faster than c", courses)
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["Sentiment"] == -1


def test_updates_for_date_class_one_student() -> None:
    strings: List[str] = """d25Dec2022
    c1ma1df01
    +Albert great question""".split("\n")
    infos: List[Dict[str, any]] = shred(strings, courses)
    assert len(infos) == 1

    current_info: Dict[str, any] = infos[0]
    assert current_info["Students"] == ["albert.enstn"]
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1


def test_updates_for_date_class_two_students() -> None:
    strings: List[str] = """d25Dec2022
    c1ma1df01
    +Albert, Gabs great question""".split("\n")
    infos: List[Dict[str, any]] = shred(strings, courses)
    assert len(infos) == 2

    current_info: Dict[str, any] = infos[0]
    assert current_info["Student"] == "albert.enstn"
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1

    current_info: Dict[str, any] = infos[1]
    assert current_info["Student"] == "gabriel.crmr"
    assert current_info["Date"] == datetime.date(2022, 12, 25)
    assert current_info["Sentiment"] == 1


def test_current_students_none() -> None:
    current_info: Dict[str, any] = {}
    assert current_students(current_info, {}) == []


def test_current_students_not_found() -> None:
    current_info: Dict[str, any] = {"Course": "Def not good"}
    assert current_students(current_info, {}) == []


def test_panderize_two_students():
    strings = \
        """d25Dec2022
        c1ma1df01
        +Albert, Gabs great question""".split("\n")
    infos = shred(strings, courses)
    table = panderize(infos)
    assert table.size == 12
    assert "Course" in table.columns
    assert "Student" in table.columns
    assert "Date" in table.columns
    assert "Sentiment" in table.columns
    assert "Info" in table.columns
    assert "DNF" in table.columns
    assert table["Course"][0] == "1ma1df01"
    assert table["Info"][1] == "+Albert, Gabs great question"
    assert list(table["Student"]) == ["albert.enstn", "gabriel.crmr"]


def test_panderize_with_no_students_only_class_date():
    strings = \
        """d25Dec2022
        c1ma1df01""".split("\n")
    infos = shred(strings, courses)
    table = panderize(infos)
    assert table.shape == (0, 6)
    assert "Course" in table.columns
    assert "Student" in table.columns
    assert "Date" in table.columns
    assert "Sentiment" in table.columns
    assert "Info" in table.columns
    assert "DNF" in table.columns


def test_reset_dnfs_one_student():
    strings = \
        """d25Dec2022
        c1ma1df01
        DNF Albert, Gabs
        DNF Gabs
        Reset Albert
        """.split("\n")
    infos = shred(strings, courses)
    table = panderize(infos)
    assert sum(table.loc[table["Student"] == "albert.enstn", "DNF"]) == 0
    assert sum(table.loc[table["Student"] == "gabriel.crmr", "DNF"]) == 2


def test_reset_dnfs_all_students():
    strings = \
        """d25Dec2022
        c1ma1df01
        DNF Albert, Gabs
        DNF Gabs
        Reset all
        """.split("\n")
    infos = shred(strings, courses)
    table = panderize(infos)
    assert sum(table.loc[table["Student"] == "albert.enstn", "DNF"]) == 0
    assert sum(table.loc[table["Student"] == "gabriel.crmr", "DNF"]) == 0


