import logging

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

import events
import icons
import seating_plan_gui_backend


def run(config_file, course, screen, clock, constants):
    seating_state = seating_plan_gui_backend.load_plan(config_file, course)
    desk_layout = (
        max(position[0] for position in seating_state["gui_places"].values()) + 1,
        max(position[1] for position in seating_state["gui_places"].values()) + 1,
    )

    desks = []
    for desk_data in seating_state["desks"]:
        student = seating_state["assignments"].get(desk_data.desk_id, "empty")
        gui_place = seating_state["gui_places"][desk_data.desk_id]
        desks.append(
            icons.Desk.create_desk(
                gui_place,
                student,
                desk_layout,
                constants.WIDTH_HEIGHT_DESKS,
                desk_id=desk_data.desk_id,
            )
        )

    clicked_desk = icons.UnclickedDesk()
    swapping_desk = icons.UnclickedDesk()
    selected_desks = set()
    unsaved_changes = False

    control_view_button = icons.Button((700, 25), (200, 50), "Go to control")
    dump_to_pdf_button = icons.Button((700, 90), (200, 50), "Dump to pdf")
    save_button = icons.Button((700, 145), (200, 50), "Save")
    buttons = [control_view_button, dump_to_pdf_button, save_button]
    sprites = pygame.sprite.Group(desks + buttons)

    while True:
        screen.fill(constants.BACKGROUND)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("seating_plan_view received pygame.QUIT course=%s", course)
                return "quit", None
            if event.type == MOUSEBUTTONDOWN:
                clicked_desk, selected_desks = events.handle_mouse_button_down(
                    *event.pos, sprites.sprites(), selected_desks
                )
                if clicked_desk == control_view_button:
                    logging.info("seating_plan_view returning to control_view course=%s", course)
                    return "control_view", course
                if clicked_desk == save_button:
                    seating_plan_gui_backend.save_plan(config_file, course, seating_state, desks)
                    unsaved_changes = False
                    clicked_desk = icons.UnclickedDesk()
                elif clicked_desk == dump_to_pdf_button:
                    if unsaved_changes:
                        seating_plan_gui_backend.save_plan(config_file, course, seating_state, desks)
                        unsaved_changes = False
                    seating_plan_gui_backend.dump_plan_pdf(config_file, course, seating_state)
                    clicked_desk = icons.UnclickedDesk()
            if event.type == MOUSEBUTTONUP and isinstance(clicked_desk, icons.Desk):
                clicked_desk, selected_desks, seating_changed = events.handle_mouse_button_up(
                    clicked_desk, swapping_desk, selected_desks
                )
                if seating_changed:
                    unsaved_changes = True
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
