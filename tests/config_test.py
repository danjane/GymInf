import config

c = config.load("../example_files/config.yaml")


def test_loadClass():
    assert c["courses"] == ["1ma1df01"]


def test_coursePath():
    assert c["courses_path"] == "../example_files/"


def test_classPaths():
    assert c["class_paths"] == ["../example_files/1ma1df01.txt"]


def test_configPath():
    assert c["config_path"] == "../example_files/"
