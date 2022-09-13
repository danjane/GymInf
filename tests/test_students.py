import students

c = students.Students("../example_files/1ma1df01.txt")


def test_oneStudent():
    assert c['albert.enstn'] == "Albert"


def test_givenName():
    assert c['gabriel.crmr'] == "Gabs"


def test_codeToName():
    assert students.code_and_name("dan.jn") == "Dan"
