import scrapeClassLists


def test_ScrapeClassList():
    assert scrapeClassLists.student_id("dan.jn,,,,,,,,,,,") == "dan.jn"
