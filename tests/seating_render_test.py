from seating_models import Desk
from seating_render import render_plan_to_latex


def test_render_plan_inserts_course_name():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": "Alice"}
    skeleton = "CourseNameHere\nDesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "1MA1" in output


def test_render_plan_inserts_all_desk_nodes():
    desks = [Desk("A1", 1.0, 0.0), Desk("A2", 3.0, 0.0)]
    assignments = {"A1": "Alice", "A2": "Bob"}
    skeleton = "DesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "Alice" in output
    assert "Bob" in output


def test_render_plan_renders_empty_desks_as_blank():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": ""}
    skeleton = "DesksHere"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert "{}" in output


def test_render_plan_uses_given_skeleton():
    desks = [Desk("A1", 1.0, 0.0)]
    assignments = {"A1": "Alice"}
    skeleton = "before\nDesksHere\nafter"

    output = render_plan_to_latex(skeleton, desks, assignments, "1MA1")

    assert output.startswith("before")
    assert output.endswith("after")
