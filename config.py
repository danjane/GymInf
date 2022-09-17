import yaml
import os

def load(filename):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    config = addClassPaths(config)
    return config


def addClassPaths(config):
    folder = config["courses_path"]
    courses = config["courses"]
    paths = [os.path.join(folder, cls + ".txt") for cls in courses]
    config["class_paths"] = paths
    return config
