import linkComments


def test_loadCfg():
    assert linkComments.cfg["comments_path"] == "../example_files/comments.txt"
