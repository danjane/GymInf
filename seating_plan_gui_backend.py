from pathlib import Path

import config
import link_gui_backend
import seating_history
import students
from seating_assignment import arrange_students, assign_students_to_desks

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
    try:
        skeleton_path, output_directory = link_gui_backend.seating_plan_export_paths(cfg)
    except ValueError:
        skeleton_path = Path(cfg.config_root / "seatingplan_skeleton.tex")
        output_directory = Path(cfg.config_root / "seatingplans")
    return seating_history.create_pdf_for_date(
        seating_state["registry_file"],
        course,
        seating_state["date"],
        skeleton_path,
        output_directory,
    )


def randomize_plan(cfg_path: str, course: str, seating_state: dict, seed=None):
    return arrange_plan(cfg_path, course, seating_state, mode="random", seed=seed)


def alphabetic_plan(cfg_path: str, course: str, seating_state: dict):
    return arrange_plan(cfg_path, course, seating_state, mode="alphabetic")


def arrange_plan(cfg_path: str, course: str, seating_state: dict, mode: str, seed=None):
    if mode == "random":
        student_names = _assigned_student_names(seating_state)
        ordered_students = arrange_students(student_names, mode=mode, seed=seed)
    else:
        cfg = config.load(cfg_path)
        class_path = cfg.class_list_path(course)
        course_students = students.parse_course_list(str(class_path))
        ordered_students = arrange_students(course_students, mode=mode, seed=seed)
    ordered_desks = _ordered_desks_for_gui(seating_state)
    return assign_students_to_desks(ordered_desks, ordered_students)


def _assigned_student_names(seating_state: dict):
    return [name for name in seating_state["assignments"].values() if name]


def _ordered_desks_for_gui(seating_state: dict):
    gui_places = seating_state.get("gui_places")
    if gui_places is None:
        return list(seating_state["desks"])
    desks_by_id = {desk.desk_id: desk for desk in seating_state["desks"]}
    ordered_desk_ids = sorted(
        gui_places,
        key=lambda desk_id: (-gui_places[desk_id][1], gui_places[desk_id][0], desk_id),
    )
    return [desks_by_id[desk_id] for desk_id in ordered_desk_ids]
