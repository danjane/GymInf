import config

c = config.load("../example_files/config.yaml")


def test_loadClass():
    assert c["courses"] == ["1ma1dfb01"]
