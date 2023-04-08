from students import parse_course_list, load_class_lists, get_code_and_name, check_name_conflicts, \
    get_first_names_in_course, get_first_names_in_courses, create_alias


def test_one_student():
    c = parse_course_list("../example_files/1ma1df01.txt")
    assert c['albert.enstn'] == "Albert"


def test_given_name():
    c = parse_course_list("../example_files/1ma1df01.txt")
    assert c['gabriel.crmr'] == "Gabs"


def test_code_to_name():
    code, name = get_code_and_name("dan.jn")
    assert name == "Dan"
    assert code == "dan.jn"


def test_code_to_given_name():
    code, name = get_code_and_name("dan.jn, Danny")
    assert name == "Danny"
    assert code == "dan.jn"


def test_load_all_classes_from_config():
    courses = load_class_lists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    assert "1ma1df01" in courses
    assert courses["1ma1df01"]['albert.enstn'] == "Albert"
    assert courses["1ma1df01"]['gabriel.crmr'] == "Gabs"


def test_name_conflict_false():
    result = check_name_conflicts({"gabriel.lm": "Gabriel", "gabriel.crmr": "Gabs"})
    assert not result


def test_name_conflict_true():
    result = check_name_conflicts({"gabriel.lm": "Gabs", "gabriel.crmr": "Gabs"})
    assert result == {"Gabs"}


def test_given_names_in_course():
    courses = load_class_lists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    result = get_first_names_in_course(courses["1ma1df01"])
    assert result == ["Albert", "Gabs", "Marie", "Dick"]


def test_given_names_in_courses():
    courses = load_class_lists(["1ma1df01"], ["../example_files/1ma1df01.txt"])
    gn_courses = get_first_names_in_courses(courses)
    assert gn_courses["1ma1df01"] == ["Albert", "Gabs", "Marie", "Dick"]


def test_dip_email_from_name():
    assert create_alias("Albert Einstein") == "albert.enstn"
    assert create_alias("Gabriel Lame Cramer") == "gabriel.crmr"
    assert create_alias("Marie Curie") == "marie.cr"
    assert create_alias("Richard Feynman") == "richard.fynmn"
