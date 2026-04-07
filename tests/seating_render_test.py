from seating_models import Desk
from seating_render import _cleanup_latex_auxiliary_files, latex_to_pdf, render_plan_to_latex
from pathlib import Path
import pytest


def test_render_plan_inserts_course_name():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": "Alice"}
    skeleton = "CourseNameHere\nDesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "1MA1" in output


def test_render_plan_inserts_all_desk_nodes():
    desks = [Desk("A1", 1.0, 0.0), Desk("A2", 3.0, 0.0)]
    assignments = {"A1": "Alice", "A2": "Bob"}
    skeleton = "DesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "Alice" in output
    assert "Bob" in output


def test_render_plan_renders_empty_desks_as_blank():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": ""}
    skeleton = "DesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "{}" in output


def test_render_plan_uses_given_skeleton():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": "Alice"}
    skeleton = "before\nDesksHere\nafter"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert output.startswith("before")
    assert output.endswith("after")


def test_cleanup_latex_auxiliary_files_removes_aux_and_log(tmp_path: Path):
    aux_file = tmp_path / "plan.aux"
    log_file = tmp_path / "plan.log"
    aux_file.write_text("aux")
    log_file.write_text("log")

    _cleanup_latex_auxiliary_files(tmp_path, "plan")

    assert not aux_file.exists()
    assert not log_file.exists()


def test_latex_to_pdf_raises_when_pdflatex_fails(monkeypatch, tmp_path: Path):
    tex_file = tmp_path / "plan.tex"
    tex_file.write_text("test")

    class FakeProcess:
        returncode = 1

        def communicate(self):
            return (b"", b"boom")

    monkeypatch.setattr("seating_render.subprocess.Popen", lambda *args, **kwargs: FakeProcess())

    try:
        latex_to_pdf(tex_file, tmp_path)
    except RuntimeError as exc:
        assert "boom" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError when pdflatex fails")


def test_latex_to_pdf_raises_when_pdf_not_created(monkeypatch, tmp_path: Path):
    tex_file = tmp_path / "plan.tex"
    tex_file.write_text("test")

    class FakeProcess:
        returncode = 0

        def communicate(self):
            return (b"", b"")

    monkeypatch.setattr("seating_render.subprocess.Popen", lambda *args, **kwargs: FakeProcess())

    with pytest.raises(FileNotFoundError):
        latex_to_pdf(tex_file, tmp_path)
