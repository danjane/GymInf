import logging
from pathlib import Path

import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION

import events
import icons
import link_gui_backend
import seating_plan_gui_backend


def apply_assignments_to_desks(desks, seating_state: dict, assignments: dict):
    seating_state["assignments"] = assignments
    for desk in desks:
        desk.name = assignments.get(desk.desk_id, "")
        desk.name_img = icons.font.render(desk.name, True, (0, 0, 0))


def sync_assignments_from_desks(desks, seating_state: dict):
    seating_state["assignments"] = {
        desk.desk_id: desk.name
        for desk in desks
        if getattr(desk, "desk_id", None)
    }


class _FallbackSpriteContainer:
    def __init__(self, sprites):
        self._sprites = list(sprites)

    def sprites(self):
        return list(self._sprites)

    def update(self, screen):
        for sprite in self._sprites:
            if hasattr(sprite, "update"):
                sprite.update(screen)


def build_sprite_container(sprites):
    try:
        return pygame.sprite.Group(sprites)
    except (TypeError, AttributeError):
        return _FallbackSpriteContainer(sprites)


def run(config_file, course, screen, clock, constants):
    seating_state = seating_plan_gui_backend.load_plan(config_file, course)
    desks, desk_layout = link_gui_backend.desks_from_seating_state(
        seating_state, constants.WIDTH_HEIGHT_DESKS
    )

    clicked_desk = icons.UnclickedDesk()
    swapping_desk = icons.UnclickedDesk()
    selected_desks = set()
    unsaved_changes = False

    control_view_button = icons.Button((700, 25), (200, 50), "Go to control")
    dump_to_pdf_button = icons.Button((700, 90), (200, 50), "Dump to pdf")
    save_button = icons.Button((700, 145), (200, 50), "Save")
    randomize_button = icons.Button((700, 200), (200, 50), "Randomize")
    alphabetic_button = icons.Button((700, 255), (200, 50), "Alphabetic")
    buttons = [control_view_button, dump_to_pdf_button, save_button, randomize_button, alphabetic_button]
    arrangement_buttons = {
        randomize_button: seating_plan_gui_backend.randomize_plan,
        alphabetic_button: seating_plan_gui_backend.alphabetic_plan,
    }
    sprites = build_sprite_container(desks + buttons)

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
                elif clicked_desk in arrangement_buttons:
                    sync_assignments_from_desks(desks, seating_state)
                    assignments = arrangement_buttons[clicked_desk](config_file, course, seating_state)
                    apply_assignments_to_desks(desks, seating_state, assignments)
                    unsaved_changes = True
                    clicked_desk = icons.UnclickedDesk()
                elif clicked_desk == dump_to_pdf_button:
                    if unsaved_changes:
                        seating_plan_gui_backend.save_plan(config_file, course, seating_state, desks)
                        unsaved_changes = False
                    pdf_file = seating_plan_gui_backend.dump_plan_pdf(config_file, course, seating_state)
                    link_gui_backend.open_file(str(Path(pdf_file).parent))
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
