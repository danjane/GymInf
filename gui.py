import pygame
import constants
import logging
import os
from pathlib import Path

import class_view
import control_view
import seating_plan_view


LOG_FILE = Path(__file__).resolve().parent / "gui_debug.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def initialize_pygame():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(constants.WIDTH_HEIGHT)
    pygame.display.set_caption("TAT: teacher assisting tools")
    return screen, clock


def run_view(next_view, config_file, course, screen, clock):
    if next_view == "quit":
        logging.info("gui.main received quit transition")
        return None, course
    view_runners = {
        "control_view": control_view.run,
        "class_view": class_view.run,
        "seating_plan_view": seating_plan_view.run,
    }
    try:
        view_runner = view_runners[next_view]
    except KeyError as exc:
        logging.error("gui.main unknown next_view=%s", next_view)
        raise NotImplementedError("This view yet to be seen to!!") from exc
    return view_runner(config_file, course, screen, clock, constants)


def main(config_file):
    logging.info("gui.main start config_file=%s", config_file)
    screen, clock = initialize_pygame()

    course = None
    next_view = "control_view"
    try:
        while next_view:
            logging.info("gui.main loop next_view=%s course=%s", next_view, course)
            next_view, course = run_view(next_view, config_file, course, screen, clock)
    except Exception:
        logging.exception("Unhandled exception in gui.main")
        raise Exception
    finally:
        logging.info("gui.main shutting down pygame")
        pygame.quit()
        logging.info("gui.main finished")


def run_script(config_file="GUI_files/config.yaml"):
    try:
        main(config_file)
    finally:
        logging.shutdown()
    # On some local macOS setups pygame exits cleanly from Python but the
    # interpreter/SDL teardown still crashes afterward. Use a hard process
    # exit only for direct script execution.
    os._exit(0)


if __name__ == "__main__":
    run_script()
