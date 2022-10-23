def latexDeskNode(name, x, y):
    return f"\\node[desk] at ({x}, {y}) {{{name}}};"


def seatingListToLatexDesks(students):
    latex_desks = [latexDeskNode(s, x, 0) for s, x in zip(students, [0, 2.5])]
    return '\n'.join(latex_desks)
