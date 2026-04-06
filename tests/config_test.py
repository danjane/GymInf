import config
import os
from pathlib import Path
import yaml


EXAMPLE_CONFIG = Path(__file__).resolve().parents[1] / "example_files" / "config.yaml"
EXAMPLE_DIR = EXAMPLE_CONFIG.parent
c = config.load(str(EXAMPLE_CONFIG))


def test_load_class():
    assert c.courses == ["1ma1df01", "2ma2dfb01"]


def test_course_path():
    assert c.courses_root == EXAMPLE_DIR


def test_class_paths():
    assert c.class_paths == [EXAMPLE_DIR / "1ma1df01.txt", EXAMPLE_DIR / "2ma2dfb01.txt"]


def test_config_path():
    assert c.config_root == EXAMPLE_DIR


def test_comments_path():
    assert c.comments.comments_file == EXAMPLE_DIR / "comments.txt"


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
    cfg.exams.exam_root = Path(exam_dir)
    config.setup_from_cfg(cfg)
    assert os.path.isdir(exam_dir)


def test_default_structure(tmp_path):
    cfg, _ = create_cfg_file(tmp_path)

    assert os.path.isdir(cfg.config_root)
    assert os.path.isdir(cfg.courses_root)
    assert os.path.isdir(cfg.exams.exam_root)

    assert os.path.isfile(cfg.comments.comments_file)
    assert os.path.isfile(cfg.comments.negative_examples)
    assert os.path.isfile(cfg.comments.positive_examples)
    assert os.path.isfile(cfg.reports.skeleton)
    assert os.path.isfile(cfg.reports.student_outline)


def test_load_resolves_extra_path_fields_relative_to_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        yaml.safe_dump(
            {
                "courses": ["1ma1df01"],
                "courses_path": ".",
                "config_path": ".",
                "comments_path": "comments.txt",
                "exam_path": ".",
                "report_student_path": "report_outline_student.tex",
                "report_skeleton_path": "report_skeleton.tex",
                "seatingplan_skeleton_path": "seatingplan_skeleton.tex",
            }
        )
    )

    cfg = config.load(str(config_file))

    assert cfg.extras["seatingplan_skeleton_path"] == str(tmp_path / "seatingplan_skeleton.tex")


def test_legacy_config_getitem_exposes_core_paths_and_extras(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        yaml.safe_dump(
            {
                "courses": ["1ma1df01"],
                "courses_path": ".",
                "config_path": ".",
                "comments_path": "comments.txt",
                "exam_path": ".",
                "report_student_path": "report_outline_student.tex",
                "report_skeleton_path": "report_skeleton.tex",
                "custom_flag": "enabled",
            }
        )
    )

    cfg = config.load(str(config_file))

    assert cfg["courses"] == ["1ma1df01"]
    assert cfg["comments_path"] == str(tmp_path / "comments.txt")
    assert cfg["custom_flag"] == "enabled"
