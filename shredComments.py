import re
import datetime


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [student for student in students if is_student(string, student)]


def update(current_info, line, students):
    char, info = line[0], line[1:]
    if char == 'd':
        current_info["Date"] = datetime.datetime.strptime(info, "%d%b%Y").date()
    elif char == 'c':
        current_info["Course"] = info
    elif char == "+":
        current_info["Students"] = find_students(info, students)
    return current_info
