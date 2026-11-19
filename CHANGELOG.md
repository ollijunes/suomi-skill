# Changelog

## 0.1.0

- `skills/suomi/SKILL.md`: a Finnish writing skill for coding agents with
  registers, sentence structure, grammar traps, banned patterns, translated
  idioms with Finnish equivalents, before-and-after pairs and a section for
  your own facts.
- `suomi-slop`: sixteen rules on three levels and four density checks,
  scores from 0 to 10, line numbers and advice for every finding.
- Reads Markdown, MDX, Astro, HTML and text. Skips front matter, code,
  comments, link addresses and block quotes. Skip markers for quoted bad
  examples.
- `--min-score` for CI and hooks, `--json`, `--below`, `--all`, `--rules`,
  standard input.
- Tests on Linux and macOS with Python 3.11–3.14. The repository's own
  Finnish is checked with the checker in CI.
