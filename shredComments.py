import re
import datetime


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [student for student in students if is_student(string, student)]


def update(current_info, info):
    current_info["Date"] = datetime.datetime.strptime(info[1:], "%d%b%Y").date()
    return current_info
