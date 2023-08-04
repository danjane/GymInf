import radon.complexity
import radon.raw
import numpy as np




def analyse_python(py_file):
    with open(py_file, "r") as f:
        code = f.read()

    test = radon.complexity.cc_visit(code)
    num_fns = len(test)
    cs = [f.complexity for f in test]
    fs = [f.name for f in test]

    test = radon.raw.analyze(code)
    return fs, cs, num_fns, test.lloc


def display(mean, median, std, total_lloc, avg_fn_len):
    print(f"Mean, median and std of ccx: {mean:.2f}, {median:.2f}, {std:.2f}")
    print(f"Total lines of logical code: {total_lloc}")
    print(f"Average length of functions: {avg_fn_len:.2f}")


def analyse(scripts):
    functions = []
    complexities = []
    total_fns = 0
    total_lloc = 0
    for script in scripts:
        f, c, nf, lloc = analyse_python(script)
        functions += f
        complexities += c
        total_fns += nf
        total_lloc += lloc

    for f, c in zip(functions, complexities):
        print(f, c)
    print("")

    mean, median, std = [f(complexities) for f in [np.mean, np.median, np.std]]
    return mean, median, std, total_lloc, total_lloc/total_fns
