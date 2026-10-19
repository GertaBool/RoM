"""html2txt.py <in.html> <out.txt>: visible text of an HTML page, block elements on their own lines."""
import html.parser, sys
BLOCK = {'p','div','br','li','h1','h2','h3','h4','h5','h6','tr','pre','blockquote','section','dt','dd','figcaption','table'}
SKIP = {'script','style','nav','header','footer','noscript','svg'}
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in SKIP: s.skip+=1
        if t in BLOCK: s.out.append('\n')
        if t in ('h1','h2','h3','h4'): s.out.append('#'*int(t[1])+' ')
    def handle_endtag(s,t):
        if t in SKIP and s.skip: s.skip-=1
        if t in BLOCK: s.out.append('\n')
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8',errors='replace').read())
import re
t=re.sub(r'[ \t]+',' ',''.join(p.out)); t=re.sub(r'\n\s*\n+','\n\n',t)
open(sys.argv[2],'w').write(t.strip()+'\n')
