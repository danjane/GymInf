import config

c = config.load("../example_files/config.yaml")


def test_load_class():
    assert c["courses"] == ["1ma1df01", "2ma2dfb01"]


def test_course_path():
    assert c["courses_path"] == "../example_files/"


def test_class_paths():
    assert c["class_paths"] == ["../example_files/1ma1df01.txt", "../example_files/2ma2dfb01.txt"]


def test_config_path():
    assert c["config_path"] == "../example_files/"


def test_comments_path():
    assert c["comments_path"] == "../example_files/comments.txt"