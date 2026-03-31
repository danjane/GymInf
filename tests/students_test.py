from students import parse_course_list, load_class_lists, get_code_and_name, check_name_conflicts, \
    get_first_names_in_course, get_first_names_in_courses, create_alias
from pathlib import Path

EXAMPLE_FILES = Path(__file__).resolve().parents[1] / "example_files"

# Test for single student in the list with proper format "SURNAME GivenName"
def test_one_student():
    c = parse_course_list(str(EXAMPLE_FILES / "1ma1df01.txt"))
    assert c['EINSTEIN Albert'] == "Albert"  # Key format is "SURNAME GivenName"

# Test for a student with a nickname, where the key is in "SURNAME GivenName" format
def test_given_name():
    c = parse_course_list(str(EXAMPLE_FILES / "1ma1df01.txt"))
    assert c['CRAMER Gabriel'] == "Gabs"  # Key in the format "SURNAME GivenName" with nickname expected

# Test code and name extraction for email alias, given the full name format "SURNAME GivenName"
def test_code_to_name():
    code, name = get_code_and_name("EINSTEIN Albert")
    assert name == "Albert"
    assert code == "EINSTEIN Albert"

# Test code to given name when alias includes the full name "SURNAME GivenName, GivenName"
def test_code_to_given_name():
    code, name = get_code_and_name("EINSTEIN Albert, Albert")
    assert name == "Albert"
    assert code == "EINSTEIN Albert"

# Test loading all students in a class list
def test_load_all_classes_from_config():
    courses = load_class_lists(["1ma1df01"], [str(EXAMPLE_FILES / "1ma1df01.txt")])
    assert "1ma1df01" in courses
    assert courses["1ma1df01"]['EINSTEIN Albert'] == "Albert"  # Full name used as key
    assert courses["1ma1df01"]['CRAMER Gabriel'] == "Gabs"     # Full name used as key

# Test for no name conflicts (when different keys have distinct names)
def test_name_conflict_false():
    result = check_name_conflicts({"LAM Gabriel": "Gabriel", "CRAMER Gabriel": "Gabs"})
    assert not result

# Test for name conflicts (when different keys have the same name)
def test_name_conflict_true():
    result = check_name_conflicts({"LAM Gabriel": "Gabs", "CRAMER Gabriel": "Gabs"})
    assert result == {"Gabs"}

# Test for extracting first names in a single course
def test_given_names_in_course():
    courses = load_class_lists(["1ma1df01"], [str(EXAMPLE_FILES / "1ma1df01.txt")])
    result = get_first_names_in_course(courses["1ma1df01"])
    assert result == ["Albert", "Gabs", "Marie", "Dick"]  # List of first names expected

# Test for extracting first names across multiple courses
def test_given_names_in_courses():
    courses = load_class_lists(["1ma1df01"], [str(EXAMPLE_FILES / "1ma1df01.txt")])
    gn_courses = get_first_names_in_courses(courses)
    assert gn_courses["1ma1df01"] == ["Albert", "Gabs", "Marie", "Dick"]  # First names from the specific course

# Test for creating email aliases from full names
def test_dip_email_from_name():
    assert create_alias("Albert Einstein") == "albert.enstn"  # Generate alias from name
    assert create_alias("Gabriel Lame Cramer") == "gabriel.crmr"
    assert create_alias("Marie Curie") == "marie.cr"
    assert create_alias("Richard Feynman") == "richard.fynmn"
