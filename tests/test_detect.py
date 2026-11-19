from pathlib import Path

import pytest

from suomi_slop.detect import check_file, check_text, collect, grade, prose
from suomi_slop.patterns import RULES, RULES_BY_NAME

EXAMPLES = Path(__file__).parents[1] / "examples"


def rules(text: str) -> list[str]:
    return [finding.rule for finding in check_text(text).findings]


def test_examples_score_as_documented():
    bad = check_file(EXAMPLES / "slop.md")
    good = check_file(EXAMPLES / "hyva.md")
    assert bad.score == 0.0
    assert bad.grade == "kirjoita uudelleen"
    assert good.score == 10.0
    assert good.grade == "julkaisukelpoinen"
    assert good.findings == []


@pytest.mark.parametrize("rule", RULES, ids=lambda rule: rule.name)
def test_every_rule_matches_its_own_example(rule):
    assert rule.regex.search(rule.example), rule.name
    assert rule.name in rules(rule.example)
    assert rule.advice.endswith((".", "”"))


def test_rule_names_are_unique():
    assert len(RULES_BY_NAME) == len(RULES)


@pytest.mark.parametrize(
    "text",
    [
        "Ketju kestää pidempään, kun sen öljyää.",
        "Hinta on 12 euroa. Toimitus kestää kaksi päivää.",
        "Vastaus on 5! Ei, se on laskutoimitus 5!.",
        "Käytä komentoa `echo Hei!` terminaalissa.",
        "![Kuva pyörästä](kuva.jpg)",
        "Lue [ohje](https://example.com/ohje!/sivu).",
        "> Tässä artikkelissa käsittelemme lainattua tekstiä!",
        "Se ei ole valmis. Tilaus saapuu huomenna.",
    ],
)
def test_plain_finnish_is_clean(text):
    assert rules(text) == []


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        ("Tämä opas kertoo kaiken leipomisesta.", "geneerinen-johdanto"),
        ("Se onnistuu helposti ⭐", "emoji"),
        ("Tilaa nyt! Saat alennuksen.", "huutomerkki"),
        ("Kielimallina en voi tietää.", "metakommentti"),
        ("On syytä huomata, että määräaika on tiukka.", "taytesana"),
        ("Rehellisyys on yrityksen kivijalka.", "tyhja-metafora"),
        ("Palvelu on ainutlaatuinen.", "superlatiivi"),
        ("Päivän päätteeksi hinta ratkaisee.", "kaannoskukkanen"),
        ("Olemme kokoajan tavoitettavissa.", "yhdyssana"),
        ("Katsotaanpa tarkemmin, mitä laki sanoo.", "siirtymalause"),
        ("Tarjoamme saumattoman kokemuksen.", "konsulttisana"),
        ("Se ei ole pelkkä työkalu vaan kumppani.", "ei-x-vaan-y"),
        ("Kyse ei ole hinnasta. Kyse on luottamuksesta.", "vastakkainasettelu"),
        ("Palvelu on nopea, varma ja edullinen.", "kolmoisrytmi"),
        ("On mahdollista, että hinta nousee.", "passiivitayte"),
        ("Ratkaisu on innovatiivinen.", "strategiasana"),
    ],
)
def test_variants(text, rule):
    assert rule in rules(text)


def test_line_numbers_point_at_the_original_file():
    head = "---\ntitle: x\n---\n\nHyvä kappale.\n\n"
    text = head + "```\nTilaa nyt! koodissa\n```\n\nTilaa nyt! tekstissä.\n"
    report = check_text(text)
    assert [(finding.rule, finding.line) for finding in report.findings] == [("huutomerkki", 11)]
    assert report.findings[0].snippet == "nyt!"


def test_markup_code_and_addresses_are_not_prose():
    raw = (
        "import Kortti from '../Kortti.astro';\n"
        '<Kortti otsikko="Hei!" data={{ a: "Tilaa nyt!" }} />\n'
        "<script>alert('Tilaa nyt! ');</script>\n"
        "<style>.a::after { content: 'Hei! '; }</style>\n"
        "<!-- Muista tämä! -->\n"
        "Teksti jatkuu rauhallisesti.\n"
    )
    assert rules(raw) == []
    assert prose(raw).count("\n") == raw.count("\n")
    assert len(prose(raw)) == len(raw)


def test_tags_and_expressions_over_several_lines_are_not_prose():
    raw = (
        "<Kortti\n"
        '  otsikko="Tervetuloa lukemaan"\n'
        '  teksti="Tilaa nyt! Heti."\n'
        "/>\n"
        "{ehto && (\n  'Tilaa nyt! Heti.'\n)}\n"
        "Jos a < b ja b > c, kannattaa muistaa järjestys.\n"
    )
    report = check_text(raw)
    assert [(finding.rule, finding.line) for finding in report.findings] == [("taytesana", 8)]


def test_byte_order_mark_does_not_hide_front_matter(tmp_path):
    path = tmp_path / "bom.md"
    path.write_bytes("\ufeff---\ntitle: Tilaa nyt! Heti.\n---\nHyvä teksti.\n".encode())
    assert check_file(path).findings == []


def test_skip_markers():
    line = "Tervetuloa lukemaan! <!-- suomi-slop: ohita -->\nTeksti.\n"
    assert rules(line) == []
    block = (
        "Teksti.\n<!-- suomi-slop: ohita-alku -->\n| Tönkkö | Korjattu |\n"
        "| Tervetuloa lukemaan! | Tervetuloa. |\n<!-- suomi-slop: ohita-loppu -->\n"
        "Tilaa nyt! Heti.\n"
    )
    report = check_text(block)
    assert [(finding.rule, finding.line) for finding in report.findings] == [("huutomerkki", 6)]
    unclosed = "Teksti.\n<!-- suomi-slop: ohita-alku -->\nTilaa nyt! Heti.\n"
    assert rules(unclosed) == []


def test_scoring_levels():
    assert check_text("Tilaa nyt! Heti.").score == 8.0
    assert check_text("Kannattaa muistaa kuitit.").score == 9.5
    assert check_text("Voidaan todeta, että sataa.").score == 9.8
    assert check_text("Tilaa! Osta! Hae! Tule! Mene! Juokse! Aja!").score == 0.0


def test_one_real_list_is_free_and_repeated_triplets_cost():
    one = "Ota mukaan maitoa, leipää ja juustoa."
    assert check_text(one).score == 10.0
    assert rules(one) == ["kolmoisrytmi"]
    many = " ".join(["Palvelu on nopea, varma ja edullinen."] * 4)
    assert check_text(many).score == 9.4


def test_ei_x_vaan_y_costs_more_when_repeated():
    once = "Se ei ole vain laskuri, vaan työkalu."
    assert check_text(once).score == 9.8
    assert check_text(f"{once} {once} {once}").score == 7.8


def test_density_metrics_need_a_real_text():
    short = "Sää oli hyvä — ja tie kuiva — ja mieli kevyt."
    assert check_text(short).metrics["ajatusviivat"]["penalty"] == 0.0
    filler = "sana " * 100
    dashes = check_text(filler + "alku — loppu. " * 2)
    assert dashes.metrics["ajatusviivat"] == {"count": 2, "per_1000": 19.2, "penalty": 1.0}
    heavy = check_text(filler + "alku – loppu. " * 4)
    assert heavy.metrics["ajatusviivat"]["penalty"] == 3.0
    tarkea = check_text(filler + "Tämä on tärkeää. " * 2)
    assert tarkea.metrics["tarkea"]["penalty"] == 1.0
    mild = check_text("sana " * 300 + "Tämä on tärkeä asia.")
    assert mild.metrics["tarkea"]["penalty"] == 0.3
    assert check_text("").metrics["tarkea"]["per_1000"] == 0.0


def test_kriittinen_and_repeated_heading_starts():
    report = check_text("Vaihe on kriittinen. Päätös on kriittinen. Aikataulu on kriittinen.")
    assert report.metrics["kriittinen"] == {"count": 3, "penalty": 1.0}
    headings = "## Miksi a\n\nx\n\n## Miksi b\n\nx\n\n<h2>Miksi c</h2>\n\n### Näin teet\n"
    assert check_text(headings).metrics["otsikoiden_alut"] == {
        "repeated": {"miksi": 3},
        "penalty": 1.0,
    }
    two = "## Miksi a\n\n## Miksi b\n"
    assert check_text(two).metrics["otsikoiden_alut"]["penalty"] == 0.0


def test_grades():
    assert [grade(value) for value in (10, 8.0, 7.9, 6.0, 5.9, 4.0, 3.9, 0)] == [
        "julkaisukelpoinen",
        "julkaisukelpoinen",
        "pieniä korjauksia",
        "pieniä korjauksia",
        "vaatii korjauksia",
        "vaatii korjauksia",
        "kirjoita uudelleen",
        "kirjoita uudelleen",
    ]


def test_long_snippets_are_cut():
    text = "Se ei ole vain " + "hyvin pitkä selitys " * 3 + "asiasta, vaan muuta."
    snippet = check_text(text).findings[0].snippet
    assert len(snippet) <= 100


def test_collect_skips_hidden_folders_symlinks_and_other_types(tmp_path):
    (tmp_path / "a.md").write_text("x", encoding="utf-8")
    (tmp_path / "b.astro").write_text("x", encoding="utf-8")
    (tmp_path / "c.py").write_text("x", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "d.md").write_text("x", encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "e.md").write_text("x", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "f.HTML").write_text("x", encoding="utf-8")
    (tmp_path / "link.md").symlink_to(tmp_path / "a.md")
    found = collect([tmp_path, tmp_path / "c.py"])
    assert [path.name for path in found] == ["a.md", "b.astro", "f.HTML", "c.py"]


def test_oversized_file_is_refused(tmp_path, monkeypatch):
    monkeypatch.setattr("suomi_slop.detect.MAX_BYTES", 10)
    path = tmp_path / "big.md"
    path.write_text("x" * 11, encoding="utf-8")
    with pytest.raises(ValueError, match="ohitetaan"):
        check_file(path)
