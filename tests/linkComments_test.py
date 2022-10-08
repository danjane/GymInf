from linkComments import *


def test_reportDnfs():
    dnfs = report_dnfs("../example_files/config.yaml")
    output = dnfs
    print(output)
    assert type(output) is dict
    assert output["albert.enstn"] == 1


def test_buildLatexReport():
    report = latex_report("../example_files/config.yaml")
    output = report
    print(output)
    exp = r"""albert.enstn (Albert) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
13Jan2022 & DNF Albert, Marie \\"""
    assert type(output) is str
    assert output[:len(exp)] == exp
