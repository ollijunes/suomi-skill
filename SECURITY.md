# Security

## Report a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/ollijunes/suomi-skill/security/advisories/new).
Do not paste unpublished text of your own or a customer's into a public
issue. A short invented sentence that shows the problem is enough.

## What the checker does

- Reads the files and folders you name and prints a report. It writes no
  files and changes nothing.
- Follows no symbolic links inside a folder, skips hidden folders and
  `node_modules`, and refuses files over 2 MB.
- No network access, no subprocesses, no dependencies outside the Python
  standard library.
- The report quotes at most 100 characters around each finding. With
  `--json` in CI, those snippets end up in the build log.

## What the skill is

`skills/suomi/SKILL.md` is a text file of instructions for a language
model. It contains no code. Read it before you install it, as you should
with any skill: an agent follows what a skill says. The section "Omat
tiedot" is yours to fill in; do not put passwords, keys or anything secret
there, because the whole file is sent to the model provider.

## Repository hygiene

Every example text in this repository is invented. CI scans the full Git
history with Gitleaks and with `scripts/check_public_tree.py`, which looks
for private network addresses, home-directory paths, email addresses
outside example domains and private files. Automated scans support a manual
review; they do not prove that nothing private slipped in.
