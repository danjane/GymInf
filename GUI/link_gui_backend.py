import os
import config
import students
import linkComments
import GUI.desk_functions
from datetime import datetime
from typing import Dict


def start_new_day(cfg: Dict, course: str):
    file_path = cfg["comments_path"]
    today = datetime.today().strftime('%d%b%Y').lower()
    with open(file_path, 'a') as f:
        f.write(f"\nd{today}\nc{course}\n")


def setup(cfg_path: str, course: str):
    cfg = config.load(cfg_path)
    start_new_day(cfg, course)
    comments_path = cfg["comments_path"]

    file_path = os.path.join(cfg["courses_path"], course + ".txt")
    seating_plan = GUI.desk_functions.load_basic_seating_plan_from_file(file_path)
    desk_layout = max(v[0] for v in seating_plan.keys()) + 1, max(v[1] for v in seating_plan.keys()) + 1
    return seating_plan, desk_layout, comments_path


def courses(cfg_path: str):
    cfg = config.load(cfg_path)
    return cfg["courses"]


def load_students(cfg_path, course):
    cfg = config.load(cfg_path)
    class_path = os.path.join(cfg["courses_path"], course + '.txt')
    student_dict = students.parse_course_list(class_path)
    students_codes_and_given_names = [code + ", " + name for code, name in student_dict.items()]
    return students_codes_and_given_names, class_path


def add_courses_in_files(config_file, course, old_courses):
    new_courses = old_courses + [course]
    config.update_courses_in_yaml(config_file, new_courses)
    cfg = config.load(config_file)
    course_file = os.path.join(cfg["courses_path"], course + ".txt")
    if not os.path.isfile(course_file):
        with open(course_file, 'w') as f:
            f.write("StudentID, StudentName")
    return new_courses


def delete_course_in_files(config_file, deleted_course):
    old_courses = courses(config_file)
    config.update_courses_in_yaml(config_file, [c for c in old_courses if c != deleted_course])


def build_reports(config_file):
    linkComments.create_report(config_file)
