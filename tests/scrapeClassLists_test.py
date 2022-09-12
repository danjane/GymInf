import scrapeClassLists


fulltext = """
Membres du groupe rousseau-classe-106
Adresse e-mail,Pseudo,État du groupe,État de l'adresse e-mail,Préférences relatives aux e-mails,Droits de publication,Année d'abonnement,Mois d'abonnement,Jour d'abonnement,Heure d'abonnement,Minute d'abonnement,Seconde d'abonnement,Fuseau horaire
dan.jn@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,13,heure d’été d’Europe centrale
dan.jn2@eduge.ch,,propriétaire,,e-mails,autorisé,2022,8,14,20,0,15,heure d’été d’Europe centrale
dan.jn3@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,20,heure d’été d’Europe centrale
dan.jn4@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,21,heure d’été d’Europe centrale
""".split("\n")

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


def test_ScrapeLinesFull():
    ids = fulltext
    assert scrapeClassLists.student_ids(ids) == ["dan.jn", "dan.jn3", "dan.jn4"]


def test_ClassFileText():
    ids = fulltext
    assert scrapeClassLists.text(ids) == "dan.jn\ndan.jn3\ndan.jn4"
