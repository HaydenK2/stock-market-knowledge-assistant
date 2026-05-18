import pathlib
import re

base = pathlib.Path('raw_docs')
files = list(base.glob('beginner_concepts/*.md')) + list(base.glob('market_mechanics/*.md'))
question = re.compile(r'^(?:What|How|Why|Can|Does|Is|Are|Do|Should|Will|Where|When|Which)\b')

keywords = {
    'definition', 'key takeaways', 'important', 'fast fact', 'tip', 'pros', 'cons',
    'ask', 'what are etfs', 'how do i invest in an ipo', 'how do i learn about the company',
    'what are stock exchanges', 'what are the risks of investing in etfs', 'what do i pay for my etf',
    'what types of etfs are there', 'how do i buy and sell etfs', 'what should i consider before investing in etfs',
    'what is pre-market and after-hours trading', 'what is an ipo', 'what is a stock dividend', 'what is a bull market'
}

for path in files:
    lines = path.read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')
    print('===', path)
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('- ') or s.startswith('* '):
            continue
        if len(s) <= 100 and (
            s.endswith('?') or
            (len(s.split()) <= 8 and question.match(s) and not any(ch in s for ch in '.:,;')) or
            s.lower() in keywords
        ):
            print(i, repr(s))
    print()
