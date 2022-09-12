import re


def student_code(string):
    # "dan.jn@eduge.ch,,membre,," -> "dan.jn"
    matches = re.findall(r"^[a-z]+\.[a-z1-9]*", string)
    return matches[0]


def is_member(string):
    # "dan.jn@eduge.ch,,membre,," -> True
    matches = re.findall(r"(?!,)membre(?=,)", string)
    return len(matches) == 1


def alphabetic(codes):
    surnames = [code.split(".")[1] for code in codes]
    # sort on surnames (in the first position) but use whole code (in second position)
    codes = [x for _, x in sorted(zip(surnames, codes))]
    return codes


def student_codes(strings):
    ids = [student_code(s) for s in strings if is_member(s)]
    return alphabetic(ids)


def text(strings):
    return "\n".join(student_codes(strings))


def scrape_file(file_name):
    with open(file_name) as f:
        string = f.readlines()
    return student_codes(string)


def outFileName(file_name):
    file_name = file_name.replace("rousseau-cours-", "")
    file_name = file_name.replace("rousseau-classe-", "rg")
    file_name = file_name.replace(".csv", ".txt")
    return file_name
