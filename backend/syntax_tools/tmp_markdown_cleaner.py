import re
import pathlib
base = pathlib.Path('raw_docs')
files = list(base.glob('beginner_concepts/*.md')) + list(base.glob('market_mechanics/*.md'))
headings = [
    'Definition','Key Takeaways','Important','Fast Fact','Tip','Pros','Cons','The Bid and the Ask',
    'Bid-Ask Spread Calculation','The Spread','Beyond the Basic','Bid-Ask Spread and Liquidity',
    'Bid-Ask Spread and Arbitrage','How Does Bid-Ask Spread Work','What Causes a Bid-Ask Spread to Be High',
    'What Is an Example of a Bid-Ask Spread in Stocks','How Pre-Market and After-Hours Trading Works',
    'After-Market Hours','Pre-Market Hours','Overnight Trading','Advantages and Disadvantages of Pre-Market and After-Hours Trading',
    'Pros of Pre-Market and After-Hours Trading','Cons of Pre-Market and After-Hours Trading','How Stock Exchanges Operate',
    'Different Kinds of Stock Exchanges','Understanding Auction Exchanges','Navigating Dealer Markets',
    'Exploring Electronic Exchanges','Understanding Over-the-Counter Markets','Key Exchanges in the United States',
    'Listing Requirements','Over-The-Counter (OTC)','International Exchanges','Steps to Start Investing in the Stock Market',
    'Choosing the Right Brokerage House','Full-Service Brokerages','Discount Brokerages','Exploring Alternative Trading Systems',
    'Insight Into Dark Pools','Overview of Cryptocurrency Exchanges','How Does the SEC Regulate Markets in the United States',
    'What Is the Difference Between Stock Exchange and Stock Market','What Are Stock Exchanges','What Is a Bid-Ask Spread',
    'What is an IPO','What are ETFs','What are the risks of investing in ETFs','What do I pay for my ETF',
    'What are some common ETF investing strategies','What types of ETFs are there','How do I buy and sell ETFs',
    'What should I consider before investing in ETFs','How do I learn about the company','What else should I consider',
    'Is a Stock Dividend a Good or Bad Thing','What Is a Good Dividend Yield','What Is an Example of a Stock Dividend',
    'Accounting Entries When Issuing Stock Dividends'
]
for path in files:
    text = path.read_text(encoding='utf-8').replace('\r\n','\n').strip() + '\n'
    text = re.sub(r'^(?:n|•|\*|\u2022)\s+', '- ', text, flags=re.M)
    lines = text.split('\n')
    out_lines = []
    cur = []
    def flush():
        global cur
        if cur:
            out_lines.append(' '.join(line.strip() for line in cur))
            cur = []
    for line in lines:
        s = line.strip()
        if not s:
            flush()
            out_lines.append('')
            continue
        if re.match(r'^(?:- |\* |\d+\.|## )', s):
            flush()
            out_lines.append(s)
            continue
        if len(s) < 120 and re.match(r'^[A-Z][A-Za-z0-9\-\'\" ]+[?]$', s):
            flush()
            out_lines.append(s)
            continue
        if len(s) < 100 and s == s.title() and ' ' in s and '.' not in s:
            flush()
            out_lines.append(s)
            continue
        cur.append(line)
    flush()
    clean = []
    for para in out_lines:
        if not para.strip():
            clean.append(para)
            continue
        if para in headings:
            clean.append('## ' + para)
            continue
        if re.match(r'^(?:What is|What are|How do|How does|How can|Why do|Why are|Can you|Does after|Does|Is|Are|Do|Should|Will|Where|When) ', para, flags=re.I):
            clean.append('## ' + para)
            continue
        if para.startswith('- '):
            clean.append(para)
            continue
        m = re.match(r'^(\d+)\.\s+(.*)$', para)
        if m:
            clean.append('- ' + m.group(2))
            continue
        clean.append(para)
    print('===', path)
    print('\n'.join(clean[:120]))
    print('\n...\n')
