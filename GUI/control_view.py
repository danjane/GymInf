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


def create_class_list_buttons(students, height, file):
    student_buttons = []
    y_pos = 15
    i = 0
    for (i, student) in enumerate(students):
        student_buttons.append(
            icons.TextButtonLinkedToFile((300, y_pos), (250, height), student, file, i)
        )
        y_pos += height + 1
    while i < 23:
        student_buttons.append(
            icons.TextButtonLinkedToFile((300, y_pos), (250, height), "", None, i)
        )
        y_pos += height + 1
        i += 1
    for button in student_buttons:
        button.linked_buttons = student_buttons
    return student_buttons


def class_list_from_file(config_file, selected_course, student_button_height):
    students, file = link_gui_backend.load_students(config_file, selected_course)
    student_buttons = create_class_list_buttons(students, student_button_height, file)
    return student_buttons


def turn_off_editors(buttons, button):
    if button in buttons:
        for b in buttons:
            if b != button:
                b.text_editor_active = False


def flatten(list_of_lists):
    return [b for sublist in list_of_lists for b in sublist]


def run(config_file, selected_course, screen, clock, constants):

    courses = link_gui_backend.courses(config_file)

    background_heights = constants.WIDTH_HEIGHT[1] - 20 * 2
    classes_rect = pygame.Rect(15, 15, 280, background_heights)

    student_button_height = background_heights // 24
    student_buttons = create_class_list_buttons(["StudentID, StudentName"], student_button_height, None)
    if selected_course:
        new_buttons = class_list_from_file(config_file, selected_course, student_button_height)
        for (i, student_button) in enumerate(new_buttons):
            student_buttons[i] = student_button

    add_course_button = icons.Button((25, 25), (125, 50), "Add Course")
    delete_course_button = icons.Button((160, 25), (125, 50), "Delete Course")

    course_buttons = []
    course_y_pos = 85
    for course in courses:
        course_button = icons.Button((25, course_y_pos), (260, 25), course)
        course_buttons.append(course_button)
        if course == selected_course:
            select_course_button(course_button, course_buttons)
        course_y_pos += 30

    class_view_button = icons.Button((700, 25), (200, 50), "Go to class view")

    control_buttons = [
        icons.ButtonWhichCallsFunction((700, 90), (200, 50), "Build reports",
                                       link_gui_backend.build_reports, config_file),
        icons.Button((700, 145), (200, 50), "Calculate moyennes"),
    ]

    buttons = [[add_course_button, delete_course_button, class_view_button],
               course_buttons, control_buttons, student_buttons]
    button = control_buttons[0]  # TODO create a proper holding button

    while True:
        screen.fill(constants.BACKGROUND)
        pygame.draw.rect(screen, DARK_GREY, classes_rect)
        flat_buttons = flatten(buttons)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", selected_course
            if event.type == KEYDOWN and button.text_editor_active:
                button.handle_keydown(event, [button])
            if event.type == MOUSEBUTTONDOWN:
                button, _ = events.handle_mouse_button_down(
                    *event.pos, flat_buttons, []
                )
                turn_off_editors(flat_buttons, button)
                if button == class_view_button and selected_course:
                    return "class_view", selected_course
                if button == delete_course_button and selected_course:
                    link_gui_backend.delete_course_in_files(config_file, selected_course)
                    return "control_view", None
                if button == add_course_button:
                    new_course = events.handle_add_course_button_click(add_course_button)
                    if new_course:
                        add_course_button.set_text("Add Course")
                        course_button = icons.Button((25, course_y_pos), (260, 25), new_course)
                        course_y_pos += 30
                        selected_course = new_course
                        course_buttons.append(course_button)
                        select_course_button(course_button, course_buttons)
                        courses = link_gui_backend.add_courses_in_files(config_file, new_course, courses)
                if button in course_buttons:
                    selected_course = button.text
                    select_course_button(button, course_buttons)
                    new_buttons = class_list_from_file(config_file, selected_course, student_button_height)
                    for (i, student_button) in enumerate(new_buttons):
                        student_buttons[i] = student_button

        for b in flat_buttons:
            b.update(screen)
        pygame.display.flip()
        clock.tick(60)
