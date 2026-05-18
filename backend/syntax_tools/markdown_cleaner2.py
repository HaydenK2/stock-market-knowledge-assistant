import pathlib
import re

base = pathlib.Path('raw_docs')
files = list(base.glob('beginner_concepts/*.md')) + list(base.glob('market_mechanics/*.md'))

heading_keywords = {
    'definition', 'key takeaways', 'important', 'fast fact', 'tip', 'pros', 'cons',
    'what is an ipo', 'what are etfs', 'what is a stock dividend', 'what is a bid-ask spread',
    'how do i invest in an ipo', 'how do i learn about the company', 'what are stocks',
    'what is pre-market and after-hours trading', 'what is an example of a stock dividend',
    'what is the difference between stock exchange and stock market', 'what are some common etf investing strategies',
    'what types of etfs are there', 'what should i consider before investing in etfs',
    'what do i pay for my etf', 'what are the risks of investing in etfs'
}
question_re = re.compile(r'^(?:What|How|Why|Can|Does|Is|Are|Do|Should|Will|Where|When|Which)\b')
heading_re = re.compile(r'^[A-Z][A-Za-z0-9\'\" ]{0,80}$')

for path in files:
    text = path.read_text(encoding='utf-8').replace('\r\n', '\n')
    text = re.sub(r'^(?:n|•|\*|\u2022)\s+', '- ', text, flags=re.M)
    lines = [line.rstrip() for line in text.split('\n')]
    out = []
    prev_blank = True

    def add_line(line: str):
        global prev_blank
        if out and out[-1] != '' and not out[-1].startswith('## ') and not out[-1].startswith('- '):
            out[-1] = out[-1] + ' ' + line
        else:
            out.append(line)
        prev_blank = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if out and out[-1] != '':
                out.append('')
            prev_blank = True
            continue

        if re.match(r'^(?:- |\* |\d+\.)\s+', stripped):
            if stripped.startswith('* '):
                stripped = '- ' + stripped[2:]
            elif re.match(r'^(\d+)\.(\s+)', stripped):
                stripped = '- ' + re.sub(r'^\d+\.\s*', '', stripped)
            out.append(stripped)
            prev_blank = False
            continue

        if len(stripped) <= 100 and stripped.endswith('?') and question_re.match(stripped):
            if not stripped.startswith('## '):
                stripped = '## ' + stripped
            if not prev_blank:
                out.append('')
            out.append(stripped)
            out.append('')
            prev_blank = True
            continue

        lower = stripped.lower()
        words = lower.split()
        if lower in heading_keywords or (
            len(words) <= 8 and heading_re.match(stripped) and not any(ch in stripped for ch in '.:,;')
        ):
            if not stripped.startswith('## '):
                stripped = '## ' + stripped
            if not prev_blank:
                out.append('')
            out.append(stripped)
            out.append('')
            prev_blank = True
            continue

        add_line(stripped)

    output = '\n'.join(out).strip() + '\n'
    print('===', path)
    print(output[:1200])
    print('\n...\n')
