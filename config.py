from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union
import os
import sys

import yaml


def adjust_path_for_cxfreeze(path):
    working_dir, _ = os.path.split(sys.executable)
    return os.path.join(working_dir, path)


def cx(filename):
    cxfreeze_executable_flag = getattr(sys, "frozen", False)
    if cxfreeze_executable_flag:
        return filename
    return filename


@dataclass(eq=True)
class ReportPaths:
    skeleton: Path
    student_outline: Path
    tex_output: Optional[Path] = None


@dataclass(eq=True)
class ExamConfig:
    exam_root: Path
    averages_output: Optional[Path] = None
    noted_exams: list[str] = field(default_factory=list)


@dataclass(eq=True)
class CommentDefaults:
    comments_file: Path
    positive_examples: Optional[Path] = None
    negative_examples: Optional[Path] = None


@dataclass(eq=True)
class AppConfig:
    courses: list[str]
    courses_root: Path
    config_root: Path
    reports: ReportPaths
    exams: ExamConfig
    comments: CommentDefaults
    latex_path: Optional[Path] = None
    rg_class: Any = None
    extras: dict[str, Any] = field(default_factory=dict)

    def class_list_path(self, course: str) -> Path:
        return self.courses_root / f"{course}.txt"

    @property
    def class_paths(self) -> list[Path]:
        return [self.class_list_path(course) for course in self.courses]

    def with_updated_courses(self, courses: list[str]) -> "AppConfig":
        return AppConfig(
            courses=courses,
            courses_root=self.courses_root,
            config_root=self.config_root,
            reports=self.reports,
            exams=self.exams,
            comments=self.comments,
            latex_path=self.latex_path,
            rg_class=self.rg_class,
            extras=dict(self.extras),
        )

    def to_dict(self) -> dict[str, Any]:
        data = {
            "courses": self.courses,
            "courses_path": str(self.courses_root),
            "config_path": str(self.config_root),
            "comments_path": str(self.comments.comments_file),
            "exam_path": str(self.exams.exam_root),
            "report_student_path": str(self.reports.student_outline),
            "report_skeleton_path": str(self.reports.skeleton),
            "rg_class": self.rg_class,
        }
        if self.exams.averages_output is not None:
            data["exam_averages_path"] = str(self.exams.averages_output)
        if self.comments.positive_examples is not None:
            data["positive_comments_defaults_path"] = str(self.comments.positive_examples)
        if self.comments.negative_examples is not None:
            data["negative_comments_defaults_path"] = str(self.comments.negative_examples)
        if self.reports.tex_output is not None:
            data["report_tex_path"] = str(self.reports.tex_output)
        if self.latex_path is not None:
            data["latex_path"] = str(self.latex_path)
        if self.exams.noted_exams:
            data["noted_exams"] = self.exams.noted_exams
        data.update(self.extras)
        return data

    def __getitem__(self, key: str):
        legacy_values = {
            "courses": self.courses,
            "courses_path": str(self.courses_root),
            "config_path": str(self.config_root),
            "class_paths": [str(path) for path in self.class_paths],
            "comments_path": str(self.comments.comments_file),
            "positive_comments_defaults_path": str(self.comments.positive_examples) if self.comments.positive_examples else None,
            "negative_comments_defaults_path": str(self.comments.negative_examples) if self.comments.negative_examples else None,
            "exam_path": str(self.exams.exam_root),
            "exam_averages_path": str(self.exams.averages_output) if self.exams.averages_output else None,
            "report_skeleton_path": str(self.reports.skeleton),
            "report_student_path": str(self.reports.student_outline),
            "report_tex_path": str(self.reports.tex_output) if self.reports.tex_output else None,
            "latex_path": str(self.latex_path) if self.latex_path else None,
            "noted_exams": self.exams.noted_exams,
            "rg_class": self.rg_class,
        }
        if key in legacy_values:
            return legacy_values[key]
        return self.extras[key]


def resolve_path(base_dir: Path, path: Optional[str]) -> Optional[Path]:
    if path is None:
        return None
    path_obj = Path(cx(path))
    if path_obj.is_absolute():
        return path_obj
    return (base_dir / path_obj).resolve()


def load(filename: str) -> AppConfig:
    filename = cx(filename)
    config_file = Path(filename).resolve()
    base_dir = config_file.parent
    with open(config_file, "r") as f:
        raw_config = yaml.safe_load(f) or {}

    known_keys = {
        "courses",
        "courses_path",
        "config_path",
        "comments_path",
        "exam_path",
        "exam_averages_path",
        "positive_comments_defaults_path",
        "negative_comments_defaults_path",
        "latex_path",
        "report_skeleton_path",
        "report_student_path",
        "report_tex_path",
        "noted_exams",
        "rg_class",
    }
    extras = {k: v for k, v in raw_config.items() if k not in known_keys}

    return AppConfig(
        courses=list(raw_config.get("courses", [])),
        courses_root=resolve_path(base_dir, raw_config.get("courses_path")) or base_dir,
        config_root=resolve_path(base_dir, raw_config.get("config_path")) or base_dir,
        reports=ReportPaths(
            skeleton=resolve_path(base_dir, raw_config.get("report_skeleton_path")) or base_dir / "report_skeleton.tex",
            student_outline=resolve_path(base_dir, raw_config.get("report_student_path")) or base_dir / "report_outline_student.tex",
            tex_output=resolve_path(base_dir, raw_config.get("report_tex_path")),
        ),
        exams=ExamConfig(
            exam_root=resolve_path(base_dir, raw_config.get("exam_path")) or base_dir / "exams",
            averages_output=resolve_path(base_dir, raw_config.get("exam_averages_path")),
            noted_exams=list(raw_config.get("noted_exams", [])),
        ),
        comments=CommentDefaults(
            comments_file=resolve_path(base_dir, raw_config.get("comments_path")) or base_dir / "comments.txt",
            positive_examples=resolve_path(base_dir, raw_config.get("positive_comments_defaults_path")),
            negative_examples=resolve_path(base_dir, raw_config.get("negative_comments_defaults_path")),
        ),
        latex_path=resolve_path(base_dir, raw_config.get("latex_path")),
        rg_class=raw_config.get("rg_class"),
        extras=extras,
    )


def mkdir_if_nec(path: Union[Path, str]):
    path = Path(path)
    if not path.is_dir():
        path.mkdir()


def save(cfg: AppConfig, filename):
    with open(cx(filename), "w") as f:
        yaml.safe_dump(cfg.to_dict(), f, sort_keys=False)


def update_courses_in_yaml(filename, courses):
    cfg = load(filename)
    save(cfg.with_updated_courses(courses), filename)


def default_config(base_path) -> AppConfig:
    base_path = Path(base_path)
    return AppConfig(
        courses=[],
        courses_root=base_path,
        config_root=base_path,
        reports=ReportPaths(
            skeleton=base_path / "latex" / "report_skeleton.tex",
            student_outline=base_path / "latex" / "report_outline_student.tex",
            tex_output=base_path / "latex" / "report.tex",
        ),
        exams=ExamConfig(
            exam_root=base_path / "exams",
            averages_output=base_path / "exams" / "big_dump.xlsx",
        ),
        comments=CommentDefaults(
            comments_file=base_path / "comments.txt",
            positive_examples=base_path / "positive_comments_examples.txt",
            negative_examples=base_path / "negative_comments_examples.txt",
        ),
        latex_path=base_path / "latex",
    )


def setup_from_cfg(cfg: AppConfig):
    folders = [cfg.config_root, cfg.courses_root, cfg.exams.exam_root]
    if cfg.latex_path is not None:
        folders.append(cfg.latex_path)
    for folder in folders:
        mkdir_if_nec(folder)

    cfg.comments.comments_file.write_text("")
    if cfg.comments.positive_examples is not None:
        cfg.comments.positive_examples.write_text("correct response\ngood question\nTN for Pythag\nquick work")
    if cfg.comments.negative_examples is not None:
        cfg.comments.negative_examples.write_text("DNF\nChatting")
    cfg.reports.skeleton.write_text("\\documentclass[11pt]{article}\n\\begin{document}\nSTUDENTPAGES\n\\end{document}")
    cfg.reports.student_outline.write_text(
        "STUDENTCODE \\hfill \\textbf{STUDENTNAME} \\hfill COURSE \\\\ \nSTUDENTCOMMENTS"
    )


def create_default(f):
    base_path = Path(f).parent
    mkdir_if_nec(base_path)
    cfg = default_config(base_path)
    setup_from_cfg(cfg)
    save(cfg, f)
    return cfg


def create_default_if_nec(f):
    if not Path(f).is_file():
        create_default(f)
