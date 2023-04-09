import os
import pytest
from updateComments import *


@pytest.fixture(scope="function")
def comment_file():
    comment_test_file = "../example_files/testing_comments.txt"
    if os.path.exists(comment_test_file):
        os.remove(comment_test_file)

    yield comment_test_file
    if os.path.exists(comment_test_file):
        os.remove(comment_test_file)


def check_file_contents(test_file, expected_text):
    if expected_text == "":
        return not os.path.exists(test_file)

    with open(test_file, 'r') as file:
        file_contents = file.read()
    return file_contents == expected_text


def test_add_positive_comment(comment_file):
    add_positive_comments(comment_file, ["Julian", "Dick"])
    assert check_file_contents(comment_file, "+Julian, Dick\n")


def test_add_negative_comment(comment_file):
    add_negative_comments(comment_file, ["Julian", "Dick"])
    assert check_file_contents(comment_file, "-Julian, Dick\n")


def test_add_positive_comment_empty(comment_file):
    add_negative_comments(comment_file, [])
    assert check_file_contents(comment_file, "")
