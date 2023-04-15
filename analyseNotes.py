import examNotes
import xlsxwriter
import linkComments
import os
import datetime


def first_semester(date_string):
    date = datetime.datetime.strptime(date_string, "%d%b%Y")
    if date.month < 6:
        current_year = date.year
    else:
        current_year = date.year + 1
    jan31 = datetime.datetime(current_year, 1, 20)
    return date < jan31


def dump_all(cfg_path, output_file):
    cfg, courses, df = linkComments.load_data_from_config_path(cfg_path)

    workbook = xlsxwriter.Workbook(output_file)

    for course in courses.keys():
        exam_folder = os.path.join(cfg["exam_path"], course)
        notes, exam_names = examNotes.merge_notes_for_one_course(exam_folder, list(courses[course].keys()))
        exam_dates = notes.columns
        student_codes = list(courses[course].keys())

        num_exams = len(exam_dates)
        num_students = len(student_codes)

        worksheet = workbook.add_worksheet(course)

        averages = ["NIP", "S1", "S2"]

        num_averages = len(averages)
        weights_s1 = [int(first_semester(d)) for d in exam_dates]
        weights_s2 = [int(not first_semester(d)) for d in exam_dates]
        weights = [weights_s1] * 2 + [weights_s2]

        headers = ["Date", "Name"] + [h + " weight" for h in averages]

        worksheet.write_column(0, 0, headers)
        worksheet.write_row(0, 1, exam_dates)
        worksheet.write_row(1, 1, exam_names)
        for i in range(num_averages):
            worksheet.write_row(2+i, 1, weights[i])

        row_for_notes = len(headers) + 1
        for i, student_code in enumerate(student_codes):
            worksheet.write(i+row_for_notes, 0, student_code)
            for j, note in enumerate(notes.loc[student_code]):
                if note > 0:
                    worksheet.write(i+row_for_notes, j+1, note)

        worksheet.write_row(row_for_notes - 1, num_exams + 2, averages)
        for i in range(num_averages):
            weight_range = xlsxwriter.utility.xl_range_abs(i + 2, 1, i + 2, num_exams)
            formula = f'=IF(SUM({weight_range})>0,SUM({weight_range}),1)'
            worksheet.write_formula(row_for_notes - 2, num_exams + 2 + i, formula)
            sum_weight_range = xlsxwriter.utility.xl_rowcol_to_cell(row_for_notes - 2, num_exams + 2 + i, row_abs=True)

            for j in range(num_students):
                note_range = xlsxwriter.utility.xl_range(row_for_notes + j, 1, row_for_notes + j, num_exams)
                formula = f'=SUMPRODUCT({weight_range}, {note_range})/{sum_weight_range}'
                worksheet.write_formula(row_for_notes + j, num_exams + 2 + i, formula)

    workbook.close()
