from examNotes import *
import students
import os


def test_create_empty_spreadsheet_for_notes(tmp_path):
    student_dict = students.parse_course_list("../example_files/1ma1df01.txt")

    student_codes = list(student_dict.keys())
    question_names = ["q1", "q2"]
    question_marks = [8, 2]
    spreadsheet_file = os.path.join(tmp_path, "testing_empty_spreadsheet_for_notes.xlsx")

    create_empty_spreadsheet_for_student_notes_flat_weights(
        student_codes, question_names, question_marks, spreadsheet_file)

    expected = load_spreadsheet_to_dataframe("../example_files/1ma1df01/empty_for_notes.xlsx")
    actual = load_spreadsheet_to_dataframe(spreadsheet_file)

    assert expected.equals(actual)
