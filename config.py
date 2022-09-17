import yaml


def load(filename):
    with open(filename, 'r') as f:
        config = yaml.safe_load(f)
    config = addClassPaths(config)
    return config


def addClassPaths(config):
    config["class_paths"] = ["../example_files/1ma1dfb01.txt"]
    return config
