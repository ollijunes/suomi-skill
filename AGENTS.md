# Working in this repository

Read [CONTRIBUTING.md](CONTRIBUTING.md) first. Before you say a change is done, run:

```sh
uv run python -m pytest --cov=suomi_slop --cov-fail-under=90
uv run ruff check .
uv run ruff format --check .
uv run suomi-slop skills README.fi.md examples/hyva.md --min-score 8
python3 scripts/check_public_tree.py
```

- Examples and test data are invented. Use `example.com` and made-up names; never copy a real
  file, page, path or text from your own machine.
- Tests do not use the network and do not read the real home folder.
- Commit each working step with a short message in the imperative. Do not use `--no-verify`.
