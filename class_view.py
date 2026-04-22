from dataclasses import dataclass, field
from enum import Enum, auto

import pygame
from pygame.locals import *
import icons
import events
import gui_layout
import link_gui_backend
import logging


CONTROL_BUTTON_POS, LARGE_BUTTON_SIZE = gui_layout.right_action_button(0)
SUGGESTIONS_BUTTON_POS, _ = gui_layout.right_action_button(5)
ABSENCES_BUTTON_POS, _ = gui_layout.right_action_button(6)
COMMENT_POSITIVE_START = (gui_layout.RIGHT_PANEL_X, 70)
COMMENT_NEGATIVE_START = (gui_layout.RIGHT_PANEL_X, 170)
COMMENT_BUTTON_SIZE = (200, 20)
COMMENT_STEP = 25


class ClassViewMode(Enum):
    NORMAL = auto()
    UPDATE_ABSENCES = auto()


@dataclass
class ClassViewState:
    mode: ClassViewMode = ClassViewMode.NORMAL
    selected_desks: set = field(default_factory=set)
    absent_students: set[str] = field(default_factory=set)


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


def create_class_view_buttons(comment_file, positive_defaults, negative_defaults, config_file, course, desks):
    absences_button = icons.Button(ABSENCES_BUTTON_POS, LARGE_BUTTON_SIZE, "Absences")
    action_buttons = [
        icons.SuggestFocusButton(SUGGESTIONS_BUTTON_POS, LARGE_BUTTON_SIZE, desks, comment_file, config_file, course),
        *create_text_editor_comment_buttons("+", COMMENT_POSITIVE_START, COMMENT_BUTTON_SIZE, COMMENT_STEP,
                                            positive_defaults, 4, comment_file),
        *create_text_editor_comment_buttons("-", COMMENT_NEGATIVE_START, COMMENT_BUTTON_SIZE, COMMENT_STEP,
                                            negative_defaults, 2, comment_file),
        absences_button,
    ]
    return action_buttons, absences_button


def set_absence_mode(absences_button, enabled: bool) -> bool:
    absences_button.color_unclicked = icons.LIGHT_BLUE if enabled else absences_button.color_default
    return enabled


def sync_absence_button(state: ClassViewState, absences_button):
    absences_button.color_unclicked = (
        icons.LIGHT_BLUE if state.mode == ClassViewMode.UPDATE_ABSENCES else absences_button.color_default
    )


def set_mode(state: ClassViewState, mode: ClassViewMode, absences_button):
    state.mode = mode
    sync_absence_button(state, absences_button)


def toggle_absence_mode(state: ClassViewState, absences_button):
    if state.mode == ClassViewMode.UPDATE_ABSENCES:
        set_mode(state, ClassViewMode.NORMAL, absences_button)
    else:
        set_mode(state, ClassViewMode.UPDATE_ABSENCES, absences_button)


def toggle_desk_absence(desk, state: ClassViewState, seating_state):
    desk.toggle_absent()
    absent_students = seating_state.setdefault("absent_students", state.absent_students)
    if desk.is_absent():
        absent_students.add(desk.student_name())
    else:
        absent_students.discard(desk.student_name())
    state.absent_students = absent_students


def handle_button_or_mode_click(clicked_desk, buttons, control_view_button, absences_button, state,
                                seating_state, course):
    if clicked_desk == absences_button:
        toggle_absence_mode(state, absences_button)
        return icons.UnclickedDesk(), None
    if state.mode == ClassViewMode.UPDATE_ABSENCES and isinstance(clicked_desk, icons.FilledDesk):
        toggle_desk_absence(clicked_desk, state, seating_state)
        return icons.UnclickedDesk(), None
    if clicked_desk in buttons:
        if getattr(clicked_desk, "text", "") == "suggestions":
            set_mode(state, ClassViewMode.NORMAL, absences_button)
        events.turn_off_editors(buttons, clicked_desk)
        return clicked_desk, None
    if clicked_desk == control_view_button:
        logging.info("class_view returning to control_view course=%s", course)
        return clicked_desk, ("control_view", course)
    return clicked_desk, None


def run(config_file, course, screen, clock, constants):
    seating_state, desk_layout, comment_file, positive_defaults, negative_defaults = link_gui_backend.setup(
        config_file, course
    )
    desks, desk_layout = link_gui_backend.desks_from_seating_state(
        seating_state, constants.WIDTH_HEIGHT_DESKS
    )

    clicked_desk = icons.UnclickedDesk()
    swapping_desk = icons.UnclickedDesk()
    state = ClassViewState(absent_students=seating_state.get("absent_students", set()))

    control_view_button = icons.Button(CONTROL_BUTTON_POS, LARGE_BUTTON_SIZE, "Go to control")
    buttons, absences_button = create_class_view_buttons(
        comment_file, positive_defaults, negative_defaults, config_file, course, desks
    )
    sync_absence_button(state, absences_button)

    sprites = pygame.sprite.Group(desks + buttons + [control_view_button])

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("class_view received pygame.QUIT course=%s", course)
                return "quit", None
            if event.type == MOUSEBUTTONDOWN:
                clicked_desk, state.selected_desks = events.handle_mouse_button_down(
                    *event.pos, sprites.sprites(), state.selected_desks
                )
                clicked_desk, transition = handle_button_or_mode_click(
                    clicked_desk,
                    buttons,
                    control_view_button,
                    absences_button,
                    state,
                    seating_state,
                    course,
                )
                if transition:
                    return transition
            if event.type == MOUSEBUTTONUP and isinstance(clicked_desk, icons.Desk):
                clicked_desk, state.selected_desks, seating_changed = \
                    events.handle_mouse_button_up(clicked_desk, swapping_desk, state.selected_desks)
                if seating_changed:
                    logging.info(
                        "class_view saving seating change course=%s selected_count=%s",
                        course,
                        len(state.selected_desks),
                    )
                    link_gui_backend.save_seating_state(config_file, course, seating_state, desks)
                swapping_desk = icons.UnclickedDesk()
            if event.type == MOUSEMOTION and isinstance(clicked_desk, icons.Desk):
                clicked_desk.move(*event.rel)
            if event.type == KEYDOWN:
                clicked_desk.handle_keydown(event, state.selected_desks)

        if isinstance(clicked_desk, icons.Desk):
            swapping_desk = events.update_swapping_desk(desks, clicked_desk, swapping_desk)

        sprites.update(screen)
        if isinstance(clicked_desk, icons.Desk):
            clicked_desk.update(screen)

        pygame.display.flip()
        clock.tick(60)
