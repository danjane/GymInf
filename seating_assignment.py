import random
from typing import Iterable, List, Optional

from seating_models import Desk


def arrange_students(students: Iterable[str], mode: str = "alphabetic", seed: Optional[int] = None) -> List[str]:
    ordered = list(students)
    if mode == "alphabetic":
        return sorted(ordered)
    if mode == "random":
        rng = random.Random(seed)
        rng.shuffle(ordered)
        return ordered
    raise ValueError("Unsupported arrangement mode: {0}".format(mode))


def assign_students_to_desks(desks: List[Desk], students: List[str]):
    if len(students) > len(desks):
        raise ValueError("Not enough desks for all students")

    assignments = {}
    padded_students = list(students) + [""] * (len(desks) - len(students))
    for desk, student in zip(desks, padded_students):
        assignments[desk.desk_id] = student
    return assignments
