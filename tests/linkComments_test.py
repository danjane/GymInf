from linkComments import *


def test_reportDnfs():
    dnfs = report_dnfs("../example_files/config.yaml")
    assert type(dnfs) is dict


def test_buildLatexReport():
    report = latex_report("../example_files/config.yaml")
    assert type(report) is str
