import shredComments
import analyseComments
import students
import config


def load_from_config(cfg_path):
    cfg = config.load(cfg_path)
    courses = students.loadClassLists(
        cfg["courses"],
        cfg["class_paths"])
    with open(cfg["comments_path"], "r") as f:
        strings = f.readlines()
    infos = shredComments.shredder(strings, courses)
    df = shredComments.panderize(infos)
    return cfg, courses, df


def report_dnfs(cfg_path):
    cfg, courses, df = load_from_config(cfg_path)
    dnfs = analyseComments.dnf_count_greater_than(df, 0)
    for student, num in dnfs.items():
        print(f"{student}: {num}")
    return dnfs


def latex_report(cfg_path):
    cfg, courses, df = load_from_config(cfg_path)

    with open(cfg["report_student_path"]) as f:
        student_report_outline = f.read()

    course_name = cfg["courses"][0]

    codes = courses[course_name].keys()
    names = courses[course_name].values()
    return analyseComments.latex_report(df, student_report_outline, codes, names, course_name)

