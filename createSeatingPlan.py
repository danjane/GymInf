def latexDeskNode(name, x, y):
    return f"\\node[desk] at ({x}, {y}) {{{name}}};"


def latexDeskPositionsSixByFourStandard(num_students):
    num_rows = (num_students - 1) // 6 + 1
    xs = [0, 2, 5, 7, 10, 12] * num_rows
    ys = []
    for row in range(num_rows):
        ys += [row*4]*6
    xs = xs[:num_students]
    ys = ys[:num_students]
    return xs, ys


def seatingListToLatexDesks(students):
    xs, ys = latexDeskPositionsSixByFourStandard(len(students))
    latex_desks = [latexDeskNode(s, x, y) for s, x, y in zip(students, xs, ys)]
    return '\n'.join(latex_desks)
