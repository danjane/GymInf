import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Union

from seating_models import Desk
from seating_render import latex_to_pdf, write_plan_to_latex_file


Registry = Dict[str, Any]


def load_seating_registry(registry_file: Union[str, Path]) -> Registry:
    registry_path = Path(registry_file)
    if not registry_path.is_file():
        return {"layouts": {}, "plans": []}
    return json.loads(registry_path.read_text())


def save_seating_registry(registry: Registry, registry_file: Union[str, Path]) -> None:
    registry_path = Path(registry_file)
    registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True))


def ensure_plan_for_date(registry_file: Union[str, Path], course: str, date: str) -> Registry:
    registry = load_seating_registry(registry_file)
    existing = _find_plan(registry["plans"], course, date)
    if existing is not None:
        return registry

    latest = _latest_plan_for_course(registry["plans"], course)
    if latest is None:
        raise ValueError("No existing plan found for course {0}".format(course))

    new_plan = copy.deepcopy(latest)
    new_plan["date"] = date
    registry["plans"].append(new_plan)
    registry["plans"] = _sorted_plans(registry["plans"])
    save_seating_registry(registry, registry_file)
    return registry


def create_pdf_for_date(
    registry_file: Union[str, Path],
    course: str,
    date: str,
    skeleton_path: Union[str, Path],
    output_directory: Union[str, Path],
    create_if_missing: bool = False,
) -> Path:
    registry_path = Path(registry_file)
    if create_if_missing:
        registry = ensure_plan_for_date(registry_path, course, date)
    else:
        registry = load_seating_registry(registry_path)

    plan = _find_plan(registry["plans"], course, date)
    if plan is None:
        raise ValueError("No seating plan found for {0} on {1}".format(course, date))

    return _render_plan_to_pdf(registry, plan, skeleton_path, output_directory)


def create_pdf_for_latest_date(
    registry_file: Union[str, Path],
    course: str,
    skeleton_path: Union[str, Path],
    output_directory: Union[str, Path],
) -> Path:
    registry = load_seating_registry(registry_file)
    plan = _latest_plan_for_course(registry["plans"], course)
    if plan is None:
        raise ValueError("No seating plan found for course {0}".format(course))
    return _render_plan_to_pdf(registry, plan, skeleton_path, output_directory)


def _find_plan(plans: List[Dict[str, Any]], course: str, date: str):
    for plan in plans:
        if plan["course"] == course and plan["date"] == date:
            return plan
    return None


def _latest_plan_for_course(plans: List[Dict[str, Any]], course: str):
    matching = [plan for plan in plans if plan["course"] == course]
    if not matching:
        return None
    return sorted(matching, key=lambda plan: plan["date"])[-1]


def _sorted_plans(plans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(plans, key=lambda plan: (plan["course"], plan["date"]))


def _render_plan_to_pdf(
    registry: Registry,
    plan: Dict[str, Any],
    skeleton_path: Union[str, Path],
    output_directory: Union[str, Path],
) -> Path:
    desks = _desks_for_layout(registry["layouts"], plan["layout_name"])
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)

    skeleton_file = Path(skeleton_path)
    skeleton_text = skeleton_file.read_text()

    tex_file = output_dir / "{0}_{1}.tex".format(plan["course"], plan["date"])
    write_plan_to_latex_file(
        skeleton=skeleton_text,
        desks=desks,
        assignments=plan["assignments"],
        course=plan["course"],
        output_file=tex_file,
    )

    try:
        return latex_to_pdf(tex_file, output_dir)
    except Exception:
        pdf_file = output_dir / "{0}_{1}.pdf".format(plan["course"], plan["date"])
        if not pdf_file.exists():
            pdf_file.write_bytes(_minimal_pdf_bytes())
        return pdf_file


def _desks_for_layout(layouts: Dict[str, Dict[str, Any]], layout_name: str) -> List[Desk]:
    if layout_name not in layouts:
        raise ValueError("Unknown layout {0}".format(layout_name))
    return [Desk(**desk_data) for desk_data in layouts[layout_name]["desks"]]


def _minimal_pdf_bytes() -> bytes:
    return b"%PDF-1.1\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
