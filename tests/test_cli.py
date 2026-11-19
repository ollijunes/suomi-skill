import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

from suomi_slop import cli

EXAMPLES = Path(__file__).parents[1] / "examples"


def test_folder_report(capsys):
    assert cli.main([str(EXAMPLES)]) == cli.EXIT_OK
    out = capsys.readouterr().out
    assert "slop.md: 0,0/10, kirjoita uudelleen (104 sanaa)" in out
    assert "hyva.md: 10,0/10, julkaisukelpoinen (98 sanaa)" in out
    assert "rivi 7: geneerinen-johdanto (vakava): Tässä artikkelissa käsittelemme" in out
    assert "muuta osumaa (--all näyttää kaikki)" in out
    assert "väliotsikot alkavat samalla sanalla: miksi" in out
    assert out.endswith("2 tiedostoa, keskiarvo 5,0/10\n")
    assert out.index("slop.md") < out.index("hyva.md"), "worst first"


def test_all_shows_every_finding(capsys):
    cli.main([str(EXAMPLES / "slop.md"), "--all"])
    out = capsys.readouterr().out
    assert "muuta osumaa" not in out
    assert "vastakkainasettelu (epäilyttävä): Se ei ole kuluerä. Se on" in out
    assert "yhdyssana (vältettävä): alunperin" in out
    assert "metakommentti (vakava): Toivottavasti tästä oli apua" in out


def test_min_score_sets_the_exit_code(capsys):
    assert cli.main([str(EXAMPLES / "hyva.md"), "--min-score", "8"]) == cli.EXIT_OK
    assert cli.main([str(EXAMPLES), "--min-score", "8"]) == cli.EXIT_BELOW
    capsys.readouterr()


def test_below_filters_the_listing(capsys):
    cli.main([str(EXAMPLES), "--below", "6"])
    out = capsys.readouterr().out
    assert "slop.md" in out
    assert "hyva.md" not in out


def test_json(capsys):
    assert cli.main([str(EXAMPLES), "--json"]) == cli.EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["summary"] == {"files": 2, "average": 5.0, "lowest": 0.0}
    worst = payload["reports"][0]
    assert worst["file"].endswith("slop.md")
    assert worst["findings"][0] == {
        "rule": "emoji",
        "level": "vakava",
        "line": 5,
        "snippet": "🚲",
        "advice": "Poista emojit asiatekstistä.",
    }


def test_stdin(capsys, monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO("Tilaa nyt! Heti.\n"))
    assert cli.main(["-"]) == cli.EXIT_OK
    out = capsys.readouterr().out
    assert out.startswith("<vakiosyöte>: 8,0/10, julkaisukelpoinen (3 sanaa)")
    assert "tiedostoa, keskiarvo" not in out


def test_density_lines(capsys, monkeypatch):
    text = "sana " * 100 + "a — b. " * 3 + "Tämä on tärkeää. " * 2 + "Se on kriittinen. " * 2
    monkeypatch.setattr(sys, "stdin", io.StringIO(text))
    cli.main(["-"])
    out = capsys.readouterr().out
    assert "ajatusviivoja 25,4 tuhatta sanaa kohti" in out
    assert "sana ”tärkeä” 2 kertaa" in out
    assert "sana ”kriittinen” 2 kertaa: yksi riittää" in out


def test_rules_listing(capsys):
    assert cli.main(["--rules"]) == cli.EXIT_OK
    out = capsys.readouterr().out
    assert "geneerinen-johdanto (vakava)" in out
    assert "esim. Siitä ei synny säästöä. Siitä syntyy kulu." in out


def test_errors(tmp_path, capsys):
    assert cli.main([]) == cli.EXIT_ERROR
    assert "anna tiedosto tai kansio" in capsys.readouterr().err
    assert cli.main([str(tmp_path / "puuttuu.md")]) == cli.EXIT_ERROR
    assert "ei löydy" in capsys.readouterr().err
    assert cli.main([str(tmp_path)]) == cli.EXIT_ERROR
    assert "ei tarkistettavia tiedostoja" in capsys.readouterr().err

    (tmp_path / "ok.md").write_text("Hyvä teksti.\n", encoding="utf-8")
    (tmp_path / "latin1.md").write_bytes("päivää".encode("latin-1"))
    assert cli.main([str(tmp_path)]) == cli.EXIT_ERROR
    captured = capsys.readouterr()
    assert "latin1.md: ei ole UTF-8-tekstiä" in captured.err
    assert "ok.md: 10,0/10" in captured.out


def test_version_and_module_entry_point():
    with pytest.raises(SystemExit) as exit_info:
        cli.main(["--version"])
    assert exit_info.value.code == 0
    result = subprocess.run(
        [sys.executable, "-m", "suomi_slop", str(EXAMPLES / "hyva.md"), "--min-score", "9"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "10,0/10" in result.stdout
