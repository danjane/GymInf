import pygame
import updateComments
import linkComments

BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 255, 255)
DARK_BLUE = (0, 100, 100)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
WHITE = (240, 240, 240)

font = pygame.font.SysFont('chalkduster.ttf', 18)


def xy_place_in_desks(place, desk_layout):
    x, y = place // desk_layout[0], place % desk_layout[0]
    print(x, y)
    return x, y


def screen_position_from_xy_and_size(x, y, desk_layout, height_width):
    def rescale(t, real_length, given_length):
        return t * real_length / given_length

    return [rescale(z, r, g) for z, r, g in zip((x, y), height_width, desk_layout)]


def pos_from_place_in_desks(place, desk_layout, height_width):
    return screen_position_from_xy_and_size(*xy_place_in_desks(place, desk_layout),
                                            height_width, desk_layout)


def deltas(xy0, xy1):
    return xy0[0] - xy1[0], xy0[1] - xy1[1]


def distance2(xy0, xy1):
    dx, dy = deltas(xy0, xy1)
    return dx ** 2 + dy ** 2


def nearest_desk(loadsa_desks, xy):
    desks = {d: distance2(d.home, xy) for d in loadsa_desks}
    return min(desks, key=desks.get)


class ParentDesk(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "not these droids"
        self.home = (1e10, 1e10)
        self.sliding = False
        self.is_swapping = False

    def __str__(self):
        return "ParentDesk"

    def update(self, *args, **kwargs):
        pass

    def move(self, *args, **kwargs):
        pass

    def clicked(self, *args, **kwargs):
        pass

    def unclicked(self, *args, **kwargs):
        return UnclickedDesk()

    def bothered(self, other):
        pass

    def unbothered(self):
        pass

    def check_collisions(self, *args, **kwargs):
        return self

    def check_new(self, *args, **kwargs):
        return self

    def append(self, selected_desks):
        return selected_desks


class UnclickedDesk(ParentDesk):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "UnclickedDesk"


class UnselectedDesk(ParentDesk):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "UnselectedDesk"


class Desk(ParentDesk):
    def __init__(self, place, name, desk_layout, height_width):
        super().__init__()
        self.color_default = YELLOW
        self.color = self.color_default
        self.color_selected = LIGHT_BLUE
        self.size = (height_width[0] // desk_layout[0], height_width[1] // desk_layout[1])

        self.pos = screen_position_from_xy_and_size(*place, desk_layout, height_width)
        self.home = self.pos
        self.target_for_sliding = self.pos

        self.name = name
        self.name_img = font.render(name, True, (0, 0, 0))
        self.button_down = False
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.sliding = False
        self.changing_position = False

    def __str__(self):
        return "Desk: " + self.name

    def update(self, surface):
        if self.sliding:
            self.slide()
        self.rect = pygame.Rect(*self.pos, *self.size)
        pygame.draw.rect(surface, self.color, self.rect)
        center_pos = (self.rect.left + self.rect.width // 2, self.rect.top + self.rect.height // 2)
        name_pos = (center_pos[0] - self.name_img.get_width() // 2, center_pos[1] - self.name_img.get_height() // 2)
        surface.blit(self.name_img, name_pos)

    def bothered(self, target):
        self.is_swapping = True
        self.color = ORANGE
        self.target_for_sliding = target.home
        self.sliding = True
        return self

    def unbothered(self):
        self.is_swapping = False
        self.color = self.color_default
        self.target_for_sliding = self.home
        self.sliding = True

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def slide(self):
        dx, dy = deltas(self.target_for_sliding, self.pos)
        if dx ** 2 + dy ** 2 < 36:
            self.pos = self.target_for_sliding
            self.sliding = False
        else:
            self.move(dx / 10, dy / 10)

    def check_collisions(self, desks, selected_desk):
        collisions = pygame.sprite.spritecollide(self, desks, False)
        collisions.remove(self)
        near_desks = [c for c in collisions if not c.sliding]
        # print(near_desks)
        return self.check_new(near_desks, selected_desk, self.pos)

    def check_new(self, desks, selected_desk, xy):
        return nearest_desk([selected_desk] + desks, xy)

    def unclicked(self, other):
        self.button_down = False
        self.sliding = True
        if self.changing_position:
            self.home, other.home = other.home, self.home
            self.target_for_sliding, other.target_for_sliding = self.home, other.home
            other.sliding = True
            self.changing_position = False
            self.color = self.color_default
        return UnclickedDesk()

    @classmethod
    def create_desk(cls, place, name, desk_layout, height_width):
        if name == 'empty':
            return EmptyDesk(place, desk_layout, height_width)
        else:
            return FilledDesk(place, name, desk_layout, height_width)


class FilledDesk(Desk):
    def __init__(self, place, name, desk_layout, height_width):
        super().__init__(place, name, desk_layout, height_width)

    def clicked(self, other):
        self.color = RED
        self.button_down = True
        self.sliding = False
        return self, other

    def append(self, selected_desks):
        if self in selected_desks:
            selected_desks.discard(self)
            self.color = self.color_default
        else:
            selected_desks.add(self)
            self.color = self.color_selected
        return selected_desks


class EmptyDesk(Desk):
    def __init__(self, place, desk_layout, height_width):
        super().__init__(place, "", desk_layout, height_width)
        self.color_default = DARK_BLUE
        self.color = self.color_default
        self.color_selected = self.color_default
        # TODO make the empty desk smaller - will require Desk.pos being center


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text):
        super().__init__()
        self.pos = pos
        self.size = size
        self.color_unclicked = YELLOW
        self.color_clicked = RED
        self.color_default = YELLOW
        self.color_selected = LIGHT_BLUE
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.fade_from_1_to_0 = 0.
        self.name_img = font.render(text, True, (0, 0, 0))
        self.name_pos = self.name_img.get_rect(center=self.rect.center)
        self.text_editor_active = False
        self.text = text
        self.text_rect = self.rect.inflate(-50, -50).move(0, 20)
        self.cursor_visible = True
        self.cursor_blink_interval_millis = 500
        self.cursor_blink_timer = 0

    def update(self, surface):
        self.rect = pygame.Rect(*self.pos, *self.size)
        if self.fade_from_1_to_0 < 0.01:
            color = self.color_unclicked
        else:
            f = self.fade_from_1_to_0
            color = [int(u * (1 - f) + c * f) for u, c in zip(self.color_unclicked, self.color_clicked)]
            self.fade_from_1_to_0 *= 0.95
        pygame.draw.rect(surface, color, self.rect)
        surface.blit(self.name_img, self.name_pos)
        if self.text_editor_active:
            pygame.draw.rect(surface, WHITE, self.text_rect)
            text_img = font.render(self.text, True, (0, 0, 0))
            text_pos = text_img.get_rect(center=self.text_rect.center)
            surface.blit(text_img, text_pos)
            self.draw_cursor(surface, text_pos)

    def draw_cursor(self, surface, text_pos):
        if pygame.time.get_ticks() - self.cursor_blink_timer >= self.cursor_blink_interval_millis:
            self.cursor_visible = not self.cursor_visible
            self.cursor_blink_timer = pygame.time.get_ticks()

        if self.cursor_visible:
            cursor_pos = text_pos.right + 1
            cursor_width = 2
            cursor_rect = pygame.Rect(cursor_pos, text_pos.top, cursor_width, text_pos.height)
            pygame.draw.rect(surface, BLACK, cursor_rect)

    def handle_keydown(self, event, selected_desks):
        self.text_editor_active = True
        if event.key == pygame.K_RETURN:
            self.clicked(selected_desks)
            self.text_editor_active = False
            self.text = ""
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode

    def clicked(self, selected_desks):
        self.fade_from_1_to_0 = 1.
        for desk in selected_desks:
            desk.color = desk.color_default
        return self, set()


class ButtonWithComments(Button):
    def __init__(self, pos, size, text, comments_path):
        super().__init__(pos, size, text)
        self.comments_path = comments_path


class PositiveButton(ButtonWithComments):
    def __init__(self, pos, size, comments_path):
        super().__init__(pos, size, "positive", comments_path)

    def clicked(self, selected_desks):
        updateComments.add_positive_comments(self.comments_path,
                                             [desk.name for desk in selected_desks], self.text)
        super().clicked(selected_desks)
        return UnclickedDesk(), set()


class NegativeButton(ButtonWithComments):
    def __init__(self, pos, size, comments_path):
        super().__init__(pos, size, "negative", comments_path)

    def clicked(self, selected_desks, comment=""):
        updateComments.add_negative_comments(self.comments_path,
                                             [desk.name for desk in selected_desks], comment)
        super().clicked(selected_desks)
        return UnclickedDesk(), set()


class SuggestionsButton(ButtonWithComments):
    def __init__(self, pos, size, desks, comments_path, config_path, course):
        super().__init__(pos, size, "suggestions", comments_path)
        self.desks = desks
        self.config_path = config_path
        self.course = course

    def clicked(self, selected_desks):
        students_for_comments = linkComments.get_students_needing_comments_from_config_path(
            self.config_path, self.course)
        students_for_comments = students_for_comments[:5]
        for desk in selected_desks:
            desk.color = desk.color_default
        selected_desks = set(desk for desk in self.desks if desk.name in students_for_comments)
        for desk in selected_desks:
            desk.color = desk.color_selected
        return UnclickedDesk(), selected_desks
