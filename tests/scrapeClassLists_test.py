from scrapeClassLists import *
from pathlib import Path
import sys

EXAMPLE_FILES = Path(__file__).resolve().parents[1] / "example_files"

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
    string = scrape_file(str(EXAMPLE_FILES / "GoogleGroupMembersDump.txt"))
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


def test_text_joins_codes_with_newlines():
    output = text([
        "dan.jnb,,membre,,,,",
        "dan.jna,,membre,,,,",
    ])
    assert output == "dan.jna\ndan.jnb"


def test_write_codes_and_load_scrape_write(tmp_path):
    input_file = tmp_path / "rousseau-classe-106.csv"
    output_file = tmp_path / "rg106.txt"
    input_file.write_text("\n".join([
        "dan.jna,,membre,,,,",
        "dan.jnb,,membre,,,,",
        "dan.jnc,,proprietaire,,,,",
    ]))

    load_scrape_write(str(input_file), str(output_file))

    assert output_file.read_text() == "dan.jna\ndan.jnb"


def test_main_creates_output_directory_and_files(tmp_path, monkeypatch):
    input_dir = tmp_path / "in"
    output_dir = tmp_path / "out"
    input_dir.mkdir()
    (input_dir / "rousseau-classe-106.csv").write_text("dan.jna,,membre,,,,\n")

    monkeypatch.setattr(sys, "argv", ["scrapeClassLists.py", str(input_dir), str(output_dir)])
    main()

    assert output_dir.is_dir()
    assert (output_dir / "rg106.txt").read_text() == "dan.jna"


def test_main_raises_for_wrong_number_of_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["scrapeClassLists.py"])
    try:
        main()
    except RuntimeError as exc:
        assert "Wrong number of args" in str(exc)
    else:
        assert False, "Expected RuntimeError"
