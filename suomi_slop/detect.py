"""Tekstin esikäsittely ja pisteytys."""

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .patterns import (
    DASH,
    HEADING,
    KRIITTINEN,
    PENALTY,
    RULES,
    TARKEA,
    WORD,
)

EXTENSIONS = {".md", ".mdx", ".markdown", ".astro", ".html", ".htm", ".txt"}
MAX_BYTES = 2_000_000

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
SKIP_BLOCK = re.compile(
    r"<!--\s*suomi-slop:\s*ohita-alku\s*-->.*?(<!--\s*suomi-slop:\s*ohita-loppu\s*-->|\Z)",
    re.DOTALL,
)
SKIP_LINE = re.compile(r"^.*suomi-slop:\s*ohita\b.*$", re.MULTILINE)
NOT_PROSE = (
    re.compile(r"^(```|~~~).*?^\1[ \t]*$", re.DOTALL | re.MULTILINE),  # koodilohko
    re.compile(r"<(script|style|code|pre)\b.*?</\1\s*>", re.DOTALL | re.IGNORECASE),
    re.compile(r"<!--.*?-->", re.DOTALL),
    re.compile(r"^\s*import\s.+?from\s+['\"].+?['\"];?\s*$", re.MULTILINE),
    re.compile(r"`[^`\n]+`"),  # koodi rivin sisällä
    re.compile(r"\]\([^)\n]*\)"),  # linkin osoite
    re.compile(r"https?://\S+"),
    re.compile(r"^>.*$", re.MULTILINE),  # lainaus on jonkun muun tekstiä
)
# A tag may span lines (Astro and JSX props); "a < b" in prose is not a tag.
MARKUP = (re.compile(r"</?[A-Za-z][^>]*>"), re.compile(r"\{[^{}]*\}"))

GRADES = (
    (8.0, "julkaisukelpoinen"),
    (6.0, "pieniä korjauksia"),
    (4.0, "vaatii korjauksia"),
    (0.0, "kirjoita uudelleen"),
)


@dataclass
class Finding:
    rule: str
    level: str
    line: int
    snippet: str
    advice: str


@dataclass
class Report:
    file: str
    score: float
    grade: str
    words: int
    findings: list[Finding] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def as_dict(self) -> dict:
        return asdict(self)


def prose(raw: str) -> str:
    """Teksti, josta koodi, merkintä ja ohitetut kohdat on tyhjätty.

    Rivinvaihdot säilyvät, joten rivinumerot vastaavat alkuperäistä tiedostoa.
    """
    text = _without_code(raw)
    for pattern in MARKUP:
        text = pattern.sub(_blank, text)
    return text


def _without_code(raw: str) -> str:
    text = raw.replace("\r\n", "\n")
    for pattern in (FRONT_MATTER, SKIP_BLOCK, SKIP_LINE, *NOT_PROSE):
        text = pattern.sub(_blank, text)
    return text


def _blank(match: re.Match) -> str:
    return re.sub(r"[^\n]", " ", match.group(0))


def grade(score: float) -> str:
    return next(label for limit, label in GRADES if score >= limit)


def check_text(raw: str, name: str = "<teksti>") -> Report:
    text = prose(raw)
    words = len(WORD.findall(text))
    findings: list[Finding] = []
    penalty = 0.0

    for rule in RULES:
        hits = list(rule.regex.finditer(text))
        charged = _charged(rule.name, len(hits), words)
        penalty += charged
        for hit in hits:
            snippet = " ".join(hit.group(0).split())
            findings.append(
                Finding(
                    rule=rule.name,
                    level=rule.level,
                    line=text.count("\n", 0, hit.start()) + 1,
                    snippet=snippet if len(snippet) <= 100 else snippet[:97] + "...",
                    advice=rule.advice,
                )
            )

    metrics = _metrics(text, words, _without_code(raw))
    penalty += sum(entry["penalty"] for entry in metrics.values())
    score = max(0.0, round(10.0 - penalty, 1))
    findings.sort(key=lambda finding: (finding.line, finding.rule))
    return Report(name, score, grade(score), words, findings, metrics)


def _charged(name: str, count: int, words: int) -> float:
    """Vähennys säännön osumista. Osa säännöistä sallii muutaman osuman."""
    rule_penalty = PENALTY[next(rule.level for rule in RULES if rule.name == name)]
    if name == "kolmoisrytmi":
        # Oikeat luettelot ovat tavallisia: kolme osumaa tuhatta sanaa kohti on ilmaista.
        free = max(1, round(3 * words / 1000))
        return rule_penalty * max(0, count - free)
    if name == "ei-x-vaan-y":
        # Kerran on tyylikeino, toistuessaan maneeri.
        return 0.0 if count == 0 else rule_penalty + 1.0 * (count - 1)
    return rule_penalty * count


def _metrics(text: str, words: int, with_tags: str) -> dict:
    per_1000 = (lambda count: round(count * 1000 / words, 1)) if words else (lambda count: 0.0)
    long_enough = words >= 100

    dashes = len(DASH.findall(text))
    dash_rate = per_1000(dashes)
    dash_penalty = 0.0
    if long_enough:
        dash_penalty = 3.0 if dash_rate > 25 else 1.0 if dash_rate > 15 else 0.0

    tarkea = len(TARKEA.findall(text))
    tarkea_rate = per_1000(tarkea)
    tarkea_penalty = 0.0
    if long_enough:
        tarkea_penalty = 1.0 if tarkea_rate > 5 else 0.3 if tarkea_rate > 3 else 0.0

    kriittinen = len(KRIITTINEN.findall(text))

    first_words: dict[str, int] = {}
    headings = [(a or b).strip() for a, b in HEADING.findall(with_tags)]
    for heading in headings:
        parts = heading.split()
        if parts:
            key = parts[0].lower().strip(":,")
            first_words[key] = first_words.get(key, 0) + 1
    repeated = {word: count for word, count in first_words.items() if count > 1}
    heading_penalty = (
        0.5 * sum(count - 1 for count in repeated.values()) if len(headings) >= 3 else 0.0
    )

    return {
        "ajatusviivat": {"count": dashes, "per_1000": dash_rate, "penalty": dash_penalty},
        "tarkea": {"count": tarkea, "per_1000": tarkea_rate, "penalty": tarkea_penalty},
        "kriittinen": {"count": kriittinen, "penalty": 0.5 * max(0, kriittinen - 1)},
        "otsikoiden_alut": {"repeated": repeated, "penalty": heading_penalty},
    }


def check_file(path: Path) -> Report:
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"{path}: yli {MAX_BYTES // 1_000_000} Mt, ohitetaan")
    return check_text(data.decode("utf-8-sig"), str(path))


def collect(targets: list[Path]) -> list[Path]:
    """Tarkistettavat tiedostot. Symbolisia linkkejä ja piilokansioita ei seurata."""
    files: list[Path] = []
    for target in targets:
        if target.is_file():
            files.append(target)
        elif target.is_dir():
            for path in sorted(target.rglob("*")):
                relative = path.relative_to(target)
                hidden = any(
                    part.startswith(".") or part == "node_modules" for part in relative.parts
                )
                if hidden or path.is_symlink() or not path.is_file():
                    continue
                if path.suffix.lower() in EXTENSIONS:
                    files.append(path)
    return files
