import pygame
import constants
import logging
from pathlib import Path
import traceback

pygame.init()

import class_view, control_view, seating_plan_view


LOG_FILE = Path(__file__).resolve().parent / "gui_debug.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def main(config_file):
    logging.info("gui.main start config_file=%s", config_file)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(constants.WIDTH_HEIGHT)
    pygame.display.set_caption("TAT: teacher assisting tools")

    running = True
    course = None
    next_view = "control_view"
    try:
        while running:
            logging.info("gui.main loop next_view=%s course=%s", next_view, course)
            if next_view == "quit":
                logging.info("gui.main received quit transition")
                running = False
            elif next_view == "control_view":
                next_view, course = control_view.run(config_file, course, screen, clock, constants)
            elif next_view == "class_view":
                next_view, course = class_view.run(config_file, course, screen, clock, constants)
            elif next_view == "seating_plan_view":
                next_view, course = seating_plan_view.run(config_file, course, screen, clock, constants)
            else:
                logging.error("gui.main unknown next_view=%s", next_view)
                raise NotImplementedError("This view yet to be seen to!!")
    except Exception:
        logging.exception("Unhandled exception in gui.main")
        raise
    finally:
        logging.info("gui.main shutting down pygame")
        pygame.quit()
        logging.info("gui.main finished")


if __name__ == "__main__":
    main("GUI_files/config.yaml")
