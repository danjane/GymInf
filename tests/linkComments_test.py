from linkComments import *
from pathlib import Path

EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"


def test_report_dnf():
    output = report_dnfs(str(EXAMPLE_CONFIG))
    print(output)
    assert isinstance(output, dict)
    assert output["EINSTEIN Albert"] == 1


def test_build_latex_report():
    output = get_latex_report_from_config_path(str(EXAMPLE_CONFIG))
    expected = r"""\documentclass[11pt]{article}
\begin{document}
EINSTEIN Albert (Albert) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
13Jan2022 & DNF Albert, Marie \\"""
    assert isinstance(output, str)
    assert output[:len(expected)] == expected


def test_students_needing_comments():
    students_needing_comments = get_students_needing_comments_from_config_path(
        str(EXAMPLE_CONFIG), "1ma1df01")
    assert students_needing_comments == ["Marie", "Dick", "Albert", "Gabs"]
