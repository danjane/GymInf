import scrapeClassLists


def test_ScrapeClassList():
    assert scrapeClassLists.student_id("dan.jn,,,,,,,,,,,") == "dan.jn"

def test_membre():
    assert scrapeClassLists.is_member("dan.jn,,membre,,,,")