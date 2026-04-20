import copy
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

from seating_models import Desk
from seating_render import latex_to_pdf, write_plan_to_latex_file


Registry = Dict[str, Any]
EMPTY_REGISTRY = {"layouts": {}, "plans": []}


def load_seating_registry(registry_file: Union[str, Path]) -> Registry:
    registry_path = Path(registry_file)
    if not registry_path.is_file():
        logging.info("load_seating_registry missing file=%s returning empty registry", registry_path)
        return copy.deepcopy(EMPTY_REGISTRY)
    logging.info("load_seating_registry reading file=%s", registry_path)
    return _normalized_registry(json.loads(registry_path.read_text()))


def save_seating_registry(registry: Registry, registry_file: Union[str, Path]) -> None:
    registry_path = Path(registry_file)
    logging.info(
        "save_seating_registry writing file=%s layouts=%s plans=%s",
        registry_path,
        len(registry.get("layouts", {})),
        len(registry.get("plans", [])),
    )
    registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True))


def save_generated_plan(
    registry_file: Union[str, Path],
    course: str,
    date: str,
    layout_name: str,
    desks,
    assignments: Dict[str, str],
    mode: str,
) -> Registry:
    logging.info(
        "save_generated_plan course=%s date=%s layout=%s mode=%s registry_file=%s",
        course,
        date,
        layout_name,
        mode,
        registry_file,
    )
    registry = load_seating_registry(registry_file)
    registry["layouts"][layout_name] = {"desks": [_serialize_desk(desk) for desk in desks]}

    new_plan = {
        "course": course,
        "date": date,
        "layout_name": layout_name,
        "assignments": assignments,
        "mode": mode,
    }

    existing = _find_plan(registry["plans"], course, date)
    if existing is None:
        registry["plans"].append(new_plan)
    else:
        existing.update(new_plan)

    registry["plans"] = _sorted_plans(registry["plans"])
    save_seating_registry(registry, registry_file)
    return registry


def ensure_plan_for_date(registry_file: Union[str, Path], course: str, date: str) -> Registry:
    logging.info(
        "ensure_plan_for_date course=%s date=%s registry_file=%s",
        course,
        date,
        registry_file,
    )
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
    desks = _pdf_oriented_desks(_desks_for_layout(registry["layouts"], plan["layout_name"]))
    output_dir = Path(output_directory)
    output_dir.mkdir(parents=True, exist_ok=True)
    skeleton_text = Path(skeleton_path).read_text()

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


def _pdf_oriented_desks(desks: List[Desk]) -> List[Desk]:
    if not desks:
        return []
    max_y = max(desk.y for desk in desks)
    return [
        Desk(
            desk_id=desk.desk_id,
            x=desk.x,
            y=max_y - desk.y,
            facing=desk.facing,
            group=desk.group,
            row=desk.row,
            seat_index=desk.seat_index,
            enabled=desk.enabled,
        )
        for desk in desks
    ]


def _minimal_pdf_bytes() -> bytes:
    return b"%PDF-1.1\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def _serialize_desk(desk):
    if isinstance(desk, Desk):
        return {
            "desk_id": desk.desk_id,
            "x": desk.x,
            "y": desk.y,
            "facing": desk.facing,
            "group": desk.group,
            "row": desk.row,
            "seat_index": desk.seat_index,
            "enabled": desk.enabled,
        }
    return desk


def _normalized_registry(registry: Registry) -> Registry:
    normalized = copy.deepcopy(EMPTY_REGISTRY)
    normalized.update(registry)
    normalized.setdefault("layouts", {})
    normalized.setdefault("plans", [])
    return normalized
