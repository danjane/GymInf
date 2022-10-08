import re
import datetime
import pandas as pd


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [k for k, v in students.items() if is_student(string, v)]


def update(current_info, line, courses):
    current_info["Students"] = []
    current_info["DNF"] = 0
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
    for unstripped_line in strings:
        line = unstripped_line.strip()
        if len(line) == 0:
            continue
        current_info = update(current_info, line, courses)
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
    force_columns = dict.fromkeys(["Student", "Date", "Course", "Info", "Sentiment", "DNF"])
    table = pd.DataFrame(infos + [force_columns]*2)
    table = table.drop(["Students"], axis=1)
    table = table[:-2]
    table['Date'] = pd.to_datetime(table.Date, format='%Y-%m-%d')
    return table
