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
        notes, exam_names, exam_files = examNotes.merge_notes_for_one_course(exam_folder, list(courses[course].keys()))
        exam_dates = notes.columns
        student_codes = list(courses[course].keys())
        spaces_before_average = 1

        num_exams = len(exam_dates)
        num_students = len(student_codes)

        noted_exams = identify_noted_exams_if_possible(exam_files, cfg)

        worksheet = workbook.add_worksheet(course)
        formats = examNotes.create_workbook_formats(workbook)

        averages = ["NIP", "S1", "S2"]

        num_averages = len(averages)
        weights_nip = [int(first_semester(d)) for d in exam_dates]
        weights_s1 = [int(first_semester(d) & n) for d, n in zip(exam_dates, noted_exams)]
        weights_s2 = [int((not first_semester(d)) & n) for d, n in zip(exam_dates, noted_exams)]
        weights = [weights_nip, weights_s1, weights_s2]

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
                else:
                    worksheet.write(i + row_for_notes, j + 1, -100, formats["red"])

        worksheet.write_row(row_for_notes - 1, num_exams + spaces_before_average + 2, averages)
        worksheet.write_column(row_for_notes, num_exams + spaces_before_average + 1, student_codes)
        for i in range(num_averages):
            weight_range = xlsxwriter.utility.xl_range_abs(i + 2, 1, i + 2, num_exams)
            formula = f'=IF(SUM({weight_range})>0,SUM({weight_range}),1)'
            worksheet.write_formula(row_for_notes - 2, num_exams + spaces_before_average + 2 + i, formula)
            sum_weight_range = xlsxwriter.utility.xl_rowcol_to_cell(
                row_for_notes - 2, num_exams + spaces_before_average + 2 + i, row_abs=True)

            for j in range(num_students):
                note_range = xlsxwriter.utility.xl_range(row_for_notes + j, 1, row_for_notes + j, num_exams)
                formula = f'=SUMPRODUCT({weight_range}, {note_range})/{sum_weight_range}'
                worksheet.write_formula(
                    row_for_notes + j, num_exams + spaces_before_average + 2 + i, formula, formats["round1b"])

        average_range = xlsxwriter.utility.xl_range(
            row_for_notes, num_exams + spaces_before_average + 2, row_for_notes + num_students - 1,
            num_exams + spaces_before_average + 2 + num_averages - 1)
        worksheet.conditional_format(average_range, formats["failing"])

        worksheet.write(row_for_notes - 1, num_exams + 2*spaces_before_average + num_averages + 2,
                        "EOY", formats["round1b"])
        for j in range(num_students):
            s1 = xlsxwriter.utility.xl_rowcol_to_cell(row_for_notes + j, num_exams + spaces_before_average + 3)
            s2 = xlsxwriter.utility.xl_rowcol_to_cell(row_for_notes + j, num_exams + spaces_before_average + 4)
            formula = f'=ROUND(AVERAGE(ROUND({s1}*10)/10, ROUND({s2}*10)/10)*10)/10'
            worksheet.write_formula(
                row_for_notes + j, num_exams + 2*spaces_before_average + num_averages + 2, formula, formats["round1b"])
        worksheet.conditional_format(
            row_for_notes, num_exams + 2 * spaces_before_average + num_averages + 2,
            row_for_notes + num_students - 1, num_exams + 2 * spaces_before_average + num_averages + 2,
            formats["failing"])

    workbook.close()


def identify_noted_exams_if_possible(exam_files, cfg):
    if "noted_exams" in cfg:
        return [f in cfg["noted_exams"] for f in exam_files]
    else:
        return [True] * len(exam_files)