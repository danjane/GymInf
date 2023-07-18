import pygame
from pygame.locals import *
import icons
import events
import link_gui_backend


DARK_GREY = (75, 75, 75)


def select_course_button(clicked_button, course_buttons):
    for button in course_buttons:
        button.color_unclicked = button.color_default
    clicked_button.color_unclicked = clicked_button.color_selected


def run(config_file, selected_course, screen, clock, constants):
    courses = link_gui_backend.courses(config_file)

    background_heights = constants.WIDTH_HEIGHT[1]-20*2
    classes_rect = pygame.Rect(15, 15, 280, background_heights)
    students_rect = pygame.Rect(300, 15, 250, background_heights)
    names_rect = pygame.Rect(555, 15, 130, background_heights)

    add_course_button = icons.Button((25, 25), (125, 50), "Add Course")
    save_class_button = icons.Button((160, 25), (125, 50), "Save ClassList")

    course_buttons = []
    y_pos = 85
    for course in courses:
        course_button = icons.Button((25, y_pos), (260, 25), course)
        course_buttons.append(course_button)
        if course == selected_course:
            select_course_button(course_button, course_buttons)
        y_pos += 30

    class_view_button = icons.Button((700, 25), (200, 50), "Go to class view")

    control_buttons = [
        icons.Button((700, 90), (200, 50), "Build reports"),
        icons.Button((700, 145), (200, 50), "Calculate moyennes"),
    ]

    buttons = [add_course_button, save_class_button, class_view_button] + course_buttons + control_buttons
    sprites = pygame.sprite.Group(buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        pygame.draw.rect(screen, DARK_GREY, classes_rect)
        pygame.draw.rect(screen, DARK_GREY, students_rect)
        pygame.draw.rect(screen, DARK_GREY, names_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_course
            if event.type == KEYDOWN and add_course_button.text_editor_active:
                add_course_button.handle_keydown(event, [add_course_button])
            if event.type == MOUSEBUTTONDOWN:
                button, _ = events.handle_mouse_button_down(
                    *event.pos, buttons, []
                )
                if button == class_view_button and selected_course:
                    return "class_view", selected_course
                if button == add_course_button:
                    refresh_flag = events.handle_add_course_button_click(add_course_button)
                    if refresh_flag:
                        return "control_view", selected_course
                if button in course_buttons:
                    selected_course = button.text
                    select_course_button(button, course_buttons)

        sprites.update(screen)
        pygame.display.flip()
        clock.tick(60)
