import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "privacy_checker", Path(__file__).parents[1] / "scripts/check_public_tree.py"
)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def test_canaries_and_allowed_examples():
    checker.self_test()
    assert not checker.detect(b"Synthetic <synthetic@example.com>")
    assert not checker.detect(b"GitHub <noreply@github.com>")
    assert checker.private_path("config.toml")
    assert not checker.private_path("examples/config.toml")
    assert not checker.private_path("examples/slop.md")


@pytest.mark.parametrize(
    "value",
    [
        "@".join(("someone", "unapproved.com")),
        "/".join(("", "Users", "synthetic", "note")),
        "+" + "358" + "401234567",
        ".".join(("192", "168", "1", "1")),
    ],
)
def test_private_values(value):
    assert checker.detect(value.encode())


@pytest.mark.parametrize("path", [".claude/CLAUDE.md", ".codex/AGENTS.md", "auth.json", ".env"])
def test_agent_runtime_paths_are_rejected(path):
    assert checker.private_path(path)
    assert checker.private_path("examples/home/.claude/CLAUDE.md")
