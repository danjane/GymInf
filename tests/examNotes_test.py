from examNotes import *
import analyseNotes
import config
import students
import os
import datetime
from pathlib import Path

EXAMPLE_FILES = Path(__file__).resolve().parents[1] / "example_files"
EXAM_FILES = EXAMPLE_FILES / "1ma1df01"


def test_create_empty_spreadsheet_for_notes(tmp_path):
    student_dict = students.parse_course_list(str(EXAMPLE_FILES / "1ma1df01.txt"))

    student_codes = list(student_dict.keys())
    question_names = ["q1", "q2"]
    question_marks = [8, 2]
    spreadsheet_file = os.path.join(tmp_path, "testing_empty_spreadsheet_for_notes.xlsx")

    create_empty_spreadsheet_for_student_notes_flat_weights(
        student_codes, question_names, question_marks, spreadsheet_file)

    expected = load_raw_spreadsheet_to_dataframe(str(EXAM_FILES / "empty_for_notes.xlsx"))
    actual = load_raw_spreadsheet_to_dataframe(spreadsheet_file)

    assert expected.equals(actual)


def test_read_info_from_filename():
    test_file = str(EXAM_FILES / "20Apr2020_ExampleExam_Notes.ods")

    exam_date, exam_name = file_info(test_file)
    assert exam_date == datetime.datetime(2020, 4, 20)
    assert exam_name == "ExampleExam"


def test_read_notes_from_filename():
    test_file = str(EXAM_FILES / "20Apr2020_ExampleExam_Notes.ods")

    data = {"Student": ["EINSTEIN Albert", "CRAMER Gabriel", "CURIE Marie", "FEYNMANN Richard"],
            "Note": [3, 2.5, 4, 6]}
    expected = pd.DataFrame(data)
    expected.set_index('Student', inplace=True)
    loaded = read_notes_from_filename(test_file)
    assert expected.equals(loaded)


def test_merge_notes_for_one_course():
    exam_folder = str(EXAM_FILES)
    student_codes = ["EINSTEIN Albert", "CRAMER Gabriel", "CURIE Marie", "FEYNMANN Richard"]
    loaded, exam_names, exam_files = merge_notes_for_one_course(exam_folder, student_codes)

    data = {"Student": ["EINSTEIN Albert", "CRAMER Gabriel", "CURIE Marie", "FEYNMANN Richard"],
            "20Apr2020": [3, 2.5, 4, 6],
            "20May2020": [3, 4.5, 3, 4]}
    expected = pd.DataFrame(data)
    expected.set_index('Student', inplace=True)

    assert exam_names == ("ExampleExam", "SecondExam")
    assert expected.equals(loaded)
    # TODO check exam_files


def test_dump_all(tmp_path):
    expected_file = str(EXAMPLE_FILES / "dump_of_all_notes.xlsx")
    spreadsheet_file = os.path.join(tmp_path, "testing_empty_spreadsheet_for_notes.xlsx")
    cfg_path = str(EXAMPLE_FILES / "config.yaml")
    analyseNotes.dump_all(cfg_path, spreadsheet_file)

    expected = load_raw_spreadsheet_to_dataframe(expected_file)
    actual = load_raw_spreadsheet_to_dataframe(spreadsheet_file)

    assert expected.equals(actual)


def test_dump_all_respects_noted_exams(tmp_path):
    cfg_path = EXAMPLE_FILES / "config.yaml"
    cfg = config.load(str(cfg_path))
    cfg["noted_exams"] = ["20Apr2020_ExampleExam_Notes.ods"]

    custom_cfg_path = tmp_path / "config_noted.yaml"
    spreadsheet_file = tmp_path / "noted_dump.xlsx"
    config.save(cfg, str(custom_cfg_path))

    analyseNotes.dump_all(str(custom_cfg_path), str(spreadsheet_file))
    actual = load_raw_spreadsheet_to_dataframe(str(spreadsheet_file))

    s2_weight_row = actual[actual["Date"] == "S2 weight"].iloc[0]
    assert [s2_weight_row["20Apr2020"], s2_weight_row["20May2020"]] == [1, 0]

    student_row = actual[actual["Date"] == "EINSTEIN Albert"].iloc[0]
    assert [student_row["20Apr2020"], student_row["20May2020"]] == [3, 3]
