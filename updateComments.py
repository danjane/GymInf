def add_comments(comments_filename, student_names, prefix):
    with open(comments_filename, "a") as f:
        line = "{}{}\n".format(prefix, ", ".join(student_names))
        f.write(line)


def add_positive_comments(comments_filename, student_names):
    add_comments(comments_filename, student_names, "+")


def add_negative_comments(comments_filename, student_names):
    add_comments(comments_filename, student_names, "-")
