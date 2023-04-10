import icons


def handle_mouse_button_down_desks(x, y, desks, selected_desks):
    for desk in desks:
        if desk.rect.collidepoint(x, y):
            desk.clicked()
            return desk, selected_desks
    return icons.UnclickedDesk(), selected_desks


def handle_mouse_button_down_buttons(x, y, desks, selected_desks):
    for desk in desks:
        if desk.rect.collidepoint(x, y):
            return desk.clicked(selected_desks)
    return selected_desks


def update_swapping_desk(desks, clicked_desk, swapping_desk):
    new_swapping_desk = clicked_desk.check_collisions(desks, swapping_desk)
    if new_swapping_desk != swapping_desk:
        clicked_desk.changing_position = True
        new_swapping_desk.bothered(clicked_desk)
        swapping_desk.unbothered()
    return new_swapping_desk


def handle_mouse_button_up(clicked_desk, swapping_desk, selected_desks):
    # TODO is_swapping flag should be handled by desk object
    if swapping_desk.is_swapping:
        clicked_desk.color = icons.YELLOW
        clicked_desk = clicked_desk.unclicked(swapping_desk)
        for desk in selected_desks:
            desk.color = icons.YELLOW
        return clicked_desk, set()
    else:
        selected_desks = clicked_desk.append(selected_desks)
        new_clicked_desk = clicked_desk.unclicked(swapping_desk)
        return new_clicked_desk, selected_desks
