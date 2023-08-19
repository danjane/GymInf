import yaml
import os
import sys
from typing import Dict, Any


def adjust_path_for_cxfreeze(path):
    working_dir, _ = os.path.split(sys.executable)
    return os.path.join(working_dir, path)


def cx(filename):
    cxfreeze_executable_flag = getattr(sys, "frozen", False)
    if cxfreeze_executable_flag:
        # return adjust_path_for_cxfreeze(filename)
        return filename
    else:
        return filename


def ispath(obj):
    return isinstance(obj, str) and len(obj) > 1 and obj[0] == "."


def load(filename: str) -> Dict[str, Any]:
    with open(cx(filename), 'r') as f:
        config = yaml.safe_load(f)
    for k, v in config.items():
        if ispath(v):
            config[k] = cx(v)
    config = add_class_paths(config)
    return config


def mkdir_if_nec(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def save(config, filename):
    with open(cx(filename), 'w') as f:
        yaml.safe_dump(config, f)


def add_class_paths(config: Dict[str, Any]) -> Dict[str, Any]:
    folder = cx(config["courses_path"])
    courses = config["courses"]
    paths = [os.path.join(folder, cls + ".txt") for cls in courses]
    config["class_paths"] = paths
    return config


def update_courses_in_yaml(filename, courses):
    with open(cx(filename), 'r') as f:
        config = yaml.safe_load(f)
    config["courses"] = courses
    save(config, filename)


def default_config(base_path):
    return {
        "courses": [],
        "courses_path": base_path,
        "config_path": base_path,
        "comments_path": os.path.join(base_path, "comments.txt"),
        "exam_path": os.path.join(base_path, "exams"),
        "exam_averages_path": os.path.join(base_path, "exams", "big_dump.xlsx"),
        "positive_comments_defaults_path": os.path.join(base_path, "positive_comments_examples.txt"),
        "negative_comments_defaults_path": os.path.join(base_path, "negative_comments_examples.txt"),
        "latex_path": os.path.join(base_path, "latex"),
        "report_skeleton_path": os.path.join(base_path, "latex", "report_skeleton.tex"),
        "report_student_path": os.path.join(base_path, "latex", "report_outline_student.tex"),
        "report_tex_path": os.path.join(base_path, "latex", "report.tex")
    }


def setup_from_cfg(cfg):
    for field in ["config_path", "courses_path", "exam_path", "latex_path"]:
        folder = cfg[field]
        mkdir_if_nec(folder)
    open(cfg["comments_path"], 'w').close()
    with open(cfg["positive_comments_defaults_path"], 'w') as f:
        f.write("correct response\ngood question\nTN for Pythag\nquick work")
    with open(cfg["negative_comments_defaults_path"], 'w') as f:
        f.write("DNF\nChatting")
    with open(cfg["report_skeleton_path"], 'w') as f:
        f.write("\\documentclass[11pt]{article}\n\\begin{document}\nSTUDENTPAGES\n\\end{document}")
    with open(cfg["report_student_path"], 'w') as f:
        f.write("STUDENTCODE \\hfill \\textbf{STUDENTNAME} \\hfill COURSE \\\\ \nSTUDENTCOMMENTS")


def create_default(f):
    base_path, _ = os.path.split(f)
    mkdir_if_nec(base_path)
    config = default_config(base_path)
    setup_from_cfg(config)
    save(config, f)
    return config


def create_default_if_nec(f):
    if not os.path.isfile(f):
        create_default(f)