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


def test_seating_plan_view_randomize_button_calls_backend(monkeypatch):
    import pygame
    pygame.init()
    import seating_plan_view

    created_buttons = {}
    calls = {"randomize": 0}

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

    seating_state = {
        "gui_places": {},
        "desks": [],
        "assignments": {},
    }

    event_calls = {"count": 0}

    def fake_event_get():
        event_calls["count"] += 1
        if event_calls["count"] == 1:
            return [SimpleNamespace(type=seating_plan_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        if event_calls["count"] == 2:
            return [SimpleNamespace(type=seating_plan_view.pygame.QUIT)]
        return []

    monkeypatch.setattr(seating_plan_view.seating_plan_gui_backend, "load_plan", lambda *args: seating_state)
    monkeypatch.setattr(
        seating_plan_view.link_gui_backend,
        "desks_from_seating_state",
        lambda seating_state, width_height_desks: ([], (8, 7)),
    )
    monkeypatch.setattr(
        seating_plan_view.seating_plan_gui_backend,
        "randomize_plan",
        lambda *args, **kwargs: calls.__setitem__("randomize", calls["randomize"] + 1) or {},
    )
    monkeypatch.setattr(seating_plan_view.icons, "Button", fake_button)
    monkeypatch.setattr(
        seating_plan_view.events,
        "handle_mouse_button_down",
        lambda x, y, buttons, selected: (created_buttons["Randomize"], selected),
    )
    monkeypatch.setattr(seating_plan_view.pygame.event, "get", fake_event_get)
    monkeypatch.setattr(seating_plan_view.pygame.display, "flip", lambda: None)

    screen = SimpleNamespace(fill=lambda *args, **kwargs: None)
    clock = SimpleNamespace(tick=lambda *args, **kwargs: None)
    constants = SimpleNamespace(BACKGROUND=(0, 0, 0), WIDTH_HEIGHT_DESKS=(640, 350))

    seating_plan_view.run("config.yaml", "1ma1df01", screen, clock, constants)

    assert calls["randomize"] == 1


def test_seating_plan_view_alphabetic_button_calls_backend(monkeypatch):
    import pygame
    pygame.init()
    import seating_plan_view

    created_buttons = {}
    calls = {"alphabetic": 0}

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

    seating_state = {
        "gui_places": {},
        "desks": [],
        "assignments": {},
    }

    event_calls = {"count": 0}

    def fake_event_get():
        event_calls["count"] += 1
        if event_calls["count"] == 1:
            return [SimpleNamespace(type=seating_plan_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        if event_calls["count"] == 2:
            return [SimpleNamespace(type=seating_plan_view.pygame.QUIT)]
        return []

    monkeypatch.setattr(seating_plan_view.seating_plan_gui_backend, "load_plan", lambda *args: seating_state)
    monkeypatch.setattr(
        seating_plan_view.link_gui_backend,
        "desks_from_seating_state",
        lambda seating_state, width_height_desks: ([], (8, 7)),
    )
    monkeypatch.setattr(
        seating_plan_view.seating_plan_gui_backend,
        "alphabetic_plan",
        lambda *args, **kwargs: calls.__setitem__("alphabetic", calls["alphabetic"] + 1) or {},
    )
    monkeypatch.setattr(seating_plan_view.icons, "Button", fake_button)
    monkeypatch.setattr(
        seating_plan_view.events,
        "handle_mouse_button_down",
        lambda x, y, buttons, selected: (created_buttons["Alphabetic"], selected),
    )
    monkeypatch.setattr(seating_plan_view.pygame.event, "get", fake_event_get)
    monkeypatch.setattr(seating_plan_view.pygame.display, "flip", lambda: None)

    screen = SimpleNamespace(fill=lambda *args, **kwargs: None)
    clock = SimpleNamespace(tick=lambda *args, **kwargs: None)
    constants = SimpleNamespace(BACKGROUND=(0, 0, 0), WIDTH_HEIGHT_DESKS=(640, 350))

    seating_plan_view.run("config.yaml", "1ma1df01", screen, clock, constants)

    assert calls["alphabetic"] == 1


def test_seating_plan_view_syncs_live_assignments_before_randomize(monkeypatch):
    import pygame
    pygame.init()
    import seating_plan_view

    created_buttons = {}
    captured_assignments = {}

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

    desks = [
        SimpleNamespace(desk_id="front_left", name="Albert", update=lambda screen: None),
        SimpleNamespace(desk_id="back_left", name="", update=lambda screen: None),
    ]
    seating_state = {
        "gui_places": {},
        "desks": [],
        "assignments": {"front_left": "", "back_left": "Albert"},
    }

    event_calls = {"count": 0}

    def fake_event_get():
        event_calls["count"] += 1
        if event_calls["count"] == 1:
            return [SimpleNamespace(type=seating_plan_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        if event_calls["count"] == 2:
            return [SimpleNamespace(type=seating_plan_view.pygame.QUIT)]
        return []

    monkeypatch.setattr(seating_plan_view.seating_plan_gui_backend, "load_plan", lambda *args: seating_state)
    monkeypatch.setattr(
        seating_plan_view.link_gui_backend,
        "desks_from_seating_state",
        lambda seating_state, width_height_desks: (desks, (8, 7)),
    )
    monkeypatch.setattr(
        seating_plan_view.seating_plan_gui_backend,
        "randomize_plan",
        lambda cfg_path, course, state, seed=None: captured_assignments.update(state["assignments"]) or state["assignments"],
    )
    monkeypatch.setattr(seating_plan_view.icons, "Button", fake_button)
    monkeypatch.setattr(
        seating_plan_view.events,
        "handle_mouse_button_down",
        lambda x, y, buttons, selected: (created_buttons["Randomize"], selected),
    )
    monkeypatch.setattr(seating_plan_view.pygame.event, "get", fake_event_get)
    monkeypatch.setattr(seating_plan_view.pygame.display, "flip", lambda: None)

    screen = SimpleNamespace(fill=lambda *args, **kwargs: None)
    clock = SimpleNamespace(tick=lambda *args, **kwargs: None)
    constants = SimpleNamespace(BACKGROUND=(0, 0, 0), WIDTH_HEIGHT_DESKS=(640, 350))

    seating_plan_view.run("config.yaml", "1ma1df01", screen, clock, constants)

    assert captured_assignments == {"front_left": "Albert", "back_left": ""}
