import os.path
import subprocess

import shredComments
import analyseComments
import students
import config
import pandas as pd
from typing import Dict, List, Tuple, Union


def load_comments_as_dataframe(comments_path: str, courses: Dict[str, Dict[str, str]]) -> pd.DataFrame:
    with open(comments_path, "r") as f:
        strings = f.readlines()
    infos = shredComments.shred(strings, courses)
    df = shredComments.panderize(infos)
    return df


def load_data_from_config_path(cfg_path: str) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, str]], pd.DataFrame]:
    cfg = config.load(cfg_path)
    courses = students.load_class_lists(cfg["courses"], cfg["class_paths"])
    df = load_comments_as_dataframe(cfg["comments_path"], courses)
    return cfg, courses, df


def report_dnfs(cfg_path: str, cut_off: int = 0) -> Dict[str, int]:
    cfg, courses, df = load_data_from_config_path(cfg_path)
    dnfs = analyseComments.count_dnf_greater_than(df, cut_off)
    for student, num in dnfs.items():
        print(f"{student}: {num}")
    return dnfs


def get_student_codes_names_course_names(courses: Dict[str, Dict[str, str]]) -> Tuple[List[str], List[str], List[str]]:
    student_codes = []
    student_names = []
    course_names = []
    for course, kids in courses.items():
        student_codes += list(kids.keys())
        student_names += list(kids.values())
        course_names += [course] * len(kids)
    return student_codes, student_names, course_names


def build_latex_report(cfg: Dict[str, Union[str, List[str]]], courses: Dict[str, Dict[str, str]], df: pd.DataFrame) -> str:
    with open(cfg["report_student_path"]) as f:
        student_report_outline = f.read()
    with open(cfg["report_skeleton_path"]) as f:
        report_skeleton = f.read()
    pages = analyseComments.latex_student_pages(df, student_report_outline,
                                                *get_student_codes_names_course_names(courses))
    report = report_skeleton.replace("STUDENTPAGES", pages)
    return report


def get_latex_report_from_config_path(cfg_path: str) -> str:
    cfg, courses, df = load_data_from_config_path(cfg_path)
    report = build_latex_report(cfg, courses, df)
    return report


def latex_to_pdf(tex_file, output_directory):
    try:
        process = subprocess.Popen(['pdflatex', '-output-directory', output_directory, tex_file],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print("Compilation successful!")
        else:
            print("Compilation failed. Error message:")
            print(stderr.decode())

    except FileNotFoundError:
        print("pdflatex command not found. Please ensure that LaTeX is installed.")

    pdf_file = tex_file[:-3] + "pdf"
    if os.path.isfile(pdf_file):
        return pdf_file
    else:
        print("pdf was NOT created from tex file!!")
        return tex_file


def create_report(cfg_path: str) -> str:
    report = get_latex_report_from_config_path(cfg_path)
    cfg = config.load(cfg_path)
    report_file = cfg["report_tex_path"]
    report_dir = os.path.dirname(report_file)
    with open(report_file, "w") as f:
        f.write(report)
    pdf_file = latex_to_pdf(report_file, report_dir)
    return pdf_file


def get_students_needing_comments_from_config_path(cfg_path: str, course: str) -> List[str]:
    cfg, courses, df = load_data_from_config_path(cfg_path)
    ss = analyseComments.comments_needed(df, list(courses[course].keys()))
    return [courses[course][s] for s in ss]
