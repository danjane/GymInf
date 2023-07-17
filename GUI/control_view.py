import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


def select_course_button(clicked_button, course_buttons):
    for button in course_buttons:
        button.color_unclicked = button.color_default
    clicked_button.color_unclicked = clicked_button.color_selected


def run(config_file, selected_course, screen, clock, constants):

    courses = link_gui_backend.courses(config_file)

    edit_buttons = [
        icons.Button((25, 25), (125, 75), "Edit Courses"),
        icons.Button((160, 25), (125, 75), "Edit ClassList")
    ]

    refresh_button = icons.Button((295, 25), (125, 75), "Refresh")

    course_buttons = []
    y_pos = 125
    for course in courses:
        course_button = icons.Button((25, y_pos), (395, 25), course)
        course_buttons.append(course_button)
        if course == selected_course:
            select_course_button(course_button, course_buttons)
        y_pos += 30

    class_view_button = icons.Button((500, 25), (125, 75), "Go to class view")

    control_buttons = [
        icons.Button((500, 110), (125, 75), "Build reports"),
        icons.Button((500, 195), (125, 75), "Calculate moyennes"),
    ]

    buttons = edit_buttons + course_buttons + [class_view_button, refresh_button] + control_buttons
    sprites = pygame.sprite.Group(buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_course
            if event.type == MOUSEBUTTONDOWN:
                button, _ = events.handle_mouse_button_down(
                    *event.pos, buttons, []
                )
                if button == class_view_button:
                    return "class_view", selected_course
                if button == refresh_button:
                    return "control_view", selected_course
                if button in course_buttons:
                    selected_course = button.text
                    select_course_button(button, course_buttons)

        sprites.update(screen)
        pygame.display.flip()
        clock.tick(60)
