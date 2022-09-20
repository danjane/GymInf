import re
import datetime
import pandas as pd


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [student for student in students if is_student(string, student)]


def update(current_info, line, courses):
    current_info["Students"] = []
    char, info = line[0], line[1:]
    if char == 'd':
        current_info["Date"] = datetime.datetime.strptime(info, "%d%b%Y").date()
    elif char == 'c':
        current_info["Course"] = info
    else:
        students = current_students(current_info, courses)
        current_info["Students"] = find_students(info, students)
        current_info["Info"] = line
        if char == "+":
            current_info["Sentiment"] = 1
        elif char == "-":
            current_info["Sentiment"] = -1
        elif char == "D":
            current_info["Sentiment"] = -1
            current_info["DNF"] = 1
        elif char == "r":
            current_info["DNF"] = -2
        else:
            raise NotImplementedError("These are not the droids you're looking for!!")
    return current_info


def shredder(strings, courses):
    current_info = {}
    infos = []
    for line in strings:
        if len(line) == 0:
            continue
        current_info = update(current_info, line.strip(), courses)
        for student in current_info["Students"]:
            c = current_info.copy()
            c["Student"] = student
            infos.append(c)
    return infos


def current_students(current_info, courses):
    if "Course" not in current_info:
        return []
    elif current_info["Course"] not in courses:
        return []
    else:
        return courses[current_info["Course"]]


def panderize(infos):
    if len(infos) < 2:
        raise NotImplementedError("Need more data!!")
    else:
        table = pd.DataFrame(infos)
        table = table.drop(["Students"], axis=1)
        return table
