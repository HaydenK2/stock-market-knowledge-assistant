import pathlib
import re

base = pathlib.Path('raw_docs')
files = list(base.glob('beginner_concepts/*.md')) + list(base.glob('market_mechanics/*.md'))

for path in files:
    lines = path.read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')
    print('===', path)
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('- ') or s.startswith('* '):
            continue
        if s.endswith('.') or s.endswith('?') or s.endswith(':'):
            continue
        words = s.split()
        if 1 < len(words) <= 10 and s == s.title() and not any(ch in s for ch in '0123456789'):
            print(i, repr(s))
    print()
