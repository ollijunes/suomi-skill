# Contributing

Osallistua voi suomeksi tai englanniksi. Issues and pull requests are
welcome in Finnish or English.

The most useful contributions are false positives (an honest Finnish
sentence the checker flags) and patterns it misses. Include the sentence.
Invent one that shows the same thing; do not paste a customer's text.

```sh
uv sync --locked
uv run python -m pytest --cov=suomi_slop --cov-fail-under=90
uv run ruff check .
uv run ruff format --check .
uv run suomi-slop skills README.fi.md examples/hyva.md --min-score 8
gitleaks git --redact --no-banner .
python3 scripts/check_public_tree.py
```

## Rules

- A new rule needs an example that it matches and plain sentences it must
  not match. Add both to `tests/test_detect.py`. The test suite checks that
  every rule matches its own example.
- Prefer a narrow rule that is always right over a broad one that is often
  wrong. A checker that cries wolf gets turned off.
- The checker only reads. Do not add a mode that rewrites files.
- Keep the runtime on the Python standard library.
- The skill is one voice. Corrections of fact (grammar, typography,
  established usage) are welcome with a source such as Kielitoimiston
  ohjepankki. Changes of taste belong in your own copy.
- No real names, brands or customer text in examples.

Use a public-safe Git author address. Report vulnerabilities through
[SECURITY.md](SECURITY.md), not a public issue.
