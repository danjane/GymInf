def add_comments(comments_filename, student_names, prefix, comment=""):
    if len(comment) > 0:
        comment = " " + comment
    if student_names:
        with open(comments_filename, "a") as f:
            line = "{}{}{}\n".format(prefix, ", ".join(student_names), comment)
            f.write(line)


def add_positive_comments(comments_filename, student_names, comment=""):
    add_comments(comments_filename, student_names, "+", comment)


def add_negative_comments(comments_filename, student_names, comment=""):
    add_comments(comments_filename, student_names, "-", comment)
