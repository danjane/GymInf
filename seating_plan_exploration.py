# Exploration of how to save, load, design and export those pesky seating plans

import config
import linkComments
import os
import students
import random

cfg_real = "/Users/danjane/Documents/Teaching/Classes/Classes2023/config.yaml"
course = "2INDF11"

# TODO This should be a single function... where?
cfg = config.load(cfg_real)
file_path = os.path.join(cfg["courses_path"], course + ".txt")
student_list = list(students.parse_course_list(file_path).values())

with open(cfg["seatingplan_skeleton_path"]) as f:
    latex_skeleton = f.read()

random.shuffle(student_list)
print(student_list)

# Create empty maths class
pair_of_desks = ["FillableDesk", "FillableDesk"]
maths_row = pair_of_desks + ["Space"] + pair_of_desks + ["Space"] + pair_of_desks
maths_desks = [maths_row] * 4
print(maths_desks)

# Create empty info class
row_of_desks = ["EmptyDesk"] + ["FillableDesk"] * 5
info_desks = [row_of_desks] * 4
print(info_desks)


def pretty_print_desks(desk_list):
    for row in desk_list[::-1]:
        print("\t".join(row).replace("Space", "  "))


# Fill up the spaces
def fill_up_spaces(desks, ss):
    ss.reverse()
    new_plan = []
    for i in range(len(desks)):
        row = desks[i]
        new_row = []
        for j in range(len(row)):
            if row[j] == "FillableDesk" and ss:
                new_row.append(ss.pop())
            else:
                new_row.append(row[j])
        new_plan.append(new_row)
    if ss:
        raise RuntimeError("Not enough desks to sit all students!!")
    return new_plan


plan = fill_up_spaces(info_desks, student_list)
pretty_print_desks(plan)


def convert_plan_to_latex(desks):
    def latex_desk(name, x, y):
        if name == "Space":
            return ""
        elif name in ["EmptyDesk", "FillableDesk"]:
            return f"\\node[desk] at ({x}, {y}) {{}};"
        else:
            return f"\\node[desk] at ({x}, {y}) {{{name}}};"

    lines = []

    y = 0
    for row in desks:
        x = 0
        for desk in row:
            lines.append(latex_desk(desk, x, y))
            x += 2
        y += 1.5
    lines = [line for line in lines if len(line) > 0]
    return "\n".join(lines)


desks_for_latex = convert_plan_to_latex(plan)
print(desks_for_latex)

latex_plan = latex_skeleton.replace("DESKS_HERE", desks_for_latex)

output_file = os.path.join(cfg["seatingplan_output_path"], course + ".tex")
print(f"\nWritten to {output_file}")
with open(output_file, 'w') as f:
    f.write(latex_plan)

linkComments.latex_to_pdf(output_file, cfg["seatingplan_output_path"])