import pygame
import constants

pygame.init()

import class_view, control_view


def main(config_file):
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(constants.WIDTH_HEIGHT)
    pygame.display.set_caption("TAT: teacher assisting tools")

    running = True
    course = None
    next_view = "control_view"
    while running:
        if next_view == "quit":
            running = False
        elif next_view == "control_view":
            next_view, course = control_view.run(config_file, course, screen, clock, constants)
        elif next_view == "class_view":
            next_view, course = class_view.run(config_file, course, screen, clock, constants)
        else:
            raise NotImplementedError("This view yet to be seen to!!")

    pygame.quit()


if __name__ == "__main__":
    main("GUI_files/config.yaml")