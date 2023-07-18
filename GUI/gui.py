import pygame
from pygame.locals import *
import constants

pygame.init()

import class_view, control_view

clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.WIDTH_HEIGHT)
pygame.display.set_caption("Teacher assisting tools")

config_file = "../example_files/config_GUI.yaml"

running = True
course = None
next_view = "control_view"
# next_view = "class_view"
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
