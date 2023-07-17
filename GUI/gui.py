import pygame
from pygame.locals import *
import constants

pygame.init()

import class_view, control_view

clock = pygame.time.Clock()
screen = pygame.display.set_mode(constants.WIDTH_HEIGHT)

config_file, course = "../example_files/config_GUI.yaml", "2ma2dfb01"

running = True
next_view = "control_view"
while running:
    if next_view == "quit":
        running = False
    elif next_view == "control_view":
        next_view, course = control_view.run(config_file, screen, clock, constants)
    elif next_view == "class_view":
        next_view = class_view.run(config_file, course, screen, clock, constants)

pygame.quit()
