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
        return adjust_path_for_cxfreeze(filename)
    else:
        return filename

def load(filename: str) -> Dict[str, Any]:
    with open(cx(filename), 'r') as f:
        config = yaml.safe_load(f)
    config = add_class_paths(config)
    return config


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
    with open(cx(filename), 'w') as f:
        yaml.safe_dump(config, f)
