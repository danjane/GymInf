import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


def run(config_file, screen, clock, constants):

    courses = link_gui_backend.courses(config_file)

    buttons = [
        icons.Button((25, 25), (125, 75), "Edit Courses"),
        icons.Button((160, 25), (125, 75), "Edit ClassList"),
        icons.Button((295, 25), (125, 75), "Refresh")
    ]
    selected_course = courses[0]

    sprites = pygame.sprite.Group(buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == MOUSEBUTTONDOWN:
                _ = events.handle_mouse_button_down_buttons(
                    *event.pos, buttons, []
                )

        sprites.update(screen)
        pygame.display.flip()
        clock.tick(60)
