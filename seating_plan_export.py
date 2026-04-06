from pathlib import Path
from typing import Callable, Iterable, List, Optional

import config
import students
from seating_assignment import arrange_students, assign_students_to_desks
from seating_layouts import create_pairs_layout
from seating_models import Desk
from seating_render import latex_to_pdf, write_plan_to_latex_file


LayoutFactory = Callable[[], List[Desk]]


def load_skeleton_text(skeleton_path: Path) -> str:
    return skeleton_path.read_text()


def create_seating_plan_pdf(
    course: str,
    student_names: Iterable[str],
    skeleton_path: Path,
    output_directory: Path,
    layout_factory: Optional[LayoutFactory] = None,
    mode: str = "alphabetic",
    seed: Optional[int] = None,
) -> Path:
    if layout_factory is None:
        layout_factory = lambda: create_pairs_layout(num_rows=4, pairs_per_row=3)

    desks = layout_factory()
    ordered_students = arrange_students(student_names, mode=mode, seed=seed)
    assignments = assign_students_to_desks(desks, ordered_students)
    skeleton = load_skeleton_text(skeleton_path)

    output_directory.mkdir(parents=True, exist_ok=True)
    tex_file = output_directory / "{0}.tex".format(course)
    write_plan_to_latex_file(skeleton, desks, assignments, course, tex_file)
    return latex_to_pdf(tex_file, output_directory)


def create_alphabetic_seating_plans_for_all_courses(
    cfg_path: str,
    skeleton_path: Optional[str] = None,
    output_directory: Optional[str] = None,
    layout_factory: Optional[LayoutFactory] = None,
) -> List[Path]:
    cfg = config.load(cfg_path)

    if skeleton_path is None:
        skeleton_path = cfg.extras.get("seatingplan_skeleton_path")
    if output_directory is None:
        output_directory = cfg.extras.get("seatingplan_output_path")

    if skeleton_path is None:
        raise ValueError("A seating plan skeleton path is required")
    if output_directory is None:
        raise ValueError("A seating plan output directory is required")

    skeleton_path = Path(skeleton_path)
    output_directory = Path(output_directory)

    pdf_files = []
    for course in cfg.courses:
        class_path = cfg.class_list_path(course)
        student_names = list(students.parse_course_list(str(class_path)).values())
        pdf_files.append(
            create_seating_plan_pdf(
                course=course,
                student_names=student_names,
                skeleton_path=skeleton_path,
                output_directory=output_directory,
                layout_factory=layout_factory,
                mode="alphabetic",
            )
        )
    return pdf_files
