import os.path
import re
import xlsxwriter
from typing import List, Tuple
import pandas as pd
import datetime


def create_empty_spreadsheet_for_student_notes(student_codes: List[str], question_names: List[str],
                                               question_weights: List[float], question_marks: List[int],
                                               spreadsheet_file: str) -> None:
    num_students = len(student_codes)
    num_questions = len(question_names)
    col_for_total = num_questions + 2
    col_for_unrounded_note = col_for_total + 1
    col_for_note = col_for_unrounded_note + 1
    row_for_students = 5

    workbook = xlsxwriter.Workbook(spreadsheet_file)
    worksheet = workbook.add_worksheet()

    formats = create_workbook_formats(workbook)

    _write_headers(worksheet, question_names, question_weights, question_marks, row_for_students,
                   formats["light_green"])
    _write_student_names_and_empty_cells(worksheet, student_codes, row_for_students, num_questions,
                                         formats["bold"], formats["light_green"])
    _add_formulae_to_calculate_notes(worksheet, num_students, num_questions, row_for_students, col_for_total,
                                     col_for_unrounded_note, col_for_note, formats)

    workbook.close()


def create_workbook_formats(workbook):
    formats = {
        "bold": workbook.add_format({'bold': True}),
        "light_green": workbook.add_format({
            'bg_color': '#C6EFCE',  # light green background
            'font_color': '#006100',  # dark green font
            }),
        "round2": workbook.add_format({'num_format': '0.00'}),
        "round1b": workbook.add_format({'num_format': '0.0', 'bold': True}),
        "red": workbook.add_format({'bg_color': '#FFC7CE'})}
    formats["failing"] = {'type': 'cell', 'criteria': 'between', 'minimum': -100., 'maximum': 3.945, 'format': formats["red"]}
    return formats


def _write_headers(worksheet, question_names, question_weights, question_marks, row_for_students,
                   light_green_format) -> None:
    worksheet.write(0, 0, "Questions")
    worksheet.write_row(0, 1, question_names)
    worksheet.write(1, 0, "Weights")
    worksheet.write_row(1, 1, question_weights, light_green_format)
    worksheet.write(2, 0, "Marks")
    worksheet.write_row(2, 1, question_marks, light_green_format)
    worksheet.write(row_for_students-1, 0, "Student")


def _write_student_names_and_empty_cells(worksheet, student_codes, row_for_students, num_questions, bold, light_green_format) -> None:
    for i, student in enumerate(student_codes):
        worksheet.write(i + row_for_students, 0, student, bold)
        worksheet.write_row(i + row_for_students, 1, [''] * num_questions, light_green_format)


def _add_formulae_to_calculate_notes(worksheet, num_students, num_questions, row_for_students,
                                     col_for_total, col_for_unrounded_note, col_for_note,
                                     formats) -> None:
    worksheet.write(0, col_for_total, "Total", formats["bold"])
    worksheet.write(0, col_for_unrounded_note, "UnroundedNote")
    worksheet.write(0, col_for_note, "Note", formats["bold"])

    row_for_working = row_for_students + num_students + 1
    worksheet.write(row_for_working, 0, "Working")
    for i in range(num_questions):
        weight_cell = xlsxwriter.utility.xl_rowcol_to_cell(1, i + 1)
        mark_cell = xlsxwriter.utility.xl_rowcol_to_cell(2, i + 1)
        formula = f'=IF({mark_cell}>0, {weight_cell}/{mark_cell}, 0)'
        worksheet.write_formula(row_for_working, i + 1, formula, formats["round2"])
    working_range = xlsxwriter.utility.xl_range_abs(row_for_working, 1, row_for_working, num_questions)

    for i in range(num_students):
        mark_range = xlsxwriter.utility.xl_range(i + row_for_students, 1, i + row_for_students, num_questions)
        formula = f'=SUMPRODUCT({mark_range}, {working_range})'
        worksheet.write_formula(i + row_for_students, col_for_total, formula, formats["round2"])
        total_cell = xlsxwriter.utility.xl_rowcol_to_cell(i + row_for_students, col_for_total)
        formula_unrounded = f'=POWER({total_cell},1.3)*4.8+1.3'
        worksheet.write_formula(i + row_for_students, col_for_unrounded_note, formula_unrounded, formats["round2"])
        unrounded_cell = xlsxwriter.utility.xl_rowcol_to_cell(i + row_for_students, col_for_unrounded_note)
        formula_rounded = f'=MAX(1.5, MIN(6, ROUND({unrounded_cell}*2, 0)/2))'
        worksheet.write_formula(i + row_for_students, col_for_note, formula_rounded, formats["round1b"])

    note_range = xlsxwriter.utility.xl_range(row_for_students, col_for_note,
                                             row_for_students + num_students - 1, col_for_note)
    worksheet.conditional_format(note_range, formats["failing"])


def create_empty_spreadsheet_for_student_notes_flat_weights(
        student_codes: List[str], question_names: List[str], question_marks: List[int], spreadsheet_file: str) -> None:
    total_marks = sum(question_marks)
    question_weights = [mark/total_marks for mark in question_marks]
    create_empty_spreadsheet_for_student_notes(
        student_codes, question_names, question_weights, question_marks, spreadsheet_file)
    return None


def load_raw_spreadsheet_to_dataframe(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.ods'):
        df = pd.read_excel(file_path, engine='odf')
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    return df


def file_info(exam_file: str) -> Tuple[datetime.datetime, str]:
    _, file_name = os.path.split(exam_file)
    date_str, exam_name, notes_str, extension = re.split('[_.]', file_name)
    return datetime.datetime.strptime(date_str, "%d%b%Y"), exam_name


def read_notes_from_filename(exam_file: str) -> pd.DataFrame:
    df = load_raw_spreadsheet_to_dataframe(exam_file)
    df = prepare_student_rows(df)
    return df


def prepare_student_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={'Questions': 'Student'})
    df = keep_student_rows(df)
    df = remove_name_after_comma(df)
    df.set_index('Student', inplace=True)
    return df[["Note"]]


def keep_student_rows(df: pd.DataFrame) -> pd.DataFrame:
    def find_first_student():
        key_word = "Student"
        for i, v in enumerate(possible_students):
            if v == key_word:
                return i + 1
        raise LookupError(f"Cannot find key word '{key_word}' in first column of exam file!!")

    def count_students(rest_of_column):
        for i, v in enumerate(rest_of_column):
            if type(v) != str:
                return i
            if v == "Working":
                return i
        raise LookupError(f"Cannot figure out students in first column of exam file!!")

    possible_students = df["Student"]
    first_student_pos = find_first_student()
    num_students = count_students(possible_students[first_student_pos:])
    df = df[first_student_pos:first_student_pos + num_students]
    return df


def remove_name_after_comma(df: pd.DataFrame) -> pd.DataFrame:
    dirty_strings = df["Student"]
    clean_strings = [s.split(",")[0] for s in dirty_strings]
    df["Student"] = clean_strings
    return df


def merge_notes_for_one_course(exam_folder, students):
    exam_files = find_all_exam_files(exam_folder)
    exam_info = [(*file_info(f), os.path.join(exam_folder, f), f) for f in exam_files]
    exam_info.sort(key=lambda x: x[0])
    exam_dates, exam_names, exam_filepaths, exam_files = zip(*exam_info)
    notes = []
    for (f, d) in zip(exam_filepaths, exam_dates):
        n = read_notes_from_filename(f)
        n = n.rename(columns={'Note': d.strftime('%d%b%Y')})
        notes.append(n)
    merged = pd.concat(notes, axis=1)
    loaded = pd.DataFrame(index=students).join(merged)
    return loaded, exam_names, exam_files


def find_all_exam_files(exam_folder):
    files = os.listdir(exam_folder)
    return [f for f in files if
            f.endswith("Notes.ods") or f.endswith("Notes.xlsx") or f.endswith("Notes.xls")]

