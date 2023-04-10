import os
import config
import desk_functions
from datetime import datetime
from typing import Dict


def start_new_day(cfg: Dict, course: str):
    file_path = cfg["comments_path"]
    today = datetime.today().strftime('%d%b%Y').lower()
    with open(file_path, 'a') as f:
        f.write(f"\nd{today}\nc{course}\n")


def setup(cfg_path: str, course: str):
    cfg = config.load(cfg_path)
    start_new_day(cfg, course)

    file_path = os.path.join(cfg["courses_path"], course + ".txt")
    seating_plan = desk_functions.load_basic_seating_plan_from_file(file_path)
    desk_layout = max(v[0] for v in seating_plan.values()) + 1, max(v[1] for v in seating_plan.values()) + 1
    return seating_plan, desk_layout
