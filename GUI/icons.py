import pygame

BLACK = (0, 0, 0)
LIGHT_BLUE = (0, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)

font = pygame.font.SysFont('chalkduster.ttf', 36)

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
    return dx**2 + dy**2


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
        self.color = YELLOW
        self.size = (height_width[0]//desk_layout[0], height_width[1]//desk_layout[1])

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
        surface.blit(self.name_img, self.pos)

    def clicked(self):
        self.color = RED
        self.button_down = True
        self.sliding = False

    def unclicked(self, other):
        self.button_down = False
        self.color = YELLOW
        self.sliding = True
        if self.changing_position:
            self.home, other.home = other.home, self.home
            self.target_for_sliding, other.target_for_sliding = self.home, other.home
            other.sliding = True
            self.changing_position = False
        return UnclickedDesk()

    def bothered(self, target):
        self.is_swapping = True
        self.color = ORANGE
        self.target_for_sliding = target.home
        self.sliding = True
        return self

    def unbothered(self):
        self.is_swapping = False
        self.color = YELLOW
        self.target_for_sliding = self.home
        self.sliding = True

    def move(self, dx, dy):
        self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def slide(self):
        dx, dy = deltas(self.target_for_sliding, self.pos)
        if dx**2 + dy**2 < 36:
            self.pos = self.target_for_sliding
            self.sliding = False
        else:
            self.move(dx/8, dy/8)

    def check_collisions(self, desks, selected_desk):
        collisions = pygame.sprite.spritecollide(self, desks, False)
        collisions.remove(self)
        near_desks = [c for c in collisions if not c.sliding]
        # print(near_desks)
        return self.check_new(near_desks, selected_desk, self.pos)

    def check_new(self, desks, selected_desk, xy):
        return nearest_desk([selected_desk] + desks, xy)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, size, text):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.size = size

        self.color_unclicked = YELLOW
        self.color_clicked = RED
        self.rect = pygame.Rect(*self.pos, *self.size)
        self.fade_from_1_to_0 = 0.

        self.name_img = font.render(text, True, (0, 0, 0))
        self.name_pos = self.name_img.get_rect(center=self.rect.center)

    def update(self, surface):
        self.rect = pygame.Rect(*self.pos, *self.size)
        if self.fade_from_1_to_0 < 0.01:
            color = self.color_unclicked
        else:
            f = self.fade_from_1_to_0
            color = [u*(1-f) + c*f for u, c in zip(self.color_unclicked, self.color_clicked)]
            self.fade_from_1_to_0 = f * 0.95

        pygame.draw.rect(surface, color, self.rect)
        surface.blit(self.name_img, self.name_pos)

    def clicked(self):
        self.fade_from_1_to_0 = 1
