from updateComments import add_positive_comments

comment_test_file = "../example_files/testing_comments.txt"


def check_file_contents(expected_text):
    with open(comment_test_file, 'r') as file:
        file_contents = file.read()
    return file_contents == expected_text


def test_add_positive_comment():
    import os

    if os.path.exists(comment_test_file):
        os.remove(comment_test_file)

    add_positive_comments(comment_test_file, ["Julian", "Dick"])
    assert check_file_contents("+Julian, Dick\n")