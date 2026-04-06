from typing import List

from seating_models import Desk


def create_pairs_layout(num_rows: int, pairs_per_row: int) -> List[Desk]:
    desks = []
    for row in range(num_rows):
        x = 1
        for pair_index in range(pairs_per_row):
            for seat_in_pair in range(2):
                desk_number = pair_index * 2 + seat_in_pair + 1
                desks.append(
                    Desk(
                        desk_id="R{0}D{1}".format(row + 1, desk_number),
                        x=float(x),
                        y=float(row * 1.5),
                        facing="front",
                        group="pair_{0}".format(pair_index + 1),
                        row=row + 1,
                        seat_index=desk_number,
                    )
                )
                x += 2
            x += 1
    return desks


def create_rows_layout(num_rows: int, desks_per_row: int) -> List[Desk]:
    desks = []
    for row in range(num_rows):
        for seat_index in range(desks_per_row):
            desks.append(
                Desk(
                    desk_id="R{0}D{1}".format(row + 1, seat_index + 1),
                    x=float(seat_index * 2),
                    y=float(row * 1.5),
                    facing="front",
                    row=row + 1,
                    seat_index=seat_index + 1,
                )
            )
    return desks


def create_mixed_rows_layout(front_rows: int, desks_per_front_row: int, back_row_desks: int) -> List[Desk]:
    desks = create_rows_layout(front_rows, desks_per_front_row)
    back_row_y = float(front_rows * 1.5)
    for seat_index in range(back_row_desks):
        desks.append(
            Desk(
                desk_id="R{0}D{1}".format(front_rows + 1, seat_index + 1),
                x=float(seat_index * 2),
                y=back_row_y,
                facing="back",
                row=front_rows + 1,
                seat_index=seat_index + 1,
            )
        )
    return desks


def create_u_shape_layout(left_side: int, bottom_side: int, right_side: int, facing: str) -> List[Desk]:
    desks = []
    for index in range(left_side):
        desks.append(
            Desk(
                desk_id="L{0}".format(index + 1),
                x=0.0,
                y=float(index * 1.5),
                facing=facing,
                group="left",
                seat_index=index + 1,
            )
        )
    for index in range(bottom_side):
        desks.append(
            Desk(
                desk_id="B{0}".format(index + 1),
                x=float(index * 2),
                y=float((left_side - 1) * 1.5 if left_side else 0.0),
                facing=facing,
                group="bottom",
                seat_index=index + 1,
            )
        )
    for index in range(right_side):
        desks.append(
            Desk(
                desk_id="R{0}".format(index + 1),
                x=float((bottom_side - 1) * 2 if bottom_side else 0.0),
                y=float(index * 1.5),
                facing=facing,
                group="right",
                seat_index=index + 1,
            )
        )
    return desks
