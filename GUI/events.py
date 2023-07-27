import icons
import pygame


def handle_mouse_button_down(x, y, desks, selected_desks):
    for desk in desks:
        if desk.rect.collidepoint(x, y):
            return desk.clicked(selected_desks)
    return icons.UnclickedDesk(), selected_desks


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
        clicked_desk.color = clicked_desk.color_default
        clicked_desk = clicked_desk.unclicked(swapping_desk)
        for desk in selected_desks:
            desk.color = desk.color_default
        return clicked_desk, set()
    else:
        selected_desks = clicked_desk.append(selected_desks)
        new_clicked_desk = clicked_desk.unclicked(swapping_desk)
        return new_clicked_desk, selected_desks


def handle_add_course_button_click(button):
    if button.text_editor_active:
        button.text_editor_active = False
        return button.text
    else:
        button.text_editor_active = True
        button.text = ""
        return None


def turn_off_editors(buttons, button):
    if button in buttons:
        for b in buttons:
            if b != button:
                b.text_editor_active = False

