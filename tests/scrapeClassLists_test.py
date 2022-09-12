import scrapeClassLists


def test_ScrapeClassList():
    assert scrapeClassLists.student_id("dan.jn,,,,,,,,,,,") == "dan.jn"


def test_IsMembre():
    assert scrapeClassLists.is_member("dan.jn,,membre,,,,")


def test_ScrapeLinesSimple():
    ids = scrapeClassLists.student_ids([
        "dan.jn,,membre,,,,",
        "dan.jn,,membre,,,,",
        "dan.jn,,prop,,,,"
    ])
    assert ids == ["dan.jn", "dan.jn"]