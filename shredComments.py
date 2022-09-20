import re


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [student for student in students if is_student(string, student)]
