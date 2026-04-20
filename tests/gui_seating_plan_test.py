from pathlib import Path
from types import SimpleNamespace


def test_control_view_can_switch_to_seating_plan_view(monkeypatch):
    import pygame
    pygame.init()
    import control_view

    created_buttons = {}

    class FakeButton:
        def __init__(self, text):
            self.text = text
            self.color_default = (0, 0, 0)
            self.color_selected = (1, 1, 1)
            self.color_unclicked = self.color_default
            self.text_editor_active = False

        def update(self, screen):
            pass

    def fake_button(pos, size, text):
        button = FakeButton(text)
        created_buttons[text] = button
        return button

    def fake_button_which_calls_function(pos, size, text, *args):
        return fake_button(pos, size, text)

    event_calls = {"count": 0}

    def fake_event_get():
        event_calls["count"] += 1
        if event_calls["count"] == 1:
            return [SimpleNamespace(type=control_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        raise AssertionError("control_view.run did not return after the seating plan click")

    monkeypatch.setattr(control_view.link_gui_backend, "courses", lambda cfg: ["1ma1df01"])
    monkeypatch.setattr(control_view, "create_class_list_buttons", lambda students, height, file: [])
    monkeypatch.setattr(control_view, "class_list_from_file", lambda config_file, selected_course, height: [])
    monkeypatch.setattr(control_view.icons, "Button", fake_button)
    monkeypatch.setattr(control_view.icons, "ButtonWhichCallsFunction", fake_button_which_calls_function)
    monkeypatch.setattr(
        control_view.events,
        "handle_mouse_button_down",
        lambda x, y, buttons, selected: (created_buttons["Go to seating plan"], selected),
    )
    monkeypatch.setattr(control_view.events, "turn_off_editors", lambda buttons, button: None)
    monkeypatch.setattr(control_view.pygame.event, "get", fake_event_get)
    monkeypatch.setattr(control_view.pygame, "draw", SimpleNamespace(rect=lambda *args, **kwargs: None))
    monkeypatch.setattr(control_view.pygame.display, "flip", lambda: None)

    screen = SimpleNamespace(fill=lambda *args, **kwargs: None)
    clock = SimpleNamespace(tick=lambda *args, **kwargs: None)
    constants = SimpleNamespace(WIDTH_HEIGHT=(940, 350), BACKGROUND=(0, 0, 0))

    next_view, course = control_view.run("config.yaml", "1ma1df01", screen, clock, constants)

    assert next_view == "seating_plan_view"
    assert course == "1ma1df01"


def test_gui_main_dispatches_to_seating_plan_view(monkeypatch):
    import gui

    calls = {"seating_plan": 0}

    monkeypatch.setattr(gui.control_view, "run", lambda *args: ("seating_plan_view", "1ma1df01"))
    monkeypatch.setattr(gui.class_view, "run", lambda *args: ("quit", None))
    monkeypatch.setattr(
        gui,
        "seating_plan_view",
        SimpleNamespace(
            run=lambda *args: calls.__setitem__("seating_plan", calls["seating_plan"] + 1) or ("quit", None)
        ),
        raising=False,
    )
    monkeypatch.setattr(gui.pygame.display, "set_mode", lambda *args, **kwargs: object())
    monkeypatch.setattr(gui.pygame.display, "set_caption", lambda *args, **kwargs: None)
    monkeypatch.setattr(gui.pygame, "quit", lambda: None)
    monkeypatch.setattr(gui.pygame.time, "Clock", lambda: SimpleNamespace(tick=lambda *args, **kwargs: None))

    gui.main("config.yaml")

    assert calls["seating_plan"] == 1
