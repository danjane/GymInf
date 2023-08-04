import radon.complexity
import radon.raw
import radon.metrics
import numpy as np


def analyse_python(py_file):
    with open(py_file, "r") as f:
        code = f.read()

    test = radon.complexity.cc_visit(code)
    num_fns = len(test)
    cs = [f.complexity for f in test]
    fs = [f.name for f in test]

    mi = radon.metrics.mi_visit(code, False)

    test = radon.raw.analyze(code)

    return fs, cs, num_fns, test.lloc, mi


def display(mean, median, std, total_lloc, avg_fn_len, mi_mean):
    print(f"Mean, median and std of ccx: {mean:.2f}, {median:.2f}, {std:.2f}")
    print(f"Average fns maintainability: {mi_mean:.2f}")
    print(f"Total lines of logical code: {total_lloc}")
    print(f"Average length of functions: {avg_fn_len:.2f}")


def analyse(scripts):
    functions = []
    complexities = []
    maintainabilities = []
    total_fns = 0
    total_lloc = 0
    for script in scripts:
        f, c, nf, lloc, mi = analyse_python(script)
        functions += f
        complexities += c
        maintainabilities += [mi]
        total_fns += nf
        total_lloc += lloc

    for f, c in zip(functions, complexities):
        print(f, c)
    print("")

    mean, median, std = [f(complexities) for f in [np.mean, np.median, np.std]]
    mi_mean = np.mean(maintainabilities)
    return mean, median, std, total_lloc, total_lloc/total_fns, mi_mean
