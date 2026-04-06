from pathlib import Path

from seating_models import SeatingPlan
from seating_storage import load_plan, save_plan


def test_save_plan_writes_json(tmp_path: Path):
    plan = SeatingPlan(course="1MA1", date="2026-04-06", layout_name="pairs", assignments={"A1": "Alice"})
    output_file = tmp_path / "plan.json"

    save_plan(plan, output_file)

    assert output_file.is_file()


def test_load_plan_restores_assignments(tmp_path: Path):
    plan = SeatingPlan(course="1MA1", date="2026-04-06", layout_name="pairs", assignments={"A1": "Alice"})
    output_file = tmp_path / "plan.json"
    save_plan(plan, output_file)

    loaded = load_plan(output_file)

    assert loaded.assignments == {"A1": "Alice"}


def test_saved_plan_preserves_layout_name(tmp_path: Path):
    plan = SeatingPlan(course="1MA1", date="2026-04-06", layout_name="u_shape", assignments={"A1": "Alice"})
    output_file = tmp_path / "plan.json"
    save_plan(plan, output_file)

    loaded = load_plan(output_file)

    assert loaded.layout_name == "u_shape"


def test_saved_plan_preserves_desk_orientation(tmp_path: Path):
    plan = SeatingPlan(
        course="1MA1",
        date="2026-04-06",
        layout_name="rows_back",
        assignments={"A1": "Alice"},
        desk_facings={"A1": "back"},
    )
    output_file = tmp_path / "plan.json"
    save_plan(plan, output_file)

    loaded = load_plan(output_file)

    assert loaded.desk_facings == {"A1": "back"}
