from pathlib import Path

from seating_history import (
    create_pdf_for_date,
    create_pdf_for_latest_date,
    ensure_plan_for_date,
    load_seating_registry,
    save_generated_plan,
    save_seating_registry,
)


def sample_registry():
    return {
        "layouts": {
            "pairs_4x3": {
                "desks": [
                    {"desk_id": "R1D1", "x": 1.0, "y": 0.0, "facing": "front"},
                    {"desk_id": "R1D2", "x": 3.0, "y": 0.0, "facing": "front"},
                    {"desk_id": "R1D3", "x": 6.0, "y": 0.0, "facing": "front"},
                ]
            }
        },
        "plans": [
            {
                "course": "1ma1df01",
                "date": "2026-04-01",
                "layout_name": "pairs_4x3",
                "assignments": {"R1D1": "Albert", "R1D2": "Gabs", "R1D3": "Marie"},
                "mode": "alphabetic",
            },
            {
                "course": "1ma1df01",
                "date": "2026-04-08",
                "layout_name": "pairs_4x3",
                "assignments": {"R1D1": "Gabs", "R1D2": "Albert", "R1D3": "Marie"},
                "mode": "manual",
            },
        ],
    }


def test_save_and_load_seating_registry_round_trip(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"

    save_seating_registry(registry, registry_file)
    loaded = load_seating_registry(registry_file)

    assert loaded == registry


def test_ensure_plan_for_date_reuses_latest_existing_plan(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    save_seating_registry(registry, registry_file)

    updated = ensure_plan_for_date(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-15",
    )

    matching = [plan for plan in updated["plans"] if plan["course"] == "1ma1df01" and plan["date"] == "2026-04-15"]
    assert len(matching) == 1
    assert matching[0]["assignments"] == {"R1D1": "Gabs", "R1D2": "Albert", "R1D3": "Marie"}
    assert matching[0]["layout_name"] == "pairs_4x3"


def test_ensure_plan_for_date_updates_registry_file(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    save_seating_registry(registry, registry_file)

    ensure_plan_for_date(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-15",
    )

    reloaded = load_seating_registry(registry_file)
    dates = [plan["date"] for plan in reloaded["plans"] if plan["course"] == "1ma1df01"]
    assert "2026-04-15" in dates


def test_create_pdf_for_date_creates_pdf_for_requested_date(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    skeleton_file = tmp_path / "skeleton.tex"
    output_dir = tmp_path / "output"
    save_seating_registry(registry, registry_file)
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    pdf_file = create_pdf_for_date(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-08",
        skeleton_path=skeleton_file,
        output_directory=output_dir,
    )

    assert pdf_file.name == "1ma1df01_2026-04-08.pdf"


def test_create_pdf_for_date_flips_rows_for_pdf_output(tmp_path: Path, monkeypatch):
    registry = {
        "layouts": {
            "pairs_4x3": {
                "desks": [
                    {"desk_id": "R1D1", "x": 1.0, "y": 0.0, "facing": "front"},
                    {"desk_id": "R2D1", "x": 1.0, "y": 4.5, "facing": "front"},
                ]
            }
        },
        "plans": [
            {
                "course": "1ma1df01",
                "date": "2026-04-08",
                "layout_name": "pairs_4x3",
                "assignments": {"R1D1": "Front", "R2D1": "Back"},
                "mode": "manual",
            }
        ],
    }
    registry_file = tmp_path / "seatingplans.json"
    skeleton_file = tmp_path / "skeleton.tex"
    output_dir = tmp_path / "output"
    save_seating_registry(registry, registry_file)
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    def fake_latex_to_pdf(tex_file, output_directory):
        pdf_file = Path(output_directory) / (Path(tex_file).stem + ".pdf")
        pdf_file.write_bytes(b"%PDF-1.1\n%%EOF\n")
        return pdf_file

    monkeypatch.setattr("seating_history.latex_to_pdf", fake_latex_to_pdf)

    create_pdf_for_date(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-08",
        skeleton_path=skeleton_file,
        output_directory=output_dir,
    )

    tex_output = (output_dir / "1ma1df01_2026-04-08.tex").read_text()
    assert r"\node[desk] at (1.000000,4.500000) {Front};" in tex_output
    assert r"\node[desk] at (1.000000,0.000000) {Back};" in tex_output


def test_create_pdf_for_latest_date_uses_latest_plan(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    skeleton_file = tmp_path / "skeleton.tex"
    output_dir = tmp_path / "output"
    save_seating_registry(registry, registry_file)
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    pdf_file = create_pdf_for_latest_date(
        registry_file=registry_file,
        course="1ma1df01",
        skeleton_path=skeleton_file,
        output_directory=output_dir,
    )

    assert pdf_file.name == "1ma1df01_2026-04-08.pdf"


def test_create_pdf_for_date_can_create_missing_date_by_reusing_latest_plan(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    skeleton_file = tmp_path / "skeleton.tex"
    output_dir = tmp_path / "output"
    save_seating_registry(registry, registry_file)
    skeleton_file.write_text("CourseNameHere\nDesksHere")

    pdf_file = create_pdf_for_date(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-15",
        skeleton_path=skeleton_file,
        output_directory=output_dir,
        create_if_missing=True,
    )

    assert pdf_file.name == "1ma1df01_2026-04-15.pdf"

    reloaded = load_seating_registry(registry_file)
    matching = [plan for plan in reloaded["plans"] if plan["course"] == "1ma1df01" and plan["date"] == "2026-04-15"]
    assert len(matching) == 1


def test_save_generated_plan_writes_layout_and_plan_to_registry(tmp_path: Path):
    registry_file = tmp_path / "seatingplans.json"

    updated = save_generated_plan(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-22",
        layout_name="pairs_4x3",
        desks=[
            {"desk_id": "R1D1", "x": 1.0, "y": 0.0, "facing": "front"},
            {"desk_id": "R1D2", "x": 3.0, "y": 0.0, "facing": "front"},
        ],
        assignments={"R1D1": "Albert", "R1D2": "Gabs"},
        mode="alphabetic",
    )

    assert "pairs_4x3" in updated["layouts"]
    matching = [plan for plan in updated["plans"] if plan["course"] == "1ma1df01" and plan["date"] == "2026-04-22"]
    assert len(matching) == 1
    assert matching[0]["mode"] == "alphabetic"


def test_save_generated_plan_updates_existing_plan_for_same_course_and_date(tmp_path: Path):
    registry = sample_registry()
    registry_file = tmp_path / "seatingplans.json"
    save_seating_registry(registry, registry_file)

    updated = save_generated_plan(
        registry_file=registry_file,
        course="1ma1df01",
        date="2026-04-08",
        layout_name="pairs_4x3",
        desks=registry["layouts"]["pairs_4x3"]["desks"],
        assignments={"R1D1": "Marie", "R1D2": "Albert", "R1D3": "Gabs"},
        mode="alphabetic",
    )

    matching = [plan for plan in updated["plans"] if plan["course"] == "1ma1df01" and plan["date"] == "2026-04-08"]
    assert len(matching) == 1
    assert matching[0]["assignments"] == {"R1D1": "Marie", "R1D2": "Albert", "R1D3": "Gabs"}
