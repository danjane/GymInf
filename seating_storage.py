import json
from pathlib import Path
from typing import Union

from seating_models import SeatingPlan


def save_plan(plan: SeatingPlan, output_file: Union[str, Path]) -> None:
    output_path = Path(output_file)
    payload = {
        "course": plan.course,
        "date": plan.date,
        "layout_name": plan.layout_name,
        "assignments": plan.assignments,
        "desk_facings": plan.desk_facings,
    }
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))


def load_plan(input_file: Union[str, Path]) -> SeatingPlan:
    input_path = Path(input_file)
    payload = json.loads(input_path.read_text())
    return SeatingPlan(
        course=payload["course"],
        date=payload["date"],
        layout_name=payload["layout_name"],
        assignments=payload["assignments"],
        desk_facings=payload.get("desk_facings", {}),
    )
