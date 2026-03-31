import config
import os
from pathlib import Path


EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"
EXAMPLE_DIR = EXAMPLE_CONFIG.parent
c = config.load(str(EXAMPLE_CONFIG))


def test_load_class():
    assert c["courses"] == ["1ma1df01", "2ma2dfb01"]


def test_course_path():
    assert c["courses_path"] == str(EXAMPLE_DIR)


def test_class_paths():
    assert c["class_paths"] == [str(EXAMPLE_DIR / "1ma1df01.txt"), str(EXAMPLE_DIR / "2ma2dfb01.txt")]


def test_config_path():
    assert c["config_path"] == str(EXAMPLE_DIR)


def test_comments_path():
    assert c["comments_path"] == str(EXAMPLE_DIR / "comments.txt")


def test_save_cfg(tmp_path):
    f = os.path.join(tmp_path, "config_saved.yaml")
    config.save(c, f)
    new_c = config.load(f)
    assert c == new_c


def create_cfg_file(path):
    f = os.path.join(path, "config.yaml")
    return config.create_default(f), f


def test_create_default_cfg_file(tmp_path):
    _, f = create_cfg_file(tmp_path)
    assert os.path.isfile(f)


def test_basic_structure_from_cfg_file(tmp_path):
    cfg, _ = create_cfg_file(tmp_path)
    config.setup_from_cfg(cfg)
    exam_dir = os.path.join(tmp_path, "exams")
    assert os.path.isdir(exam_dir)


def test_tweak_structure_from_cfg_file(tmp_path):
    cfg, _ = create_cfg_file(tmp_path)
    exam_dir = os.path.join(tmp_path, "exams2")
    cfg["exam_path"] = exam_dir
    config.setup_from_cfg(cfg)
    assert os.path.isdir(exam_dir)


def test_default_structure(tmp_path):
    cfg, _ = create_cfg_file(tmp_path)

    assert os.path.isdir(cfg["config_path"])
    assert os.path.isdir(cfg["courses_path"])
    assert os.path.isdir(cfg["exam_path"])

    assert os.path.isfile(cfg["comments_path"])
    assert os.path.isfile(cfg["negative_comments_defaults_path"])
    assert os.path.isfile(cfg["positive_comments_defaults_path"])
    assert os.path.isfile(cfg["report_skeleton_path"])
    assert os.path.isfile(cfg["report_student_path"])
