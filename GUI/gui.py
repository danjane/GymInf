import pygame
from pygame.locals import *
pygame.init()

import icons
import events
import desk_functions

BACKGROUND = (0, 0, 0)

places = desk_functions.standard_pairs_layout(6, 4)
desk_layout = (places[-1][0] + 1, places[-1][1] + 1)
WIDTH_HEIGHT_DESKS = (desk_layout[0] * 80, desk_layout[1] * 50)

WIDTH_HEIGHT = (WIDTH_HEIGHT_DESKS[0] + 300, WIDTH_HEIGHT_DESKS[1])

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WIDTH_HEIGHT)

# desks = pygame.sprite.Group()
desks = []
for place in places:
    desk = icons.Desk(place, str(place), desk_layout, WIDTH_HEIGHT_DESKS)
    desks.append(desk)
clicked_desk = icons.UnclickedDesk()
swapping_desk = icons.UnclickedDesk()

selected_desks = set()

buttons = [
    icons.Button((700, 25), (200, 75), "positive"),
    icons.Button((700, 140), (200, 75), "negative"),
    icons.Button((700, 255), (200, 75), "suggestions")
]

sprites = pygame.sprite.Group(desks, buttons)

running = True
while running:
    screen.fill(BACKGROUND)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            clicked_desk, selected_desks = events.mouse_button_down_desks(*event.pos, desks, selected_desks)
            selected_desks = events.mouse_button_down_buttons(*event.pos, buttons, selected_desks)
            print(selected_desks)
        if event.type == MOUSEBUTTONUP:
            clicked_desk, selected_desks = \
                events.mouse_button_up(clicked_desk, swapping_desk, selected_desks)
        if event.type == MOUSEMOTION:
            clicked_desk.move(*event.rel)

    swapping_desk = events.update_swapping_desk(desks, clicked_desk, swapping_desk)

    sprites.update(screen)
    clicked_desk.update(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
