import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


def run(config_file, screen, clock, constants):

    courses = link_gui_backend.courses(config_file)

    edit_buttons = [
        icons.Button((25, 25), (125, 75), "Edit Courses"),
        icons.Button((160, 25), (125, 75), "Edit ClassList"),
        icons.Button((295, 25), (125, 75), "Refresh")
    ]

    course_buttons = []
    y_pos = 125
    for course in courses:
        course_buttons.append(icons.Button((25, y_pos), (395, 25), course))
        y_pos += 30

    control_buttons = [
        icons.Button((500, 25), (125, 75), "Go to class view"),
        icons.Button((500, 110), (125, 75), "Build reports"),
        icons.Button((500, 195), (125, 75), "Calculate moyennes"),
    ]

    selected_course = courses[0]

    buttons = edit_buttons + course_buttons + control_buttons
    sprites = pygame.sprite.Group(buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_course
            if event.type == MOUSEBUTTONDOWN:
                _ = events.handle_mouse_button_down(
                    *event.pos, buttons, []
                )

        sprites.update(screen)
        pygame.display.flip()
        clock.tick(60)
