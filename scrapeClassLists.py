import re


def student_id(str):
    matches = re.findall("^[a-z]+\.[a-z1-9]*", str)
    return matches[0]


def is_member(str):
    matches = re.findall("(?!,)membre(?=,)", str)
    return len(matches) == 1
