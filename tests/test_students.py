from students import *

c = Students("../example_files/1ma1df01.txt")


def test_oneStudent():
    assert c['albert.enstn'] == "Albert"


def test_givenName():
    assert c['gabriel.crmr'] == "Gabs"


def test_codeToName():
    c, n = code_and_name("dan.jn")
    assert c == "Dan"


def test_codeToGivenName():
    c, n = code_and_name("dan.jn, Danny")
    assert c == "Danny"

