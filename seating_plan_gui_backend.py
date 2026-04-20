from pathlib import Path

import config
import link_gui_backend
import seating_history

from link_gui_backend import save_seating_state


def load_plan(cfg_path: str, course: str):
    cfg = config.load(cfg_path)
    class_path = cfg.class_list_path(course)
    seating_state = link_gui_backend.load_or_create_seating_state(cfg, course, class_path)
    seating_state["gui_places"] = link_gui_backend._gui_places_for_desks(
        seating_state["layout_name"], seating_state["desks"]
    )
    return seating_state


def save_plan(cfg_path: str, course: str, seating_state: dict, desks) -> None:
    save_seating_state(cfg_path, course, seating_state, desks)


def dump_plan_pdf(cfg_path: str, course: str, seating_state: dict):
    cfg = config.load(cfg_path)
    skeleton_path = Path(
        cfg.extras.get("seatingplan_skeleton_path", cfg.config_root / "seatingplan_skeleton.tex")
    )
    output_directory = Path(
        cfg.extras.get("seatingplan_output_path", cfg.config_root / "seatingplans")
    )
    return seating_history.create_pdf_for_date(
        seating_state["registry_file"],
        course,
        seating_state["date"],
        skeleton_path,
        output_directory,
    )
