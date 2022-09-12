import re


def student_id(str):
    matches = re.findall("^[a-z]+\.[a-z1-9]*", str)
    return matches[0]