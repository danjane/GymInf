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
    student_list = list(students.parse_course_list(filename).values())
    pairs = standard_pairs_layout(6, 4)
    number_empties = len(pairs) - len(student_list)
    if number_empties < 0:
        raise NotImplementedError("Cannot handle more than 24 students, legal limit in gva!!")
    padded_student_list = ["empty"]*number_empties + student_list[::-1]
    return dict(zip(padded_student_list, pairs))
