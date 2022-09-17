import config

c = config.load("../example_files/config.yaml")


def test_loadClass():
    assert c["courses"] == ["1ma1dfb01"]


def test_coursePath():
    assert c["courses_path"] == "../example_files/"


def test_configPath():
    assert c["config_path"] == "../example_files/"
