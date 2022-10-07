import re


def code_and_name(s_dirty):
    s = s_dirty.strip().split(', ')
    code = s[0]
    if len(s) == 1:
        name = re.search(r"^[a-z\-]+", code).group(0).capitalize()
    else:
        name = s[1]
    return code, name


def duplicate_warning(duplicates):
    print(f"The following names are duplicated!! {duplicates}")


def name_conflict(name_dict):
    names = list(name_dict.values())
    duplicates = set([name for name in names if names.count(name) > 1])
    if duplicates:
        duplicate_warning(duplicates)
    return duplicates


def course_list(filename):
    with open(filename, 'r') as f:
        values = {}
        for s_dirty in f.readlines():
            c, n = code_and_name(s_dirty)
            values[c] = n
    return values


def loadClassLists(course_names, class_paths):
    classes = {}
    for cls, path in zip(course_names, class_paths):
        classes[cls] = course_list(path)
    return classes


def firstNamesInCourse(course):
    return list(course.values())


def firstNamesInCourses(courses):
    courses_with_given_name = {}
    for course_name, students in courses.items():
        courses_with_given_name[course_name] = firstNamesInCourse(students)
    return courses_with_given_name
