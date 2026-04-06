import random
from typing import Iterable, List, Mapping, Optional, Union

from seating_models import Desk


StudentOrderingInput = Union[Iterable[str], Mapping[str, str]]


def arrange_students(students: StudentOrderingInput, mode: str = "alphabetic", seed: Optional[int] = None) -> List[str]:
    if isinstance(students, Mapping):
        return _arrange_student_mapping(students, mode=mode, seed=seed)

    ordered = list(students)
    if mode == "alphabetic":
        return sorted(ordered)
    if mode == "random":
        rng = random.Random(seed)
        rng.shuffle(ordered)
        return ordered
    raise ValueError("Unsupported arrangement mode: {0}".format(mode))


def _arrange_student_mapping(students: Mapping[str, str], mode: str, seed: Optional[int]) -> List[str]:
    items = list(students.items())
    if mode == "alphabetic":
        return [display_name for _, display_name in sorted(items, key=lambda item: item[0])]
    if mode == "random":
        rng = random.Random(seed)
        rng.shuffle(items)
        return [display_name for _, display_name in items]
    raise ValueError("Unsupported arrangement mode: {0}".format(mode))


def assign_students_to_desks(desks: List[Desk], students: List[str]):
    if len(students) > len(desks):
        raise ValueError("Not enough desks for all students")

    assignments = {}
    padded_students = list(students) + [""] * (len(desks) - len(students))
    for desk, student in zip(desks, padded_students):
        assignments[desk.desk_id] = student
    return assignments
