from pathlib import Path
import subprocess
from typing import Dict, Iterable, Union

from seating_models import Desk


def latex_desk(name: str, xpos: float, ypos: float) -> str:
    return "\\node[desk] at ({0:f},{1:f}) {{{2}}};\n".format(xpos, ypos, name)


def render_plan_to_latex(skeleton: str, desks: Iterable[Desk], assignments: Dict[str, str], course: str) -> str:
    plan = []
    for desk in desks:
        name = assignments.get(desk.desk_id, "")
        plan.append(latex_desk(name, desk.x, desk.y))

    output = skeleton.replace("DesksHere", "".join(plan))
    output = output.replace("CourseNameHere", course)
    return output


def write_plan_to_latex_file(
    skeleton: str,
    desks: Iterable[Desk],
    assignments: Dict[str, str],
    course: str,
    output_file: Union[str, Path],
) -> Path:
    output_path = Path(output_file)
    latex_text = render_plan_to_latex(skeleton, desks, assignments, course)
    output_path.write_text(latex_text)
    return output_path


def latex_to_pdf(tex_file: Union[str, Path], output_directory: Union[str, Path]) -> Path:
    tex_path = Path(tex_file)
    output_dir = Path(output_directory)
    process = subprocess.Popen(
        ["pdflatex", "-output-directory", str(output_dir), str(tex_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    _, stderr = process.communicate()

    if process.returncode != 0:
        raise RuntimeError(stderr.decode() or "pdflatex failed")

    pdf_file = output_dir / (tex_path.stem + ".pdf")
    if not pdf_file.is_file():
        raise FileNotFoundError("pdflatex did not create {0}".format(pdf_file))
    return pdf_file
