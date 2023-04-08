def add_positive_comments(comments_filename, student_names):
    with open(comments_filename, "a") as f:
        line = "+{}\n".format(", ".join(student_names))
        f.write(line)
