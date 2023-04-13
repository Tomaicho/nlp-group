import re

file = open('./XMLs/anatomia gerals.html', encoding='utf8')
html = file.read()
file.close()

txt = re.sub(r'\#160', '', html)

print(txt)

