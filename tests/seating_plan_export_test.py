from pathlib import Path

from seating_history import load_seating_registry
from seating_plan_export import create_seating_plan_pdf


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
