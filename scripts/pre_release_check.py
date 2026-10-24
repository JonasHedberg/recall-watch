"""Refuse a release with unresolved required maintainer metadata.

Run after tests and GitHub actions. This checks only local metadata; it does NOT
substitute for live Home Assistant and feed verification.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'custom_components' / 'recall_watch' / 'manifest.json'


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    issues: list[str] = []
    for field in ('documentation', 'issue_tracker'):
        link = manifest.get(field, '')
        if not link.startswith('https://github.com/') or 'REPLACE_WITH_OWNER' in link:
            issues.append(f'{field}: set a real public GitHub URL')
    owners = manifest.get('codeowners', [])
    if not owners or any(not owner.startswith('@') or 'REPLACE' in owner for owner in owners):
        issues.append('codeowners: assign a real GitHub maintainer')
    if not (ROOT / 'custom_components/recall_watch/translations/en.json').is_file():
        issues.append('translations: English fallback is missing')
    if not (ROOT / 'custom_components/recall_watch/translations/sv.json').is_file():
        issues.append('translations: Swedish locale is missing')
    if issues:
        print('Release BLOCKED:')
        for issue in issues:
            print(f' - {issue}')
        return 1
    print('Local metadata checks passed. Release still requires CI and Home Assistant smoke tests.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
