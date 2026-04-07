from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

import config
import examNotes


GraphMap = Dict[Tuple[str, str], str]

GRAPH_WIDTH_CM = 12.0
GRAPH_HEIGHT_CM = 4.0
NO_DATA_BOX = r"\fbox{\parbox[c][4cm][c]{0.95\linewidth}{\centering %s}}"


def build_student_graphs(
    cfg: config.AppConfig,
    courses: Dict[str, Dict[str, str]],
    comments_df: pd.DataFrame,
) -> Dict[str, GraphMap]:
    return {
        "sentiment": build_sentiment_graphs(courses, comments_df),
        "exam": build_exam_graphs(cfg, courses),
    }


def build_sentiment_graphs(
    courses: Dict[str, Dict[str, str]],
    comments_df: pd.DataFrame,
) -> GraphMap:
    graphs: GraphMap = {}
    for course, students_in_course in courses.items():
        course_students = list(students_in_course.keys())
        course_df = comments_df[
            (comments_df["Course"] == course) & (comments_df["Sentiment"] != 0)
        ].copy()
        if course_df.empty:
            _fill_missing_graphs(graphs, course, course_students, "No comment progress data yet")
            continue

        course_df["Date"] = pd.to_datetime(course_df["Date"]).dt.normalize()
        dates = pd.date_range(course_df["Date"].min(), course_df["Date"].max(), freq="D")
        weights = np.exp(np.linspace(0, -1, 5))
        signal = np.zeros((len(dates) + len(weights), len(course_students)))
        student_index = {student: index for index, student in enumerate(course_students)}
        date_index = {date: index for index, date in enumerate(dates)}

        for row in course_df.itertuples():
            if row.Student not in student_index:
                continue
            index = date_index[pd.Timestamp(row.Date).normalize()]
            sentiment = 1.0 if row.Sentiment > 0 else -1.0
            signal[index:index + len(weights), student_index[row.Student]] += sentiment * weights

        signal = np.cumsum(signal[:-len(weights)], axis=0)

        for student, index in student_index.items():
            graphs[(course, student)] = render_comparison_graph(
                signal,
                index,
                [date.strftime("%d%b") for date in dates],
                title="Comment progress",
                y_tick_labels=[],
            )
    return graphs


def build_exam_graphs(
    cfg: config.AppConfig,
    courses: Dict[str, Dict[str, str]],
) -> GraphMap:
    graphs: GraphMap = {}
    for course, students_in_course in courses.items():
        course_students = list(students_in_course.keys())
        exam_folder = Path(cfg.exams.exam_root) / course
        if not exam_folder.is_dir():
            _fill_missing_graphs(graphs, course, course_students, "No exam results yet")
            continue

        exam_files = examNotes.find_all_exam_files(str(exam_folder))
        if not exam_files:
            _fill_missing_graphs(graphs, course, course_students, "No exam results yet")
            continue

        notes, _, exam_files = examNotes.merge_notes_for_one_course(str(exam_folder), course_students)
        exam_dates = [examNotes.file_info(exam_file)[0] for exam_file in exam_files]
        ordered_notes = notes.reindex(index=course_students)
        series = ordered_notes.to_numpy(dtype=float)
        labels = [date.strftime("%d%b") for date in exam_dates]

        for index, student in enumerate(course_students):
            graphs[(course, student)] = render_comparison_graph(
                series,
                index,
                labels,
                title="Exam results",
                y_min=1.5,
                y_max=6.0,
                y_tick_labels=[(1.5, "1.5"), (4.0, "4.0"), (6.0, "6.0")],
                reference_lines=[(4.0, "red!60")],
            )
    return graphs


def render_comparison_graph(
    series: np.ndarray,
    highlight_index: int,
    x_labels: List[str],
    title: str,
    y_min: Optional[float] = None,
    y_max: Optional[float] = None,
    y_tick_labels: Optional[List[Tuple[float, str]]] = None,
    reference_lines: Optional[List[Tuple[float, str]]] = None,
) -> str:
    if series.size == 0:
        return NO_DATA_BOX % "No data yet"

    finite_values = series[np.isfinite(series)]
    if finite_values.size == 0:
        return NO_DATA_BOX % "No data yet"

    if y_min is None:
        y_min = float(np.min(finite_values))
    if y_max is None:
        y_max = float(np.max(finite_values))
    if abs(y_max - y_min) < 1e-9:
        y_min -= 1.0
        y_max += 1.0
    else:
        margin = 0.15 * (y_max - y_min)
        y_min -= margin
        y_max += margin

    lines = [
        r"\begin{tikzpicture}[x=1cm,y=1cm]",
        _graph_frame(title),
    ]

    if reference_lines:
        for value, color in reference_lines:
            lines.append(_reference_line(value, color, y_min, y_max))

    for series_index in range(series.shape[1]):
        color = "black" if series_index == highlight_index else "gray!40"
        width = "0.9pt" if series_index == highlight_index else "0.35pt"
        line = _series_path(series[:, series_index], color, width, y_min, y_max)
        if line:
            lines.append(line)

    if y_tick_labels:
        for value, label in y_tick_labels:
            lines.append(_y_tick(value, label, y_min, y_max))

    for x_position, label in _x_tick_positions(x_labels):
        lines.append(
            r"\node[anchor=north, font=\scriptsize] at (%.3f, -0.15) {%s};"
            % (x_position, _latex_escape(label))
        )

    lines.append(r"\end{tikzpicture}")
    return "\n".join(lines)


def _graph_frame(title: str) -> str:
    return "\n".join(
        [
            r"\draw[black] (0,0) rectangle (%.3f, %.3f);" % (GRAPH_WIDTH_CM, GRAPH_HEIGHT_CM),
            r"\node[anchor=west, font=\small\bfseries] at (0, %.3f) {%s};"
            % (GRAPH_HEIGHT_CM + 0.35, _latex_escape(title)),
        ]
    )


def _reference_line(value: float, color: str, y_min: float, y_max: float) -> str:
    y = _scaled_y(value, y_min, y_max)
    return r"\draw[%s, dashed] (0, %.3f) -- (%.3f, %.3f);" % (color, y, GRAPH_WIDTH_CM, y)


def _series_path(values: np.ndarray, color: str, width: str, y_min: float, y_max: float) -> str:
    valid_points = [(index, value) for index, value in enumerate(values) if np.isfinite(value)]
    if not valid_points:
        return ""

    points = [
        "(%.3f, %.3f)" % (_scaled_x(index, len(values)), _scaled_y(value, y_min, y_max))
        for index, value in valid_points
    ]
    if len(points) == 1:
        return r"\fill[%s] %s circle (1.2pt);" % (color, points[0])
    return r"\draw[%s, line width=%s] %s;" % (color, width, " -- ".join(points))


def _scaled_x(index: int, count: int) -> float:
    if count <= 1:
        return GRAPH_WIDTH_CM / 2
    return GRAPH_WIDTH_CM * index / (count - 1)


def _scaled_y(value: float, y_min: float, y_max: float) -> float:
    return GRAPH_HEIGHT_CM * (value - y_min) / (y_max - y_min)


def _y_tick(value: float, label: str, y_min: float, y_max: float) -> str:
    y = _scaled_y(value, y_min, y_max)
    return "\n".join(
        [
            r"\draw (-0.1, %.3f) -- (0, %.3f);" % (y, y),
            r"\node[anchor=east, font=\scriptsize] at (-0.15, %.3f) {%s};"
            % (y, _latex_escape(label)),
        ]
    )


def _x_tick_positions(labels: List[str]) -> Iterable[Tuple[float, str]]:
    if not labels:
        return []
    if len(labels) <= 4:
        indices = list(range(len(labels)))
    else:
        indices = sorted({0, len(labels) // 2, len(labels) - 1})
    return [(_scaled_x(index, len(labels)), labels[index]) for index in indices]


def _fill_missing_graphs(graphs: GraphMap, course: str, students: List[str], message: str) -> None:
    for student in students:
        graphs[(course, student)] = NO_DATA_BOX % message


def _latex_escape(text: str) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    escaped = text
    for before, after in replacements.items():
        escaped = escaped.replace(before, after)
    return escaped
