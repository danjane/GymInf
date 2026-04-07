from linkComments import *
from pathlib import Path
from unittest.mock import patch

EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"


def test_report_dnf():
    output = report_dnfs(str(EXAMPLE_CONFIG))
    print(output)
    assert isinstance(output, dict)
    assert output["EINSTEIN Albert"] == 1


def test_build_latex_report():
    output = get_latex_report_from_config_path(str(EXAMPLE_CONFIG))
    assert isinstance(output, str)
    assert output.startswith(r"""\documentclass[11pt]{article}
\usepackage[margin=1.5cm]{geometry}
\usepackage{tikz}
\begin{document}
EINSTEIN Albert (Albert) \hfill 1ma1df01 \\""")
    assert "Comment progress" in output
    assert "Exam results" in output
    assert r"\begin{tabular}{ll}" in output


def test_students_needing_comments():
    students_needing_comments = get_students_needing_comments_from_config_path(
        str(EXAMPLE_CONFIG), "1ma1df01")
    assert students_needing_comments == ["Marie", "Dick", "Albert", "Gabs"]


def test_latex_to_pdf_returns_existing_pdf_after_runtime_error(tmp_path):
    tex_file = tmp_path / "report.tex"
    pdf_file = tmp_path / "report.pdf"
    tex_file.write_text("test")
    pdf_file.write_text("pdf")

    with patch("linkComments.compile_latex_to_pdf", side_effect=RuntimeError("boom")):
        assert latex_to_pdf(str(tex_file), str(tmp_path)) == str(pdf_file)


def test_latex_to_pdf_returns_tex_file_if_pdf_not_created(tmp_path, capsys):
    tex_file = tmp_path / "report.tex"
    tex_file.write_text("test")

    with patch("linkComments.compile_latex_to_pdf", side_effect=FileNotFoundError()):
        output = latex_to_pdf(str(tex_file), str(tmp_path))

    captured = capsys.readouterr()
    assert output == str(tex_file)
    assert "pdflatex command not found" in captured.out
    assert "pdf was NOT created from tex file!!" in captured.out


def test_create_report_falls_back_to_report_tex_in_config_root(tmp_path):
    cfg_file = tmp_path / "config.yaml"
    comments_file = tmp_path / "comments.txt"
    course_file = tmp_path / "1ma1df01.txt"
    outline_file = tmp_path / "report_outline_student.tex"
    skeleton_file = tmp_path / "report_skeleton.tex"

    cfg_file.write_text(
        "\n".join(
            [
                "courses:",
                "- 1ma1df01",
                "courses_path: .",
                "config_path: .",
                "comments_path: comments.txt",
                "report_student_path: report_outline_student.tex",
                "report_skeleton_path: report_skeleton.tex",
            ]
        )
    )
    comments_file.write_text("d13Jan2022\nc1ma1df01\n+ Albert\n")
    course_file.write_text("EINSTEIN Albert, Albert\n")
    outline_file.write_text("STUDENTCODE STUDENTNAME COURSE SENTIMENTGRAPH EXAMGRAPH STUDENTCOMMENTS")
    skeleton_file.write_text(r"\documentclass{article}\begin{document}STUDENTPAGES\end{document}")

    with patch("linkComments.latex_to_pdf", return_value="created.pdf") as mocked_latex_to_pdf:
        output = create_report(str(cfg_file))

    assert output == "created.pdf"
    report_file = tmp_path / "report.tex"
    assert report_file.is_file()
    mocked_latex_to_pdf.assert_called_once_with(str(report_file), str(tmp_path))
