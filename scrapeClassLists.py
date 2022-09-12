import re


def student_id(string):
    matches = re.findall(r"^[a-z]+\.[a-z1-9]*", string)
    return matches[0]


def is_member(string):
    matches = re.findall(r"(?!,)membre(?=,)", string)
    return len(matches) == 1
