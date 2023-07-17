import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


def run(config_file, course, screen, clock, constants):
    seating_plan, desk_layout, comment_file = link_gui_backend.setup(config_file, course)

    desks = []
    for student, place in seating_plan.items():
        desk = icons.Desk.create_desk(place, student, desk_layout, constants.WIDTH_HEIGHT_DESKS)
        desks.append(desk)

    clicked_desk = icons.UnclickedDesk()
    swapping_desk = icons.UnclickedDesk()
    selected_desks = set()

    buttons = [
        icons.PositiveButton((700, 25), (200, 75), comment_file),
        icons.NegativeButton((700, 140), (200, 75), comment_file),
        icons.SuggestionsButton((700, 255), (200, 75), desks, comment_file,
                                config_file, course)
    ]
    selected_button = 0

    sprites = pygame.sprite.Group(desks + buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                clicked_desk, selected_desks = events.handle_mouse_button_down(
                    *event.pos, desks + buttons, selected_desks
                )
            if event.type == MOUSEBUTTONUP:
                clicked_desk, selected_desks = \
                    events.handle_mouse_button_up(clicked_desk, swapping_desk, selected_desks)
            if event.type == MOUSEMOTION:
                clicked_desk.move(*event.rel)
            if event.type == KEYDOWN:
                selected_button = events.handle_keydown(event, selected_desks, selected_button, buttons)

        swapping_desk = events.update_swapping_desk(desks, clicked_desk, swapping_desk)

        sprites.update(screen)
        clicked_desk.update(screen)
        pygame.display.flip()
        clock.tick(60)
