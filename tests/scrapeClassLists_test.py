import os
from scrapeClassLists import *

fulltext = """
Membres du groupe rousseau-classe-106
Adresse e-mail,Pseudo,État du groupe,État de l'adresse e-mail,Préférences relatives aux e-mails," / 
"Droits de publication,Année d'abonnement,Mois d'abonnement,Jour d'abonnement,Heure d'abonnement," /
"Minute d'abonnement,Seconde d'abonnement,Fuseau horaire
dan.jn@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,13,heure d’été d’Europe centrale
dan.jn2@eduge.ch,,propriétaire,,e-mails,autorisé,2022,8,14,20,0,15,heure d’été d’Europe centrale
dan.jn3@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,20,heure d’été d’Europe centrale
dan.jn4@eduge.ch,,membre,,e-mails,autorisé,2022,8,14,20,0,21,heure d’été d’Europe centrale
""".split("\n")


def test_ScrapeClassList():
    assert student_code("dan.jn,,,,,,,,,,,") == "dan.jn"


def test_IsMembre():
    assert is_member("dan.jn,,membre,,,,")


def test_ScrapeLinesSimple():
    ids = student_codes([
        "dan.jn,,membre,,,,",
        "dan.jn,,membre,,,,",
        "dan.jn,,prop,,,,"
    ])
    assert ids == ["dan.jn", "dan.jn"]


def test_ScrapeLinesAlphabetic():
    ids = student_codes([
        "dan.jnb,,membre,,,,",
        "dan.jna,,membre,,,,",
        "dan.jn,,prop,,,,"
    ])
    assert ids == ["dan.jna", "dan.jnb"]


def test_ScrapeLinesFull():
    ids = fulltext
    assert student_codes(ids) == ["dan.jn", "dan.jn3", "dan.jn4"]


def test_LoadAndScrape():
    string = scrape_file("../example_files/GoogleGroupMembersDump.txt")
    assert string == ["marie.cr", "gabriel.crmr", "albert.enstn", "richard.fynmn"]


def test_outputFileName():
    assert outFileName("rousseau-classe-106.csv") == "rg106.txt"
    assert outFileName("rousseau-cours-1ma1dfb08.csv") == "1ma1dfb08.txt"


def test_fullpaths():
    dump_file = "rousseau-classe-106.csv"
    in_path = os.path.join("C:", "test", "dump")
    out_path = os.path.join("C:", "Control")
    in_file, out_file = file_paths(dump_file, in_path, out_path)
    assert in_file == "C:/test/dump/rousseau-classe-106.csv"
    assert out_file == "C:/Control/rg106.txt"
