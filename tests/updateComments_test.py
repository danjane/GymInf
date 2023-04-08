from updateComments import *

comment_test_file = "../example_files/testing_comments.txt"


def check_file_contents(file_path, expected_text):
    with open(file_path, 'r') as file:
        file_contents = file.read()
    return file_contents == expected_text


def test_add_positive_comment():
    updateComments.add_positive_comments(comment_test_file, ["Julian", "Dick"])
    assert check_file_contents("+Julian, Dick\n")