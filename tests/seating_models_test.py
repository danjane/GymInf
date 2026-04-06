from seating_models import Desk, Layout, SeatingAssignment, SeatingPlan


def test_desk_stores_coordinates_and_orientation():
    desk = Desk(desk_id="A1", x=1.0, y=2.5, facing="front")

    assert desk.desk_id == "A1"
    assert desk.x == 1.0
    assert desk.y == 2.5
    assert desk.facing == "front"


def test_desk_defaults_to_front_facing():
    desk = Desk(desk_id="A2", x=0.0, y=0.0)

    assert desk.facing == "front"


def test_layout_contains_ordered_desks():
    desks = [Desk(desk_id="A1", x=0.0, y=0.0), Desk(desk_id="A2", x=2.0, y=0.0)]
    layout = Layout(name="pairs", desks=desks)

    assert layout.name == "pairs"
    assert layout.desks == desks


def test_seating_assignment_links_student_to_desk():
    assignment = SeatingAssignment(desk_id="A1", student="Alice")

    assert assignment.desk_id == "A1"
    assert assignment.student == "Alice"


def test_seating_plan_keeps_course_and_date():
    plan = SeatingPlan(course="1MA1", date="2026-04-06", layout_name="pairs", assignments={"A1": "Alice"})

    assert plan.course == "1MA1"
    assert plan.date == "2026-04-06"
    assert plan.layout_name == "pairs"
    assert plan.assignments == {"A1": "Alice"}
