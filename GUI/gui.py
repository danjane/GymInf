import pygame
from pygame.locals import *
from typing import Tuple

pygame.init()

import icons
import events
import link_gui_backend

BACKGROUND: Tuple[int, int, int] = (0, 0, 0)

seating_plan, desk_layout = link_gui_backend.setup("../example_files/config_GUI.yaml", "2ma2dfb01")
WIDTH_HEIGHT_DESKS = (desk_layout[0] * 80, desk_layout[1] * 50)

WIDTH_HEIGHT = (WIDTH_HEIGHT_DESKS[0] + 300, WIDTH_HEIGHT_DESKS[1])

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIDTH_HEIGHT)

desks = []
for student, place in seating_plan.items():
    desk = icons.Desk(place, student, desk_layout, WIDTH_HEIGHT_DESKS)
    desks.append(desk)

clicked_desk = icons.UnclickedDesk()
swapping_desk = icons.UnclickedDesk()
selected_desks = set()

buttons = [
    icons.PositiveButton((700, 25), (200, 75)),
    icons.NegativeButton((700, 140), (200, 75)),
    icons.SuggestionsButton((700, 255), (200, 75), desks)
]

sprites = pygame.sprite.Group(desks + buttons)

running = True
while running:
    screen.fill(BACKGROUND)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            # TODO merge events.handle_mouse_button_down
            clicked_desk, selected_desks = events.handle_mouse_button_down_desks(
                *event.pos, desks, selected_desks
            )
            selected_desks = events.handle_mouse_button_down_buttons(
                *event.pos, buttons, selected_desks
            )
        if event.type == MOUSEBUTTONUP:
            clicked_desk, selected_desks = \
                events.handle_mouse_button_up(clicked_desk, swapping_desk, selected_desks)
        if event.type == MOUSEMOTION:
            clicked_desk.move(*event.rel)
        if event.type == KEYDOWN:
            buttons[0].handle_keydown(event, selected_desks)

    swapping_desk = events.update_swapping_desk(desks, clicked_desk, swapping_desk)

    sprites.update(screen)
    clicked_desk.update(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
