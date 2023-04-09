import os
import pytest
from updateComments import add_positive_comments


@pytest.fixture
def comment_file():
    comment_test_file = "../example_files/testing_comments.txt"
    if os.path.exists(comment_test_file):
        os.remove(comment_test_file)

    yield comment_test_file
    os.remove(comment_test_file)


def check_file_contents(test_file, expected_text):
    with open(test_file, 'r') as file:
        file_contents = file.read()
    return file_contents == expected_text


def test_add_positive_comment(comment_file):
    add_positive_comments(comment_file, ["Julian", "Dick"])
    assert check_file_contents(comment_file, "+Julian, Dick\n")
