from examNotes import *
import students
import os
import datetime


def test_create_empty_spreadsheet_for_notes(tmp_path):
    student_dict = students.parse_course_list("../example_files/1ma1df01.txt")

    student_codes = list(student_dict.keys())
    question_names = ["q1", "q2"]
    question_marks = [8, 2]
    spreadsheet_file = os.path.join(tmp_path, "testing_empty_spreadsheet_for_notes.xlsx")

    create_empty_spreadsheet_for_student_notes_flat_weights(
        student_codes, question_names, question_marks, spreadsheet_file)

    expected = load_raw_spreadsheet_to_dataframe("../example_files/1ma1df01/empty_for_notes.xlsx")
    actual = load_raw_spreadsheet_to_dataframe(spreadsheet_file)

    assert expected.equals(actual)


def test_read_info_from_filename():
    test_file = "../example_files/1ma1df01/20Apr2020_ExampleExam_Notes.ods"

    exam_date, exam_name = file_info(test_file)
    assert exam_date == datetime.datetime(2020, 4, 20)
    assert exam_name == "ExampleExam"


def test_read_notes_from_filename():
    test_file = "../example_files/1ma1df01/20Apr2020_ExampleExam_Notes.ods"

    data = {"Student": ["albert.enstn", "gabriel.crmr", "marie.cr", "richard.fynmn"],
            "Note": [3, 2.5, 4, 6]}
    expected = pd.DataFrame(data)
    expected.set_index('Student', inplace=True)
    loaded = read_notes_from_filename(test_file)
    assert expected.equals(loaded)


def test_merge_notes_for_one_course():
    exam_folder = "../example_files/1ma1df01/"
    students = ["albert.enstn", "gabriel.crmr", "marie.cr", "richard.fynmn"]

    data = {"Student": ["albert.enstn", "gabriel.crmr", "marie.cr", "richard.fynmn"],
            "20Apr2020": [3, 2.5, 4, 6],
            "20May2020": [3, 4.5, 3, 4]}
    expected = pd.DataFrame(data)
    expected.set_index('Student', inplace=True)

    loaded, exam_names = merge_notes_for_one_course(exam_folder, students)
    assert exam_names == ["ExampleExam", "SecondExam"]
    assert expected.equals(loaded)
