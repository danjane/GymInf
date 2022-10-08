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


def codes_names_courseNames(courses):
    student_codes = []
    student_names = []
    course_names = []
    for course, kids in courses.items():
        student_codes += kids.keys()
        student_names += kids.values()
        course_names += [course] * len(kids)
    return student_codes, student_names, course_names


def latex_report(cfg_path):
    cfg, courses, df = load_from_config(cfg_path)

    with open(cfg["report_student_path"]) as f:
        student_report_outline = f.read()

    return analyseComments.latex_report(df, student_report_outline,
                                        *codes_names_courseNames(courses))

