from typing import Dict, Iterable

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
