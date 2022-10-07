from linkComments import *


def test_loadCfg():
    cfg = setup(None)
    assert cfg["comments_path"] == "../example_files/comments.txt"
