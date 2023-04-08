import yaml
import os
from typing import Dict, Any


def load(filename: str) -> Dict[str, Any]:
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    config = add_class_paths(config)
    return config


def add_class_paths(config: Dict[str, Any]) -> Dict[str, Any]:
    folder = config["courses_path"]
    courses = config["courses"]
    paths = [os.path.join(folder, cls + ".txt") for cls in courses]
    config["class_paths"] = paths
    return config
