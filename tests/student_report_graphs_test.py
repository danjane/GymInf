from pathlib import Path

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
