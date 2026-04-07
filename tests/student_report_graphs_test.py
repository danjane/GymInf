from pathlib import Path

import numpy as np
import pandas as pd

import config
import student_report_graphs
import students


EXAMPLE_ROOT = Path(__file__).resolve().parents[1] / "example_files"
EXAMPLE_CONFIG = EXAMPLE_ROOT / "config.yaml"


def test_build_sentiment_graphs_with_no_comments():
    courses = {"1ma1df01": {"EINSTEIN Albert": "Albert"}}
    comments = pd.DataFrame(columns=["Student", "Date", "Course", "Info", "Sentiment", "DNF"])
    graphs = student_report_graphs.build_sentiment_graphs(courses, comments)
    assert "No comment progress data yet" in graphs[("1ma1df01", "EINSTEIN Albert")]


def test_build_exam_graphs_for_example_course():
    cfg = config.load(str(EXAMPLE_CONFIG))
    courses = students.load_class_lists(cfg.courses, [str(path) for path in cfg.class_paths])
    graphs = student_report_graphs.build_exam_graphs(cfg, courses)
    output = graphs[("1ma1df01", "EINSTEIN Albert")]
    assert "Exam results" in output
    assert "20Apr" in output
    assert "4.0" in output


def test_build_student_graphs_returns_both_graph_types():
    cfg = config.load(str(EXAMPLE_CONFIG))
    courses = students.load_class_lists(cfg.courses, [str(path) for path in cfg.class_paths])
    comments = pd.DataFrame(
        {
            "Student": ["EINSTEIN Albert"],
            "Date": pd.to_datetime(["2022-01-13"]),
            "Course": ["1ma1df01"],
            "Info": ["+ Albert"],
            "Sentiment": [1],
            "DNF": [0],
        }
    )
    graphs = student_report_graphs.build_student_graphs(cfg, courses, comments)
    assert ("1ma1df01", "EINSTEIN Albert") in graphs["sentiment"]
    assert ("1ma1df01", "EINSTEIN Albert") in graphs["exam"]


def test_build_exam_graphs_with_missing_exam_directory():
    cfg = config.default_config(EXAMPLE_ROOT / "tmp")
    courses = {"1ma1df01": {"EINSTEIN Albert": "Albert"}}
    graphs = student_report_graphs.build_exam_graphs(cfg, courses)
    assert "No exam results yet" in graphs[("1ma1df01", "EINSTEIN Albert")]


def test_render_comparison_graph_handles_empty_series():
    output = student_report_graphs.render_comparison_graph(np.array([]), 0, [], "Empty")
    assert "No data yet" in output


def test_render_comparison_graph_handles_only_nan_values():
    output = student_report_graphs.render_comparison_graph(np.array([[np.nan], [np.nan]]), 0, ["A", "B"], "NaN")
    assert "No data yet" in output


def test_render_comparison_graph_handles_constant_single_value_series():
    output = student_report_graphs.render_comparison_graph(np.array([[3.0]]), 0, ["Only"], "Constant")
    assert "\\fill[black]" in output
    assert "Constant" in output


def test_render_comparison_graph_uses_sparse_x_ticks_for_long_labels():
    output = student_report_graphs.render_comparison_graph(
        np.array([[1.0], [2.0], [3.0], [4.0], [5.0]]),
        0,
        ["A", "B", "C", "D", "E"],
        "Ticks",
    )
    assert "{A}" in output
    assert "{C}" in output
    assert "{E}" in output
    assert "{B}" not in output


def test_series_path_returns_empty_string_for_no_valid_points():
    output = student_report_graphs._series_path(
        np.array([np.nan, np.nan]),
        "black",
        "1pt",
        0.0,
        1.0,
    )
    assert output == ""


def test_x_tick_positions_empty_labels():
    assert student_report_graphs._x_tick_positions([]) == []
