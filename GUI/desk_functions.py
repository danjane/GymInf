import students
from typing import Dict, Tuple


def standard_pairs_layout(columns, rows):
    num_possible_columns = 3 * columns // 2 - 1
    num_possible_rows = 2 * rows - 1
    pairs = [(x, y)
             for y in range(num_possible_rows)
             for x in range(num_possible_columns)
             if x % 3 < 2 if y % 2 == 0]
    return pairs


def load_basic_seating_plan_from_file(filename: str) -> Dict[str, Tuple]:
    student_list = students.parse_course_list(filename)
    pairs = standard_pairs_layout(6, 4)
    return dict(zip(student_list.values(), pairs))
