from linkComments import *


def test_reportDnfs():
    output = report_dnfs("../example_files/config.yaml")
    print(output)
    assert type(output) is dict
    assert output["albert.enstn"] == 1


def test_buildLatexReport():
    output = latex_report_from_config_path("../example_files/config.yaml")
    exp = r"""\documentclass[11pt]{article}
\begin{document}
albert.enstn (Albert) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
13Jan2022 & DNF Albert, Marie \\"""
    assert type(output) is str
    assert output[:len(exp)] == exp
