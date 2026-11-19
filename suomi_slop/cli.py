"""Komentorivi."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .detect import Report, check_file, check_text, collect
from .patterns import RULES

EXIT_OK = 0
EXIT_BELOW = 1
EXIT_ERROR = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="suomi-slop",
        description="Etsii suomenkielisestä tekstistä tekoälytekstin ja käännössuomen merkit.",
    )
    parser.add_argument("--version", action="version", version=f"suomi-slop {__version__}")
    parser.add_argument("paths", nargs="*", help="tiedostot tai kansiot; - lukee vakiosyötteestä")
    parser.add_argument("--json", action="store_true", help="tulosta JSON")
    parser.add_argument(
        "--min-score",
        type=float,
        metavar="N",
        help="lopeta virhekoodilla 1, jos jonkin tiedoston pisteet jäävät alle N:n",
    )
    parser.add_argument(
        "--below", type=float, metavar="N", help="näytä vain tiedostot, joiden pisteet ovat alle N"
    )
    parser.add_argument("--all", action="store_true", help="näytä tiedoston kaikki osumat")
    parser.add_argument("--rules", action="store_true", help="listaa säännöt esimerkkeineen")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.rules:
        for rule in RULES:
            print(f"{rule.name} ({rule.level})\n  esim. {rule.example}\n  {rule.advice}")
        return EXIT_OK
    if not args.paths:
        print("suomi-slop: anna tiedosto tai kansio (tai - vakiosyötteelle)", file=sys.stderr)
        return EXIT_ERROR

    reports: list[Report] = []
    failed = False
    if args.paths == ["-"]:
        reports.append(check_text(sys.stdin.read(), "<vakiosyöte>"))
    else:
        targets = [Path(value) for value in args.paths]
        for target in targets:
            if not target.exists():
                print(f"suomi-slop: ei löydy: {target}", file=sys.stderr)
                failed = True
        for path in collect([target for target in targets if target.exists()]):
            try:
                reports.append(check_file(path))
            except (OSError, UnicodeDecodeError, ValueError) as error:
                reason = "ei ole UTF-8-tekstiä" if isinstance(error, UnicodeDecodeError) else error
                print(f"suomi-slop: {path}: {reason}", file=sys.stderr)
                failed = True
    if not reports:
        print("suomi-slop: ei tarkistettavia tiedostoja", file=sys.stderr)
        return EXIT_ERROR

    shown = [report for report in reports if args.below is None or report.score < args.below]
    shown.sort(key=lambda report: (report.score, report.file))
    average = round(sum(report.score for report in reports) / len(reports), 1)
    if args.json:
        payload = {
            "summary": {
                "files": len(reports),
                "average": average,
                "lowest": min(report.score for report in reports),
            },
            "reports": [report.as_dict() for report in shown],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for report in shown:
            print(_human(report, args.all))
        if len(reports) > 1:
            print(f"{len(reports)} tiedostoa, keskiarvo {_number(average)}/10")

    if failed:
        return EXIT_ERROR
    if args.min_score is not None and any(report.score < args.min_score for report in reports):
        return EXIT_BELOW
    return EXIT_OK


def _number(value: float) -> str:
    return f"{value:.1f}".replace(".", ",")


def _human(report: Report, show_all: bool) -> str:
    lines = [f"{report.file}: {_number(report.score)}/10, {report.grade} ({report.words} sanaa)"]
    limit = len(report.findings) if show_all else 12
    for finding in report.findings[:limit]:
        lines.append(f"  rivi {finding.line}: {finding.rule} ({finding.level}): {finding.snippet}")
        lines.append(f"    {finding.advice}")
    if len(report.findings) > limit:
        lines.append(f"  ja {len(report.findings) - limit} muuta osumaa (--all näyttää kaikki)")
    metrics = report.metrics
    if metrics["ajatusviivat"]["penalty"]:
        rate = _number(metrics["ajatusviivat"]["per_1000"])
        lines.append(f"  ajatusviivoja {rate} tuhatta sanaa kohti: käytä pilkkua tai pistettä")
    if metrics["tarkea"]["penalty"]:
        count = metrics["tarkea"]["count"]
        lines.append(f"  sana ”tärkeä” {count} kertaa: kerro, miksi asia on tärkeä")
    if metrics["kriittinen"]["penalty"]:
        count = metrics["kriittinen"]["count"]
        lines.append(f"  sana ”kriittinen” {count} kertaa: yksi riittää")
    if metrics["otsikoiden_alut"]["penalty"]:
        words = ", ".join(sorted(metrics["otsikoiden_alut"]["repeated"]))
        lines.append(f"  väliotsikot alkavat samalla sanalla: {words}")
    return "\n".join(lines)
