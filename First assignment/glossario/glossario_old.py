import re, json

file = open('./trabalho-grupo/XMLs/Glossario de Termos Medicos Tecnicos e Populares.xml', 'r', encoding='utf-8')
xml_text = file.read()
file.close()

"""
This document has lines that are separated into 2 elements in the xml file:
- the term (in bold), followed by a empty text or a comma
- the description (in italic), followed by a text containing '(pop)'

There are some exceptions to this:
- the term 'adolescente' is not followed by a empty text or a comma, but by another term
- the terms 'acne', 'mediador', 'pico do débito', 'vulvovaginite' and 'anxiolítico' are not followed by a 
empty text or a comma, but they are followed by a
- the defenition of the terms 'acne' and 'esfoliação' are not followed by a '(pop)'

This way, it is needed to mark the text in bold followed by a a empty text or a comma with a '#T=...=T#',
and the text in italic followed by a '(pop)' with a '#D=...=D#'

It is essencial to notice that the descriptions do not always follow the terms,
sometimes the terms (in bold) appear after the description (in italic),
so we can't rely on the order of these two, unless we put all of them with the same order

All the letters that are used as a marker to find the terms manually (for example, to find 'vacina',
we go to the section 'V') have the font number '4' or '6'

It's important to notice that there are some entries that don't have descriptions, for example
'ambiente', 'antidopaminérgico', 'antifibrinolítico', 'bacteróide', 'betablocante', 'camada superficial',
'clónico' and 'pós-carga', but all of these are followed by a '(pop)', so we can easily fix them
"""

### pre-processing:
# remove multiple spaces and new lines
xml_text = re.sub(r'([ \n]){2,}', r'\1', xml_text)

# remove spaces and ponctuations in the start or end of the text
xml_text = re.sub(r'>[ ,.]+', r'>', xml_text)
xml_text = re.sub(r'[ ,.]+<', r'<', xml_text)

# remove '\t'
xml_text = re.sub(r'\t', r'', xml_text)

# verify if the '(pop)' are all alone in the same line
# res = ''
# for line in re.findall(r'.+\(pop\).+', xml_text):
#     text = re.sub(r'<.+?>(.+?)<.+?>', r'\1', line)
#     if text != '(pop)':
#         res += text + '\n'

# fix the terms 'acne' and 'esfoliação'
xml_text = re.sub(r'(<.+?>)(.+?) \(pop\)(<.+?>)', r'\1<i>\2</i>\3\n\1(pop)\3', xml_text)

# fix the tems 'adolescente'
fix_list = ['adolescente']
for element in fix_list:
    original_expression = r'(<.+>)'+element+r'(<.+>)'
    replacing_expression = r'\1'+element+r'\2\n\1\2'
    xml_text = re.sub(original_expression, replacing_expression, xml_text)



### processing
# remove all the non-text elements from the file
xml_text = re.sub(r'\n<[^t].+', r'', xml_text)
xml_text = re.sub(r'^<[^t].+\n', r'', xml_text)

# remove the mark for the manual search
xml_text = re.sub(r'<.+font="4".+\n', r'', xml_text)
xml_text = re.sub(r'<.+font="6".+\n', r'', xml_text)

# consolidate the terms and descriptions that were separated by new lines
while re.search(r'(.+?<b>.+?)</b>.+?\n.+?<b>(.+?\n)', xml_text):
    xml_text = re.sub(r'(.+?<b>.+?)</b>.+?\n.+?<b>(.+?\n)', r'\1 \2', xml_text)
while re.search(r'(.+?<i>.+?)</i>.+?\n.+?<i>(.+?\n)', xml_text):
    xml_text = re.sub(r'(.+?<i>.+?)</i>.+?\n.+?<i>(.+?\n)', r'\1 \2', xml_text)

# fix the terms 'ambiente', 'antidopaminérgico', 'antifibrinolítico', 'bacteróide', 'betablocante',
# 'camada superficial', 'clónico' and 'pós-carga'
xml_text = re.sub(r'(<.+>)<b>(.+)</b>(.+)\n(<.+>\(pop\)<.+>)\n', r'\1<b>\2</b>\3\n\1<i>\2</i>\3\n\4\n', xml_text)


# mark the terms and descriptions with '#T=' and #D=', respectively
xml_text = re.sub(r'.+?<b>(.+)</b>.+?\n', r'#T=\1\n', xml_text)
xml_text = re.sub(r'.+?<i>(.+)</i>.+?\n', r'#D=\1\n', xml_text)

# to confirm the terms and descriptions, mark them with "=T#" and "=D#" at the end, if they are followed by a blank text or a '(pop)'
xml_text = re.sub(r'(#T=.+?)\n<.+?>.+?\n', r'\1=T#\n', xml_text)
xml_text = re.sub(r'<text.+?></text>\n', r'', xml_text)
xml_text = re.sub(r'(#D=.+?)\n<.+?>\(pop\)<.+?>\n', r'\1=D#\n', xml_text)

# remove the rest of the XML elements
xml_text = re.sub(r'<.+\n', r'', xml_text)

# after all that, there are 2 lines that are marked as text that shoudn't be:
# '#T=(em português de Portugal) Fonte:=T#' and '#T=Multilingual Glossary of Technical and Popular Medical Terms in Nine European Languages Observação:=T#'
# there are the first two lines, so they can easily be removed
xml_text = re.sub(r'^#.+#\n#.+#\n', r'', xml_text)

# remove '=T#' and '=D#'
xml_text = re.sub(r'=[TD]#\n', r'\n', xml_text)

xml_cpy = xml_text
xml_cpy = re.sub(r'(#.=.+)\n(#.=.+)\n', r'\1\n\2\n\n', xml_cpy)

file = open('./trabalho-grupo/glossario/glossario.xml', 'w', encoding='utf-8')
file.write(xml_cpy)
file.close()

# now the terms and descriptions are in pairs, but not in order
dictionary = {}
# ':=' is a Walrus Operator, which asigns the result of the
# condition of the loop to a variable, in this case 'pair'
while pair := re.search(r'(#.=.+)\n(#.=.+)\n', xml_text):
    if re.search(r'#T=', pair.group(1)) and re.search(r'#D=', pair.group(2)):
        term = pair.group(1)[3:]
        description = pair.group(2)[3:]
        xml_text = re.sub(r'^(#.=.+)\n(#.=.+)\n', r'', xml_text)
    elif re.search(r'#T=', pair.group(2)) and re.search(r'#D=', pair.group(1)):
        term = pair.group(2)[3:]
        description = pair.group(1)[3:]
        xml_text = re.sub(r'^(#.=.+)\n(#.=.+)\n', r'', xml_text)
    else:
        print('ERROR', pair)
    
    if term in dictionary.keys():
        if type(dictionary.get(term)) == list:
            if description not in dictionary.get(term):
                dictionary[term] = dictionary[term].append(description)
        else:
            if dictionary.get(term) != description:
                dictionary[term] = [dictionary[term], description]
    else:
        dictionary[term] = description

file = open('./trabalho-grupo/glossario/glossario.json', 'w', encoding='utf-8')
json.dump(dictionary, file, ensure_ascii=False, indent=4)
file.close()
