import re
from typing import Dict, List, Tuple


def get_code_and_name(student_code: str) -> Tuple[str, str]:
    student_code = student_code.strip().split(', ')
    course_code = student_code[0]
    if len(student_code) == 1:
        course_name = re.search(r"^[a-z\-]+", course_code).group(0).capitalize()
    else:
        course_name = student_code[1]
    return course_code, course_name


def warn_about_duplicates(duplicates: set) -> None:
    print(f"The following names are duplicated!! {duplicates}")


def check_name_conflicts(name_dict: Dict[str, str]) -> set:
    names = list(name_dict.values())
    duplicates = set([name for name in names if names.count(name) > 1])
    if duplicates:
        warn_about_duplicates(duplicates)
    return duplicates


def parse_course_list(filename: str) -> Dict[str, str]:
    with open(filename, 'r') as f:
        values = {}
        for student_info in f.readlines():
            student_code, student_name = get_code_and_name(student_info)
            values[student_code] = student_name
    return values


def load_class_lists(course_names: List[str], class_paths: List[str]) -> Dict[str, Dict[str, str]]:
    classes = {}
    for course_name, path in zip(course_names, class_paths):
        classes[course_name] = parse_course_list(path)
    return classes


def get_first_names_in_course(course: Dict[str, str]) -> List[str]:
    return list(course.values())


def get_first_names_in_courses(courses: Dict[str, Dict[str, str]]) -> Dict[str, List[str]]:
    courses_with_given_name = {}
    for course_name, students in courses.items():
        courses_with_given_name[course_name] = get_first_names_in_course(students)
    return courses_with_given_name


def create_alias(full_name: str) -> str:
    first_name, *surnames = full_name.split()
    surname = surnames[-1]
    first_letter = surname[0]
    vowels = "AEIOUaeiou"
    surname_alias = "".join([c for c in surname if c not in vowels])
    if first_letter in vowels:
        surname_alias = first_letter + surname_alias
    return f"{first_name.lower()}.{surname_alias.lower()}"
