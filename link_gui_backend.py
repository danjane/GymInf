import os
import subprocess
import platform
import logging
import config
import students
import linkComments
import analyseNotes
import desk_functions
import seating_history
import seating_plan_export
from seating_layouts import create_pairs_layout
from seating_models import Desk
from datetime import datetime
from pathlib import Path


def start_new_day(cfg: config.AppConfig, course: str):
    file_path = cfg.comments.comments_file
    today = datetime.today().strftime('%d%b%Y').lower()
    with open(file_path, 'a') as f:
        f.write(f"\nd{today}\nc{course}\n")


def setup(cfg_path: str, course: str):
    cfg = config.load(cfg_path)
    config.ensure_support_files(cfg)
    start_new_day(cfg, course)
    comments_path = cfg.comments.comments_file
    positive_defaults = cfg.comments.positive_examples
    negative_defaults = cfg.comments.negative_examples

    file_path = cfg.class_list_path(course)
    seating_state = load_or_create_seating_state(cfg, course, file_path)
    logging.info(
        "link_gui_backend.setup course=%s class_path=%s registry_file=%s plan_date=%s layout=%s assignment_count=%s",
        course,
        file_path,
        seating_state["registry_file"],
        seating_state["date"],
        seating_state["layout_name"],
        len(seating_state["assignments"]),
    )
    seating_state["gui_places"] = _gui_places_for_desks(
        seating_state["layout_name"], seating_state["desks"]
    )
    desk_layout = _desk_layout_bounds(seating_state["gui_places"].values())
    return seating_state, desk_layout, comments_path, positive_defaults, negative_defaults


def desks_from_seating_state(seating_state: dict, width_height_desks):
    import icons

    desk_layout = _desk_layout_bounds(seating_state["gui_places"].values())
    desks = []
    for desk_data in seating_state["desks"]:
        student = seating_state["assignments"].get(desk_data.desk_id, "empty")
        gui_place = seating_state["gui_places"][desk_data.desk_id]
        desks.append(
            icons.Desk.create_desk(
                gui_place,
                student,
                desk_layout,
                width_height_desks,
                desk_id=desk_data.desk_id,
            )
        )
    return desks, desk_layout


def save_seating_state(cfg_path: str, course: str, seating_state: dict, desks) -> None:
    assignments = {}
    for desk in desks:
        if not getattr(desk, "desk_id", None):
            continue
        if desk.name:
            assignments[desk.desk_id] = desk.name

    logging.info(
        "save_seating_state course=%s registry_file=%s date=%s layout=%s assignment_count=%s",
        course,
        seating_state["registry_file"],
        seating_state["date"],
        seating_state["layout_name"],
        len(assignments),
    )
    seating_history.save_generated_plan(
        registry_file=seating_state["registry_file"],
        course=course,
        date=seating_state["date"],
        layout_name=seating_state["layout_name"],
        desks=seating_state["desks"],
        assignments=assignments,
        mode=seating_state["mode"],
    )


def open_file(filepath):
    # https://stackoverflow.com/questions/434597
    if platform.system() == 'Darwin':  # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':  # Windows
        os.startfile(filepath)
    else:  # linux variants
        subprocess.call(('xdg-open', filepath))


def courses(cfg_path: str):
    cfg = config.load(cfg_path)
    return cfg.courses


def load_students(cfg_path, course):
    cfg = config.load(cfg_path)
    class_path = cfg.class_list_path(course)
    student_dict = students.parse_course_list(str(class_path))
    students_codes_and_given_names = [code + ", " + name for code, name in student_dict.items()]
    return students_codes_and_given_names, class_path


def add_courses_in_files(config_file, course, old_courses):
    new_courses = old_courses + [course]
    config.update_courses_in_yaml(config_file, new_courses)
    cfg = config.load(config_file)
    course_file = cfg.class_list_path(course)
    if not os.path.isfile(course_file):
        with open(course_file, 'w') as f:
            f.write("StudentID, StudentName")
    return new_courses


def delete_course_in_files(config_file, deleted_course):
    old_courses = courses(config_file)
    config.update_courses_in_yaml(config_file, [c for c in old_courses if c != deleted_course])


def build_reports(config_file):
    report_file = linkComments.create_report(config_file)
    open_file(report_file)


def calculate_averages(config_file):
    moyennes_file = analyseNotes.dump_all(config_file, None)
    open_file(moyennes_file)


def load_or_create_seating_state(cfg: config.AppConfig, course: str, class_path: Path) -> dict:
    registry_file = _registry_path(cfg)
    date = datetime.today().date().isoformat()
    logging.info(
        "load_or_create_seating_state course=%s registry_file=%s date=%s",
        course,
        registry_file,
        date,
    )
    registry = seating_history.load_seating_registry(registry_file)
    plan = _find_plan(registry["plans"], course, date)

    if plan is None:
        latest_plan = _latest_plan(registry["plans"], course)
        if latest_plan is None:
            logging.info(
                "load_or_create_seating_state creating initial plan course=%s date=%s",
                course,
                date,
            )
            registry = _create_initial_plan(registry_file, course, class_path, date)
        else:
            logging.info(
                "load_or_create_seating_state cloning latest plan course=%s latest_date=%s target_date=%s",
                course,
                latest_plan["date"],
                date,
            )
            registry = seating_history.ensure_plan_for_date(registry_file, course, date)
        plan = _find_plan(registry["plans"], course, date)
    else:
        logging.info(
            "load_or_create_seating_state found existing plan course=%s date=%s layout=%s",
            course,
            date,
            plan["layout_name"],
        )

    desks = _desks_for_layout(registry, plan["layout_name"])
    return {
        "registry_file": registry_file,
        "date": date,
        "layout_name": plan["layout_name"],
        "mode": plan.get("mode", "manual"),
        "desks": desks,
        "assignments": dict(plan["assignments"]),
    }


def _create_initial_plan(registry_file: Path, course: str, class_path: Path, date: str):
    desks = create_pairs_layout(num_rows=4, pairs_per_row=3)
    seating_plan = desk_functions.load_basic_seating_plan_from_file(str(class_path))
    ordered_places = desk_functions.standard_pairs_layout(6, 4)
    ordered_students = [seating_plan[place] for place in ordered_places]
    assignments = {
        desk.desk_id: student
        for desk, student in zip(desks, ordered_students)
        if student and student != "empty"
    }
    logging.info(
        "_create_initial_plan course=%s registry_file=%s date=%s assignment_count=%s",
        course,
        registry_file,
        date,
        len(assignments),
    )
    return seating_history.save_generated_plan(
        registry_file=registry_file,
        course=course,
        date=date,
        layout_name="pairs_4x3",
        desks=desks,
        assignments=assignments,
        mode="manual",
    )


def _registry_path(cfg: config.AppConfig) -> Path:
    configured_path = cfg.extras.get("seatingplans_registry_path")
    if configured_path:
        resolved_path = Path(configured_path)
        logging.info("link_gui_backend using configured seating registry %s", resolved_path)
        return resolved_path
    resolved_path = cfg.config_root / "seatingplans.json"
    logging.info("link_gui_backend using default seating registry %s", resolved_path)
    return resolved_path


def _find_plan(plans, course: str, date: str):
    for plan in plans:
        if plan["course"] == course and plan["date"] == date:
            return plan
    return None


def _latest_plan(plans, course: str):
    matching_plans = [plan for plan in plans if plan["course"] == course]
    if not matching_plans:
        return None
    return sorted(matching_plans, key=lambda plan: plan["date"])[-1]


def _desks_for_layout(registry, layout_name: str):
    return [Desk(**desk_data) for desk_data in registry["layouts"][layout_name]["desks"]]


def _desk_layout_bounds(desks) -> tuple[int, int]:
    max_x = max(position[0] for position in desks)
    max_y = max(position[1] for position in desks)
    return int(max_x) + 1, int(max_y) + 1


def _gui_places_for_desks(layout_name: str, desks) -> dict[str, tuple[float, float]]:
    if layout_name == "pairs_4x3":
        ordered_desks = sorted(desks, key=lambda desk: (desk.row or 0, desk.seat_index or 0, desk.desk_id))
        positions = desk_functions.standard_pairs_layout(6, 4)
        return {
            desk.desk_id: position
            for desk, position in zip(ordered_desks, positions)
        }
    return {desk.desk_id: (desk.x, desk.y) for desk in desks}


def seating_plan_export_paths(cfg: config.AppConfig):
    return seating_plan_export.resolve_export_paths(
        cfg,
        cfg.extras.get("seatingplan_skeleton_path"),
        cfg.extras.get("seatingplan_output_path"),
        cfg.extras.get("seatingplans_registry_path"),
    )[:2]
