from linkComments import report_dnfs, get_latex_report_from_config_path


def test_report_dnf():
    output = report_dnfs("../example_files/config.yaml")
    print(output)
    assert isinstance(output, dict)
    assert output["albert.enstn"] == 1


def test_build_latex_report():
    output = get_latex_report_from_config_path("../example_files/config.yaml")
    expected = r"""\documentclass[11pt]{article}
\begin{document}
albert.enstn (Albert) \hfill 1ma1df01 \\
\begin{tabular}{ll}
Date & Info \\
13Jan2022 & DNF Albert, Marie \\"""
    assert isinstance(output, str)
    assert output[:len(expected)] == expected


def test_students_needing_comments():
    students = get_students_needing_comments_from_config_path("../example_files/config.yaml")
    assert students == ["Marie", "Dick", "Albert", "Gabs"]
