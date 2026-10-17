#!/usr/bin/env python3
"""Stamp js/site-meta.js with the current UTC time when site content is staged.

Runs automatically from the pre-commit hook (.githooks/pre-commit).
Only real site content counts: changes to the stamp file itself, scripts,
hooks, deploy files and Markdown docs do not update the timestamp.
"""
import datetime
import pathlib
import re
import subprocess
import sys

META = 'js/site-meta.js'
IGNORED_PREFIXES = ('scripts/', '.githooks/', 'deploy/')
IGNORED_SUFFIXES = ('.md', '.gitignore')


def git(*args):
    return subprocess.run(['git', *args], capture_output=True, text=True)


def is_content(path):
    if path == META:
        return False
    if path.startswith(IGNORED_PREFIXES):
        return False
    return not path.endswith(IGNORED_SUFFIXES)


def main():
    top = git('rev-parse', '--show-toplevel')
    if top.returncode != 0:
        print('stamp: not a git repository, skipped')
        return 0

    repo = pathlib.Path(top.stdout.strip())
    staged = git('diff', '--cached', '--name-only', '--diff-filter=ACMRD').stdout.splitlines()
    changed = [f for f in staged if is_content(f)]
    if not changed:
        return 0

    stamp = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    value = stamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    path = repo / META
    text = path.read_text(encoding='utf-8')
    new_text, count = re.subn(
        r"window\.QF_LAST_UPDATED = '[^']*';",
        f"window.QF_LAST_UPDATED = '{value}';",
        text,
    )
    if count != 1:
        print(f'stamp: could not find QF_LAST_UPDATED line in {META}')
        return 1

    path.write_text(new_text, encoding='utf-8')
    git('add', META)
    print(f'stamp: {META} set to {value} ({len(changed)} content file(s) changed)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
