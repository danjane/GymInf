import sys
import os
import re


def student_code(string):
    # "dan.jn@eduge.ch,,membre,," -> "dan.jn"
    matches = re.findall(r"^[a-z\-]+\.[a-z1-9]*", string)
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
    with open(file_name, 'r') as f:
        string = f.readlines()
    return student_codes(string)


def outFileName(file_name):
    file_name = file_name.replace("rousseau-cours-", "")
    file_name = file_name.replace("rousseau-classe-", "rg")
    file_name = file_name.replace(".csv", ".txt")
    return file_name


def file_paths(dump_file, in_path, out_path):
    in_file = os.path.join(in_path, dump_file)
    out_file = os.path.join(out_path, outFileName(dump_file))
    return in_file, out_file


def write_codes(file_name, codes):
    with open(file_name, 'w') as f:
        f.write('\n'.join(codes))


def load_scrape_write(in_file, out_file):
    codes = scrape_file(in_file)
    write_codes(out_file, codes)


def main():
    if len(sys.argv) != 3:
        raise RuntimeError("Wrong number of args, expected 2 !!")
    in_path = sys.argv[1]
    out_path = sys.argv[2]

    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    files = os.listdir(in_path)
    for file in files:
        load_scrape_write(*file_paths(file, in_path, out_path))


if __name__ == "__main__":
    main()
