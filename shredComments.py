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
    else:
        current_info["Students"] = find_students(info, students)
        if char == "+":
            current_info["Sentiment"] = 1
        elif char == "-":
            current_info["Sentiment"] = -1
        else:
            raise NotImplementedError("These are not the droids you're looking for!!")
    return current_info
