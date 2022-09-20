import re
import datetime


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [student for student in students if is_student(string, student)]


def update(current_info, info):
    current_info["Date"] = datetime.date(1982, 1, 13)
    return current_info