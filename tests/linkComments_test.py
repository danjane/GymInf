from linkComments import *


def test_reportDnfs():
    dnfs = report_dnfs("../example_files/config.yaml")
    assert type(dnfs) is dict

