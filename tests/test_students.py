import students

c = students.Students()


def test_oneStudent():
    assert c['albert.enstn'] == "Albert"


def test_givenName():
    assert c['gabriel.crmr'] == "Gabs"
