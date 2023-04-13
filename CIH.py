import re

file = open('./XMLs/CIH.html', encoding='utf8')
html = file.read()
file.close()

txt = re.sub(r'\#160', '', html)
txt = re.sub(r'&;', '', txt)

print(txt)
