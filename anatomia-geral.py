import re, json

file = open('./trabalho-grupo/XMLs/anatomia geral.xml', 'r', encoding='utf-8')
xml_text = file.read()
file.close()

"""
This document has only images in pages 2, 4, 6, 8, 10, 12, 20, 22, and 24.

Some terms are in italic, others in bold, so they are surrounded by <i>, </i>, <b> and </b>.

In total, it has 20 different 'font' values, that go from 0 to 19.

On the even pages, some of the 'font' values represent:
- The 'font="0"' is the number of the page
- The 'font="1"' is the desciption of the page
- The 'font="2"' is (most likely) the chapter of the book
- The 'font="3"' is both the number (label) of the terms and the description
- The 'font="4"' is the terms group (eg. parts of the human body)
- The 'font="5"' is the terms subgroup (eg. head)
- The 'font="6"' is term
...

The font values that we want to keep are 5, 6, 7, 12 and 18
"""

# Remove even images, since they only have images
expression=r'(<page number="(?:[2468]|1[02]|2[024])".*\n(?:.*\n)*?</page>\n)'
xml_text = re.sub(expression, r'', xml_text)

# Remove \t
expression=r'\t'
xml_text = re.sub(expression, r'', xml_text)

# From 'font="X"' to #X=
expression=r'(?:<text.*?font="([0-9]*)".*?>(?:<.*?>)*\s*([^<>]+)\s*(?:<.*?>)*\n)'
xml_text = re.sub(expression, r'#\1=\2\n', xml_text)

# Remove the lines that don't have "#" in the start
expression=r'<.+\n'
xml_text = re.sub(expression, r'', xml_text)

# Remove A, B, C and D at the end of the lines
expression=r'([ABCD],? ?)+\n'
xml_text = re.sub(expression, r'\n', xml_text)

# Remove ". " at the start of the lines
expression=r'(#.*?=)\. (.+)'
xml_text = re.sub(expression, r'\1\2', xml_text)

# Remove final dots
expression=r'(.+)\. ?\n'
xml_text = re.sub(expression, r'\1\n', xml_text)

# Remove *
expression=r'\*'
xml_text = re.sub(expression, r'', xml_text)

# Remove words cut by the end of the line
expression=r'(#.*?=.*)-\n#.*?=(.*)'
xml_text = re.sub(expression, r'\1\2', xml_text)

# Remove the number (label) of the terms
expression=r'#.+=[0-9]*\n'
xml_text = re.sub(expression, r'', xml_text)

# Condense the descriptions
expression=r'(#3=.+)\n#3=(.+)'
while re.findall(expression, xml_text):
    xml_text = re.sub(expression, r'\1 \2', xml_text)

# Remove double spaces
expression=r'  '
xml_text = re.sub(expression, r' ', xml_text)

# Remove empty lines
expression=r'#.*?= *\n'
xml_text = re.sub(expression, r'', xml_text)

# Remove unwanted fonts that have or don't have descriptions
expression=r'#([0124]|1[0179])=.*\n'
expression_with_description = expression + r'#3=.+\n'
xml_text = re.sub(expression_with_description, r'', xml_text)
xml_text = re.sub(expression, r'', xml_text)

# Change #3= to #D=
expression=r'#3=(.+)'
xml_text = re.sub(expression, r'#D=\1', xml_text)

# Change #5=, #6=, #7=, #12= and #18= to #T=
expression=r'#(?:[567]|1[28])=(.+)'
xml_text = re.sub(expression, r'#T=\1', xml_text)

file = open('./trabalho-grupo/anatomia-geral/final.xml', 'w', encoding='utf-8')
file.write(xml_text)
file.close()

# Findall terms without description
expression=r'#T=(.+)\n#T='
terms_no_des = re.findall(expression, xml_text)

file = open('./trabalho-grupo/anatomia-geral/terms-no-des.json', 'w', encoding='utf-8')
json.dump(terms_no_des, file, ensure_ascii=False, indent=4)
file.close()

# Findall terms with description
expression=r'#T=(.+)\n#D=(.+)\n'
terms_des = re.findall(expression, xml_text)

terms = {}
for term, des in terms_des:
    terms[term]=des

file = open('./trabalho-grupo/anatomia-geral/dictionary.json', 'w', encoding='utf-8')
json.dump(terms, file, ensure_ascii=False, indent=4)
file.close()