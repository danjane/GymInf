import os
import subprocess
import platform
import config
import students
import linkComments
import analyseNotes
import desk_functions
from datetime import datetime
from typing import Tuple


def start_new_day(cfg: config.AppConfig, course: str):
    file_path = cfg.comments.comments_file
    today = datetime.today().strftime('%d%b%Y').lower()
    with open(file_path, 'a') as f:
        f.write(f"\nd{today}\nc{course}\n")


def setup(cfg_path: str, course: str):
    cfg = config.load(cfg_path)
    start_new_day(cfg, course)
    comments_path = cfg.comments.comments_file
    positive_defaults = cfg.comments.positive_examples
    negative_defaults = cfg.comments.negative_examples

    file_path = cfg.class_list_path(course)
    seating_plan = desk_functions.load_basic_seating_plan_from_file(str(file_path))
    desk_layout = max(v[0] for v in seating_plan.keys()) + 1, max(v[1] for v in seating_plan.keys()) + 1
    return seating_plan, desk_layout, comments_path, positive_defaults, negative_defaults


def open_file(filepath):
    # https://stackoverflow.com/questions/434597
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


def courses(cfg_path: str):
    cfg = config.load(cfg_path)
    return cfg.courses


def load_students(cfg_path, course):
    cfg = config.load(cfg_path)
    class_path = cfg.class_list_path(course)
    student_dict = students.parse_course_list(str(class_path))
    students_codes_and_given_names = [code + ", " + name for code, name in student_dict.items()]
    return students_codes_and_given_names, class_path


def add_courses_in_files(config_file, course, old_courses):
    new_courses = old_courses + [course]
    config.update_courses_in_yaml(config_file, new_courses)
    cfg = config.load(config_file)
    course_file = cfg.class_list_path(course)
    if not os.path.isfile(course_file):
        with open(course_file, 'w') as f:
            f.write("StudentID, StudentName")
    return new_courses


def delete_course_in_files(config_file, deleted_course):
    old_courses = courses(config_file)
    config.update_courses_in_yaml(config_file, [c for c in old_courses if c != deleted_course])


def build_reports(config_file):
    report_file = linkComments.create_report(config_file)
    open_file(report_file)


def calculate_averages(config_file):
    moyennes_file = analyseNotes.dump_all(config_file, None)
    open_file(moyennes_file)
