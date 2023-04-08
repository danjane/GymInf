import icons


def mouse_button_down_desks(x, y, desks, selected_desks):
    for desk in desks:
        if desk.rect.collidepoint(x, y):
            desk.clicked()
            selected_desks.add(desk)
            return desk, selected_desks
    return icons.UnclickedDesk(), selected_desks


def mouse_button_down_buttons(x, y, desks, selected_desks):
    for desk in desks:
        if desk.rect.collidepoint(x, y):
            desk.clicked()
            for desk in selected_desks:
                desk.color = icons.YELLOW
            return set()
    return selected_desks

def update_swapping_desk(desks, clicked_desk, swapping_desk):
    new_swapping_desk = clicked_desk.check_collisions(desks, swapping_desk)
    #print(new_swapping_desk, swapping_desk, clicked_desk)
    if new_swapping_desk != swapping_desk:
        clicked_desk.changing_position = True
        new_swapping_desk.bothered(clicked_desk)
        swapping_desk.unbothered()
    return new_swapping_desk


def mouse_button_up(clicked_desk, swapping_desk, selected_desks):
    if swapping_desk.is_swapping:
        clicked_desk = clicked_desk.unclicked(swapping_desk)
        for desk in selected_desks:
            desk.color = icons.YELLOW
        return clicked_desk, set()
    else:
        selected_desks.add(clicked_desk)
        new_clicked_desk = clicked_desk.unclicked(swapping_desk)
        clicked_desk.color = icons.LIGHT_BLUE
        return new_clicked_desk, selected_desks