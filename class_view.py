import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


def create_text_editor_comment_buttons(pn, pos, size, step, file, number, comment_file):
    buttons = []
    x_pos, y_pos = pos
    x_size, y_size = size
    x_size_quick = x_size // 4
    x_size_text = x_size - x_size_quick
    for count in range(number):
        if pn == "+":
            quick_button = icons.PositiveButton((x_pos, y_pos), (x_size_quick, y_size), comment_file)
        else:
            quick_button = icons.NegativeButton((x_pos, y_pos), (x_size_quick, y_size), comment_file)

        text_button = icons.TextButtonLinkedToFile(
            (x_pos + x_size_quick + 5, y_pos), (x_size_text - 5, y_size), None, file, count)
        quick_button.linked_button = text_button

        buttons.append(quick_button)
        buttons.append(text_button)
        y_pos += step
    return buttons


def run(config_file, course, screen, clock, constants):
    seating_plan, desk_layout, comment_file, positive_defaults, negative_defaults = link_gui_backend.setup(config_file,
                                                                                                           course)

    desks = []
    for place, student in seating_plan.items():
        desk = icons.Desk.create_desk(place, student, desk_layout, constants.WIDTH_HEIGHT_DESKS)
        desks.append(desk)

    clicked_desk = icons.UnclickedDesk()
    swapping_desk = icons.UnclickedDesk()
    selected_desks = set()

    control_view_button = icons.Button((700, 25), (200, 50), "Go to control")

    buttons = [
                  icons.SuggestFocusButton((700, 270), (200, 50), desks, comment_file,
                                           config_file, course)
              ] + create_text_editor_comment_buttons("+", (700, 90), (200, 20), 25,
                                                     positive_defaults, 4, comment_file) + \
              create_text_editor_comment_buttons("-", (700, 200), (200, 20), 25,
                                                 negative_defaults, 2,comment_file)

    sprites = pygame.sprite.Group(desks + buttons + [control_view_button])

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            if event.type == MOUSEBUTTONDOWN:
                clicked_desk, selected_desks = events.handle_mouse_button_down(
                    *event.pos, sprites.sprites(), selected_desks
                )
                if clicked_desk in buttons:
                    events.turn_off_editors(buttons, clicked_desk)
                elif clicked_desk == control_view_button:
                    return "control_view", course
            if event.type == MOUSEBUTTONUP and isinstance(clicked_desk, icons.Desk):
                clicked_desk, selected_desks = \
                    events.handle_mouse_button_up(clicked_desk, swapping_desk, selected_desks)
                swapping_desk = icons.UnclickedDesk()
            if event.type == MOUSEMOTION and isinstance(clicked_desk, icons.Desk):
                clicked_desk.move(*event.rel)
            if event.type == KEYDOWN:
                clicked_desk.handle_keydown(event, selected_desks)

        if isinstance(clicked_desk, icons.Desk):
            swapping_desk = events.update_swapping_desk(desks, clicked_desk, swapping_desk)

        sprites.update(screen)
        if isinstance(clicked_desk, icons.Desk):
            clicked_desk.update(screen)

        pygame.display.flip()
        clock.tick(60)
