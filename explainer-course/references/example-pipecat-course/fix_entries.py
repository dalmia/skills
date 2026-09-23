"""Replace whole add(...) entries in lessons_m_all.py by title. Usage: from fix_entries import replace; replace({title: new_add_source})"""
import re
P='lessons_m_all.py'
def replace(entries):
    s=open(P).read()
    for title,new in entries.items():
        m=re.search(r'add\(\d, "%s", .*?\)\n(?=\n)' % re.escape(title), s, re.S)
        assert m, title
        s=s[:m.start()]+new.strip()+"\n"+s[m.end():]
    open(P,'w').write(s)
