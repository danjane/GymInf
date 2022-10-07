import shredComments
import analyseComments
import students
import config


def report_dnfs(cfg_path):
    cfg = config.load(cfg_path)
    courses = students.loadClassLists(
        cfg["courses"],
        cfg["class_paths"])

    with open(cfg["comments_path"], "r") as f:
        strings = f.readlines()
    infos = shredComments.shredder(strings, courses)
    df = shredComments.panderize(infos)
    dnfs = analyseComments.dnf_count_positives(df)
    for student, num in dnfs.items():
        print(f"{student}: {num}")
    return dnfs
