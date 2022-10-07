from linkComments import *


def test_reportDnfs():
    dnfs = report_dnfs(None)
    assert dnfs is dict

