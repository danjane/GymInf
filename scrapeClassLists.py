import re


def student_id(string):
    # "dan.jn@eduge.ch,,membre,," -> "dan.jn"
    matches = re.findall(r"^[a-z]+\.[a-z1-9]*", string)
    return matches[0]


def is_member(string):
    # "dan.jn@eduge.ch,,membre,," -> True
    matches = re.findall(r"(?!,)membre(?=,)", string)
    return len(matches) == 1


def student_ids(strings):
    return [student_id(s) for s in strings if is_member(s)]


def text(strings):
    return "\n".join(student_ids(strings))


def scrape_file(file_name):
    with open(file_name) as f:
        string = f.readlines()
    return text(string)
