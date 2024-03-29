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
    current_info["Sentiment"] = 0
    char, info = line[0], line[1:]
    if char == 'd':
        current_info["Date"] = datetime.datetime.strptime(info, "%d%b%Y").date()
    elif char == 'c':
        current_info["Course"] = info
    else:
        all_students = current_students(current_info, courses)
        current_info["Students"] = find_students(info, all_students)
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
        elif char == "R":
            current_info["DNF"] = -10
            if not current_info["Students"]:
                current_info["Students"] = all_students
        elif char == "":
            pass
        else:
            print(line)
            raise NotImplementedError("These are not the droids you're looking for!!")
    return current_info


def shred(strings, courses):
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


def reset_dnfs(df):
    for student in df["Student"].unique():
        student_idx = df["Student"] == student
        dnf_list = list(df.loc[student_idx, 'DNF'])
        df.loc[student_idx, 'DNF'] = reset_dnf_list_one_student(dnf_list)
    return df


def reset_dnf_list_one_student(dnfs):
    for i in range(len(dnfs)-1, 0, -1):
        if dnfs[i] == -10:
            dnfs[:i + 1] = [0] * (i + 1)
            break
    return dnfs


def panderize(infos):
    force_columns = dict.fromkeys(["Students", "Student", "Date", "Course", "Info", "Sentiment", "DNF"])
    table = pd.DataFrame(infos + [force_columns] * 2)
    table = table.drop(["Students"], axis=1)
    table = table[:-2]
    table['Date'] = pd.to_datetime(table.Date, format='%Y-%m-%d')  # TODO should this be %d%b%Y ?
    table = reset_dnfs(table)
    return table
