from pathlib import Path
import datetime
from typing import Callable, Iterable, List, Optional

import config
import seating_history
import students
from seating_assignment import arrange_students, assign_students_to_desks
from seating_layouts import create_pairs_layout
from seating_models import Desk
from seating_render import latex_to_pdf, write_plan_to_latex_file


LayoutFactory = Callable[[], List[Desk]]
DEFAULT_LAYOUT_NAME = "pairs_4x3"


def load_skeleton_text(skeleton_path: Path) -> str:
    return skeleton_path.read_text()


def default_layout_factory() -> List[Desk]:
    return create_pairs_layout(num_rows=4, pairs_per_row=3)


def build_plan_assignments(
    student_names: Iterable[str],
    layout_factory: LayoutFactory,
    mode: str,
    seed: Optional[int],
):
    desks = layout_factory()
    ordered_students = arrange_students(student_names, mode=mode, seed=seed)
    assignments = assign_students_to_desks(desks, ordered_students)
    return desks, assignments


def create_seating_plan_pdf(
    course: str,
    student_names: Iterable[str],
    skeleton_path: Path,
    output_directory: Path,
    layout_factory: Optional[LayoutFactory] = None,
    mode: str = "alphabetic",
    seed: Optional[int] = None,
    registry_file: Optional[Path] = None,
    date: Optional[str] = None,
    layout_name: str = DEFAULT_LAYOUT_NAME,
) -> Path:
    if layout_factory is None:
        layout_factory = default_layout_factory

    desks, assignments = build_plan_assignments(student_names, layout_factory, mode, seed)
    skeleton = load_skeleton_text(skeleton_path)

    if registry_file is not None:
        if date is None:
            date = datetime.date.today().isoformat()
        seating_history.save_generated_plan(
            registry_file=registry_file,
            course=course,
            date=date,
            layout_name=layout_name,
            desks=desks,
            assignments=assignments,
            mode=mode,
        )

    output_directory.mkdir(parents=True, exist_ok=True)
    tex_file = output_directory / "{0}.tex".format(course)
    write_plan_to_latex_file(skeleton, desks, assignments, course, tex_file)
    return latex_to_pdf(tex_file, output_directory)


def resolve_export_paths(
    cfg: config.AppConfig,
    skeleton_path: Optional[str],
    output_directory: Optional[str],
    registry_file: Optional[str],
):
    if skeleton_path is None:
        skeleton_path = cfg.extras.get("seatingplan_skeleton_path")
    if output_directory is None:
        output_directory = cfg.extras.get("seatingplan_output_path")
    if registry_file is None:
        registry_file = cfg.extras.get("seatingplans_registry_path")

    if skeleton_path is None:
        raise ValueError("A seating plan skeleton path is required")
    if output_directory is None:
        raise ValueError("A seating plan output directory is required")

    return (
        Path(skeleton_path),
        Path(output_directory),
        Path(registry_file) if registry_file is not None else None,
    )


def create_alphabetic_seating_plans_for_all_courses(
    cfg_path: str,
    skeleton_path: Optional[str] = None,
    output_directory: Optional[str] = None,
    layout_factory: Optional[LayoutFactory] = None,
    registry_file: Optional[str] = None,
    date: Optional[str] = None,
    layout_name: str = DEFAULT_LAYOUT_NAME,
) -> List[Path]:
    cfg = config.load(cfg_path)
    skeleton_path, output_directory, registry_path = resolve_export_paths(
        cfg, skeleton_path, output_directory, registry_file
    )

    pdf_files = []
    for course in cfg.courses:
        class_path = cfg.class_list_path(course)
        student_names = students.parse_course_list(str(class_path))
        pdf_files.append(
            create_seating_plan_pdf(
                course=course,
                student_names=student_names,
                skeleton_path=skeleton_path,
                output_directory=output_directory,
                layout_factory=layout_factory,
                mode="alphabetic",
                registry_file=registry_path,
                date=date,
                layout_name=layout_name,
            )
        )
    return pdf_files
