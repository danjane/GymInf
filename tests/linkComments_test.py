from linkComments import *


def test_reportDnfs():
    dnfs = report_dnfs("../example_files/config.yaml")
    output = dnfs
    print(output)
    assert type(output) is dict


def test_buildLatexReport():
    report = latex_report("../example_files/config.yaml")
    output = report
    print(output)
    assert type(output) is str
