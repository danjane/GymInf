import students


def test_students():
    c = students.Students()
    assert c['albert.enstn'] == "Albert"
