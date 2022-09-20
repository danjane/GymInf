from shredComments import *


def test_findStudents():
    assert find_students("Albert good question", ["Albert"]) == "Albert"
