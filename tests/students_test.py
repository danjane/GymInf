from students import course_list, loadClassLists, code_and_name, name_conflict, \
    firstNamesInCourse, firstNamesInCourses, create_alias


def test_one_student():
    c = course_list("../example_files/1ma1df01.txt")
    assert c['albert.enstn'] == "Albert"


def test_given_name():
    c = course_list("../example_files/1ma1df01.txt")
    assert c['gabriel.crmr'] == "Gabs"


def test_code_to_name():
    code, name = code_and_name("dan.jn")
    assert name == "Dan"
    assert code == "dan.jn"


def test_code_to_given_name():
    code, name = code_and_name("dan.jn, Danny")
    assert name == "Danny"
    assert code == "dan.jn"


def test_load_all_classes_from_config():
    courses = loadClassLists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    assert "1ma1df01" in courses
    assert courses["1ma1df01"]['albert.enstn'] == "Albert"
    assert courses["1ma1df01"]['gabriel.crmr'] == "Gabs"


def test_name_conflict_false():
    result = name_conflict({"gabriel.lm": "Gabriel", "gabriel.crmr": "Gabs"})
    assert not result


def test_name_conflict_true():
    result = name_conflict({"gabriel.lm": "Gabs", "gabriel.crmr": "Gabs"})
    assert result == {"Gabs"}


def test_given_names_in_course():
    courses = loadClassLists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    result = firstNamesInCourse(courses["1ma1df01"])
    assert result == ["Albert", "Gabs", "Marie", "Dick"]


def test_given_names_in_courses():
    courses = loadClassLists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    gn_courses = firstNamesInCourses(courses)
    assert gn_courses["1ma1df01"] == ["Albert", "Gabs", "Marie", "Dick"]


def test_dip_email_from_name():
    assert create_alias("Albert Einstein") == "albert.enstn"
    assert create_alias("Gabriel Lame Cramer") == "gabriel.crmr"
    assert create_alias("Marie Curie") == "marie.cr"
    assert create_alias("Richard Feynman") == "richard.fynmn"
