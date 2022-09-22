from students import *

c = Students("../example_files/1ma1df01.txt")
courses = loadClassLists("../example_files/config.yaml")


def test_oneStudent():
    assert c['albert.enstn'] == "Albert"


def test_givenName():
    assert c['gabriel.crmr'] == "Gabs"


def test_codeToName():
    code, name = code_and_name("dan.jn")
    assert name == "Dan"
    assert code == "dan.jn"


def test_codeToGivenName():
    code, name = code_and_name("dan.jn, Danny")
    assert name == "Danny"
    assert code == "dan.jn"


def test_loadAllClassesFromConfig():
    assert "1ma1df01" in courses
    assert courses["1ma1df01"]['albert.enstn'] == "Albert"
    assert courses["1ma1df01"]['gabriel.crmr'] == "Gabs"


def test_nameConflict():
    assert not name_conflict({"gabriel.lm": "Gabriel", "gabriel.crmr": "Gabs"})
