import pygame
import GUI.constants

pygame.init()

import class_view, control_view

clock = pygame.time.Clock()
screen = pygame.display.set_mode(GUI.constants.WIDTH_HEIGHT)
pygame.display.set_caption("TAT: teacher assisting tools")

config_file = "../GUI_files/config.yaml"

running = True
course = None
next_view = "control_view"
while running:
    if next_view == "quit":
        running = False
    elif next_view == "control_view":
        next_view, course = control_view.run(config_file, course, screen, clock, GUI.constants)
    elif next_view == "class_view":
        next_view, course = class_view.run(config_file, course, screen, clock, GUI.constants)
    else:
        raise NotImplementedError("This view yet to be seen to!!")

pygame.quit()
