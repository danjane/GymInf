from seating_assignment import assign_students_to_desks, arrange_students
from seating_models import Desk


def test_alphabetic_assignment_orders_students_by_name():
    ordered = arrange_students(["Chloe", "Alice", "Bob"], mode="alphabetic")

    assert ordered == ["Alice", "Bob", "Chloe"]


def test_random_assignment_is_reproducible_with_seed():
    students = ["Alice", "Bob", "Chloe", "David"]

    ordered_one = arrange_students(students, mode="random", seed=42)
    ordered_two = arrange_students(students, mode="random", seed=42)

    assert ordered_one == ordered_two


def test_assignment_leaves_extra_desks_empty():
    desks = [Desk("A1", 0, 0), Desk("A2", 1, 0), Desk("A3", 2, 0)]
    assignments = assign_students_to_desks(desks, ["Alice", "Bob"])

    assert assignments["A1"] == "Alice"
    assert assignments["A2"] == "Bob"
    assert assignments["A3"] == ""


def test_assignment_raises_when_not_enough_desks():
    desks = [Desk("A1", 0, 0)]

    try:
        assign_students_to_desks(desks, ["Alice", "Bob"])
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError when there are more students than desks")
