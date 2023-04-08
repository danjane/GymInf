import shredComments
import analyseComments
import students
import config


def load_comments_as_DataFrame(comments_path, courses):
    with open(comments_path, "r") as f:
        strings = f.readlines()
    infos = shredComments.shredder(strings, courses)
    df = shredComments.panderize(infos)
    return df


def load_from_config_path(cfg_path):
    cfg = config.load(cfg_path)
    courses = students.loadClassLists(
        cfg["courses"],
        cfg["class_paths"])
    df = load_comments_as_DataFrame(cfg["comments_path"], courses)
    return cfg, courses, df


def report_dnfs(cfg_path, cut_off=0):
    cfg, courses, df = load_from_config_path(cfg_path)
    dnfs = analyseComments.count_dnf_greater_than(df, cut_off)
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


def build_latex_report(cfg, courses, df):
    with open(cfg["report_student_path"]) as f:
        student_report_outline = f.read()
    with open(cfg["report_skeleton_path"]) as f:
        report_skeleton = f.read()
    pages = analyseComments.latex_student_pages(df, student_report_outline,
                                                *codes_names_courseNames(courses))
    report = report_skeleton.replace("STUDENTPAGES", pages)
    return report


def latex_report_from_config_path(cfg_path):
    cfg, courses, df = load_from_config_path(cfg_path)
    report = build_latex_report(cfg, courses, df)
    return report
