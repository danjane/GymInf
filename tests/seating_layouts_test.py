from seating_layouts import (
    create_mixed_rows_layout,
    create_pairs_layout,
    create_rows_layout,
    create_u_shape_layout,
)


def test_pairs_layout_creates_expected_number_of_desks():
    desks = create_pairs_layout(num_rows=4, pairs_per_row=3)

    assert len(desks) == 24


def test_pairs_layout_inserts_spacing_between_pairs():
    desks = create_pairs_layout(num_rows=1, pairs_per_row=3)

    x_positions = [desk.x for desk in desks[:6]]
    assert x_positions == [1, 3, 6, 8, 11, 13]


def test_rows_layout_marks_all_desks_front_facing():
    desks = create_rows_layout(num_rows=8, desks_per_row=3)

    assert all(desk.facing == "front" for desk in desks)


def test_mixed_rows_layout_marks_last_row_back_facing():
    desks = create_mixed_rows_layout(front_rows=8, desks_per_front_row=3, back_row_desks=3)

    assert all(desk.facing == "front" for desk in desks[:-3])
    assert all(desk.facing == "back" for desk in desks[-3:])


def test_u_shape_inside_layout_faces_desks_inward():
    desks = create_u_shape_layout(left_side=4, bottom_side=6, right_side=4, facing="inside")

    assert {desk.facing for desk in desks} == {"inside"}


def test_u_shape_outside_layout_faces_desks_outward():
    desks = create_u_shape_layout(left_side=4, bottom_side=6, right_side=4, facing="outside")

    assert {desk.facing for desk in desks} == {"outside"}
