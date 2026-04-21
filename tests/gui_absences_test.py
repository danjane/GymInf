from types import SimpleNamespace


def test_class_view_buttons_fit_within_screen_height(monkeypatch):
    import pygame
    pygame.init()
    import class_view

    created_buttons = {}

    class FakeButton:
        def __init__(self, pos, size, text):
            self.pos = pos
            self.size = size
            self.text = text

    monkeypatch.setattr(
        class_view.icons,
        "Button",
        lambda pos, size, text: created_buttons.setdefault(text, FakeButton(pos, size, text)),
    )
    monkeypatch.setattr(
        class_view.icons,
        "SuggestFocusButton",
        lambda pos, size, desks, comment_file, config_file, course:
        created_buttons.setdefault("suggestions", FakeButton(pos, size, "suggestions")),
    )
    monkeypatch.setattr(class_view, "create_text_editor_comment_buttons", lambda *args: [])

    class_view.create_class_view_buttons("comments.txt", "positive.txt", "negative.txt", "cfg", "course", [])

    assert created_buttons["Absences"].pos[1] + created_buttons["Absences"].size[1] <= 350
    assert created_buttons["suggestions"].pos[1] < created_buttons["Absences"].pos[1]


def test_filled_desk_can_toggle_absent_visual_state():
    import pygame
    pygame.init()
    import icons

    desk = icons.FilledDesk((0, 0), "Albert", (8, 7), (640, 350), desk_id="R1D1")

    assert desk.is_absent() is False
    assert desk.color_default == icons.YELLOW

    desk.toggle_absent()

    assert desk.is_absent() is True
    assert desk.color_default == icons.WHITE
    assert desk.color == icons.WHITE

    desk.toggle_absent()

    assert desk.is_absent() is False
    assert desk.color_default == icons.YELLOW
    assert desk.color == icons.YELLOW


def test_suggest_focus_button_ignores_absent_students(monkeypatch):
    import pygame
    pygame.init()
    import icons

    present_desk = icons.FilledDesk((0, 0), "Albert", (8, 7), (640, 350), desk_id="R1D1")
    absent_desk = icons.FilledDesk((1, 0), "Gabs", (8, 7), (640, 350), desk_id="R1D2")
    absent_desk.toggle_absent()

    button = icons.SuggestFocusButton((0, 0), (50, 20), [present_desk, absent_desk], "comments.txt", "cfg", "course")

    monkeypatch.setattr(
        icons.linkComments,
        "get_students_needing_comments_from_config_path",
        lambda cfg, course: ["Albert", "Gabs"],
    )

    _, selected_desks = button.clicked(set())

    assert present_desk in selected_desks
    assert absent_desk not in selected_desks


def test_suggest_focus_button_adds_one_more_eligible_student_each_click(monkeypatch):
    import pygame
    pygame.init()
    import icons

    first_desk = icons.FilledDesk((0, 0), "Albert", (8, 7), (640, 350), desk_id="R1D1")
    absent_desk = icons.FilledDesk((1, 0), "Gabs", (8, 7), (640, 350), desk_id="R1D2")
    third_desk = icons.FilledDesk((2, 0), "Marie", (8, 7), (640, 350), desk_id="R1D3")
    absent_desk.toggle_absent()

    button = icons.SuggestFocusButton(
        (0, 0), (50, 20), [first_desk, absent_desk, third_desk], "comments.txt", "cfg", "course"
    )

    monkeypatch.setattr(
        icons.linkComments,
        "get_students_needing_comments_from_config_path",
        lambda cfg, course: ["Albert", "Gabs", "Marie"],
    )

    _, selected_desks = button.clicked(set())
    assert selected_desks == {first_desk}

    _, selected_desks = button.clicked(selected_desks)
    assert selected_desks == {first_desk, third_desk}


def test_class_view_absences_button_marks_student_absent(monkeypatch):
    import pygame
    pygame.init()
    import class_view
    import icons

    created_buttons = {}
    desk = icons.FilledDesk((0, 0), "Albert", (8, 7), (640, 350), desk_id="R1D1")

    class FakeButton(pygame.sprite.Sprite):
        def __init__(self, text):
            super().__init__()
            self.text = text
            self.color_default = (0, 0, 0)
            self.color_selected = (1, 1, 1)
            self.color_unclicked = self.color_default
            self.text_editor_active = False
            self.rect = pygame.Rect(0, 0, 10, 10)

        def update(self, screen):
            pass

    def fake_button(pos, size, text):
        button = FakeButton(text)
        created_buttons[text] = button
        return button

    click_sequence = []

    def fake_handle_mouse_button_down(x, y, sprites, selected_desks):
        click_sequence.append(len(click_sequence))
        if len(click_sequence) == 1:
            return created_buttons["Absences"], selected_desks
        if len(click_sequence) == 2:
            return desk, selected_desks
        return icons.UnclickedDesk(), selected_desks

    event_calls = {"count": 0}

    def fake_event_get():
        event_calls["count"] += 1
        if event_calls["count"] == 1:
            return [SimpleNamespace(type=class_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        if event_calls["count"] == 2:
            return [SimpleNamespace(type=class_view.MOUSEBUTTONDOWN, pos=(0, 0))]
        if event_calls["count"] == 3:
            return [SimpleNamespace(type=class_view.pygame.QUIT)]
        return []

    monkeypatch.setattr(
        class_view.link_gui_backend,
        "setup",
        lambda *args: (
            {"assignments": {"R1D1": "Albert"}, "gui_places": {}, "desks": [], "absent_students": set()},
            (8, 7),
            "comments.txt",
            "positive.txt",
            "negative.txt",
        ),
    )
    monkeypatch.setattr(
        class_view.link_gui_backend,
        "desks_from_seating_state",
        lambda seating_state, width_height_desks: ([desk], (8, 7)),
    )
    monkeypatch.setattr(class_view, "create_text_editor_comment_buttons", lambda *args: [])
    monkeypatch.setattr(class_view.icons, "Button", fake_button)
    monkeypatch.setattr(class_view.events, "handle_mouse_button_down", fake_handle_mouse_button_down)
    monkeypatch.setattr(class_view.pygame.event, "get", fake_event_get)
    monkeypatch.setattr(class_view.pygame.display, "flip", lambda: None)

    screen = SimpleNamespace(fill=lambda *args, **kwargs: None)
    clock = SimpleNamespace(tick=lambda *args, **kwargs: None)
    constants = SimpleNamespace(BACKGROUND=(0, 0, 0), WIDTH_HEIGHT_DESKS=(640, 350))

    class_view.run("config.yaml", "1ma1df01", screen, clock, constants)

    assert desk.is_absent() is True
