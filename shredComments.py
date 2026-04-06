from dataclasses import asdict, dataclass, field
from datetime import date
import datetime
import re
from typing import Dict, List, Optional

import pandas as pd


@dataclass
class CommentContext:
    date: Optional[date] = None
    course: Optional[str] = None
    students: List[str] = field(default_factory=list)
    info: str = ""
    sentiment: int = 0
    dnf: int = 0


@dataclass
class CommentEntry:
    student: str
    date: date
    course: str
    info: str
    sentiment: int
    dnf: int
    students: List[str] = field(default_factory=list)

    def to_row(self) -> Dict[str, object]:
        row = asdict(self)
        row["Student"] = row.pop("student")
        row["Date"] = row.pop("date")
        row["Course"] = row.pop("course")
        row["Info"] = row.pop("info")
        row["Sentiment"] = row.pop("sentiment")
        row["DNF"] = row.pop("dnf")
        row["Students"] = row.pop("students")
        return row


def is_student(string, student):
    return re.search(student, string)


def find_students(string, students):
    return [k for k, v in students.items() if is_student(string, v)]


def update(current_info, line, courses):
    if isinstance(current_info, dict):
        current_info = CommentContext(
            date=current_info.get("Date"),
            course=current_info.get("Course"),
            students=list(current_info.get("Students", [])),
            info=current_info.get("Info", ""),
            sentiment=current_info.get("Sentiment", 0),
            dnf=current_info.get("DNF", 0),
        )

    current_info.students = []
    current_info.dnf = 0
    current_info.sentiment = 0
    char, info = line[0], line[1:]
    if char == "d":
        current_info.date = datetime.datetime.strptime(info, "%d%b%Y").date()
    elif char == "c":
        current_info.course = info
    elif char == "" or char == "#":
        pass
    else:
        all_students = current_students(current_info, courses)
        current_info.students = find_students(info, all_students)
        current_info.info = line
        if char == "+":
            current_info.sentiment = 1
        elif char == "-":
            current_info.sentiment = -1
        elif char == "D":
            current_info.sentiment = -1
            current_info.dnf = 1
        elif char == "r":
            current_info.dnf = -2
        elif char == "R":
            current_info.dnf = -10
            if not current_info.students:
                current_info.students = list(all_students)
        else:
            print(line)
            raise NotImplementedError("These are not the droids you're looking for!!")
    return current_info


def shred(strings, courses):
    current_info = CommentContext()
    infos: List[CommentEntry] = []
    for unstripped_line in strings:
        line = unstripped_line.strip()
        if len(line) == 0:
            continue
        current_info = update(current_info, line, courses)
        for student in current_info.students:
            infos.append(
                CommentEntry(
                    student=student,
                    date=current_info.date,
                    course=current_info.course,
                    info=current_info.info,
                    sentiment=current_info.sentiment,
                    dnf=current_info.dnf,
                    students=list(current_info.students),
                )
            )
    return infos


def current_students(current_info, courses):
    course = current_info.course if isinstance(current_info, CommentContext) else current_info.get("Course")
    if not course:
        return []
    elif course not in courses:
        return []
    else:
        return courses[course]


def reset_dnfs(df):
    for student in df["Student"].unique():
        student_idx = df["Student"] == student
        dnf_list = list(df.loc[student_idx, "DNF"])
        df.loc[student_idx, "DNF"] = reset_dnf_list_one_student(dnf_list)
    return df


def reset_dnf_list_one_student(dnfs):
    for i in range(len(dnfs) - 1, 0, -1):
        if dnfs[i] == -10:
            dnfs[: i + 1] = [0] * (i + 1)
            break
    return dnfs


def panderize(infos):
    force_columns = dict.fromkeys(["Students", "Student", "Date", "Course", "Info", "Sentiment", "DNF"])
    rows = [info.to_row() if isinstance(info, CommentEntry) else info for info in infos]
    table = pd.DataFrame(rows + [force_columns] * 2)
    table = table.drop(["Students"], axis=1)
    table = table[:-2]
    table["Date"] = pd.to_datetime(table.Date, format="%Y-%m-%d")
    table = reset_dnfs(table)
    return table
