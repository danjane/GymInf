from pathlib import Path

from seating_history import load_seating_registry
from seating_plan_export import create_alphabetic_seating_plans_for_all_courses, create_seating_plan_pdf


def test_create_seating_plan_pdf_updates_registry_when_registry_file_is_provided(tmp_path: Path, monkeypatch):
    skeleton_file = tmp_path / "skeleton.tex"
    registry_file = tmp_path / "seatingplans.json"
    output_dir = tmp_path / "output"
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    def fake_latex_to_pdf(tex_file, output_directory):
        pdf_file = Path(output_directory) / (Path(tex_file).stem + ".pdf")
        pdf_file.write_bytes(b"%PDF-1.1\n%%EOF\n")
        return pdf_file

    monkeypatch.setattr("seating_plan_export.latex_to_pdf", fake_latex_to_pdf)

    pdf_file = create_seating_plan_pdf(
        course="1ma1df01",
        student_names={
            "ZETA Alice": "Alice",
            "ALPHA Bob": "Bob",
        },
        skeleton_path=skeleton_file,
        output_directory=output_dir,
        registry_file=registry_file,
        date="2026-04-22",
    )

    registry = load_seating_registry(registry_file)
    matching = [plan for plan in registry["plans"] if plan["course"] == "1ma1df01" and plan["date"] == "2026-04-22"]

    assert pdf_file.name == "1ma1df01.pdf"
    assert len(matching) == 1
    assert matching[0]["assignments"]["R1D1"] == "Bob"
    assert matching[0]["assignments"]["R1D2"] == "Alice"


def test_create_seating_plan_pdf_uses_today_when_registry_enabled_without_date(tmp_path: Path, monkeypatch):
    skeleton_file = tmp_path / "skeleton.tex"
    registry_file = tmp_path / "seatingplans.json"
    output_dir = tmp_path / "output"
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    class FakeDate:
        @staticmethod
        def today():
            class FakeToday:
                @staticmethod
                def isoformat():
                    return "2026-04-30"

            return FakeToday()

    def fake_latex_to_pdf(tex_file, output_directory):
        pdf_file = Path(output_directory) / (Path(tex_file).stem + ".pdf")
        pdf_file.write_bytes(b"%PDF-1.1\n%%EOF\n")
        return pdf_file

    monkeypatch.setattr("seating_plan_export.datetime.date", FakeDate)
    monkeypatch.setattr("seating_plan_export.latex_to_pdf", fake_latex_to_pdf)

    create_seating_plan_pdf(
        course="1ma1df01",
        student_names={"ALPHA Bob": "Bob"},
        skeleton_path=skeleton_file,
        output_directory=output_dir,
        registry_file=registry_file,
    )

    registry = load_seating_registry(registry_file)
    matching = [plan for plan in registry["plans"] if plan["date"] == "2026-04-30"]
    assert len(matching) == 1


def test_create_alphabetic_seating_plans_for_all_courses_uses_config_paths(tmp_path: Path, monkeypatch):
    config_file = tmp_path / "config.yaml"
    courses_dir = tmp_path / "courses"
    output_dir = tmp_path / "output"
    courses_dir.mkdir()
    output_dir.mkdir()
    (courses_dir / "1ma1df01.txt").write_text("ZETA Alice\nALPHA Bob\n")
    (tmp_path / "seatingplan_skeleton.tex").write_text("CourseNameHere\nDesksHere")
    config_file.write_text(
        "\n".join(
            [
                "courses:",
                "- 1ma1df01",
                "courses_path: courses",
                "config_path: .",
                "comments_path: comments.txt",
                "exam_path: .",
                "report_student_path: report_outline_student.tex",
                "report_skeleton_path: report_skeleton.tex",
                "seatingplan_skeleton_path: seatingplan_skeleton.tex",
                "seatingplan_output_path: output",
                "seatingplans_registry_path: seatingplans.json",
            ]
        )
    )

    def fake_latex_to_pdf(tex_file, output_directory):
        pdf_file = Path(output_directory) / (Path(tex_file).stem + ".pdf")
        pdf_file.write_bytes(b"%PDF-1.1\n%%EOF\n")
        return pdf_file

    monkeypatch.setattr("seating_plan_export.latex_to_pdf", fake_latex_to_pdf)

    pdfs = create_alphabetic_seating_plans_for_all_courses(str(config_file), date="2026-04-30")

    assert [pdf.name for pdf in pdfs] == ["1ma1df01.pdf"]
    registry = load_seating_registry(tmp_path / "seatingplans.json")
    assert registry["plans"][0]["assignments"]["R1D1"] == "Bob"
