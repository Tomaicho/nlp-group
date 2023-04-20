import re, json

file = open('XMLs\Glossario de Termos Medicos Tecnicos e Populares.xml', 'r', encoding='utf-8')
xml_text = file.read()
file.close()

"""
This document has lines that are separated into 2 elements in the XML file:
- the terms (in bold), usually followed by a empty text or a comma;
- the descriptions (in italic), usually followed by a text containing '(pop)'.

There are some exceptions to this:
- the definition of the terms 'acne' and 'esfoliação' are not followed by a '(pop)', instead they are together in the same text (so we will need
to separate the two). 
- the terms 'acne', 'mediador', 'pico do débito', 'vulvovaginite' and 'anxiolítico' are not followed by an empty text or a comma (this won't be a
problem, since the marking of the terms only uses the fact that they're bold). 
- in some lines that end with a term and the next one begins with another term, the first one is not followed by an empty text or a comma, such as
'adolescente', 'receptor' and 'polidipsia' (this won't be a problem, since the marking of the terms only uses the fact that they're bold). 
- in some lines, terms with 2 words are separated in the end, and they appear in 2 different XML elements, such as 'pré-medicação',
'infecção cruzada', 'efeito colateral' and 'tremor intencional' (so we will need to join them together). 

This way, it is needed to mark the text in bold a '#T=', and the text in italic with a '#D=...'.

It is essencial to notice that the descriptions do not always follow the terms, sometimes the terms (in bold) appear after the description (in
italic), so we can't rely on the order of these two.

All the letters that are used as a marker to find the terms manually (for example, to find 'vacina', we go to the section 'V') have the font
number '4' or '6', and they are not used anywhere else in the file.

It's important to notice that there are some entries that don't have descriptions, for example 'ambiente', 'antidopaminérgico',
'antifibrinolítico', 'bacteróide', 'betablocante', 'camada superficial', 'clónico' and 'pós-carga', but all of these are followed by a '(pop)',
so we can easily fix them by removing them.

There's also some terms in the file which descriptions are exactly the same as the term, so we opted to remove them
"""

### pre-processing:
# remove multiple spaces and new lines
xml_text = re.sub(r'([ ]){2,}', r'\1', xml_text)
xml_text = re.sub(r'([\n]){2,}', r'\1', xml_text) 

# remove spaces and ponctuations in the start or end of the text elements
xml_text = re.sub(r'>[ ,.]+', r'>', xml_text)
xml_text = re.sub(r'[ ,.]+<', r'<', xml_text)

# remove '\t'
xml_text = re.sub(r'\t', r'', xml_text)



### processing
# fix the terms 'acne' and 'esfoliação' - separate the description and the '(pop)'
xml_text = re.sub(r'(<.+?>)(.+?) \(pop\)(<.+?>)', r'\1<i>\2</i>\3\n\1(pop)\3', xml_text)

# remove all the non-text elements from the file
xml_text = re.sub(r'\n<[^t].+', r'', xml_text)
xml_text = re.sub(r'^<[^t].+\n', r'', xml_text)

# remove the mark of the sections for the manual search
xml_text = re.sub(r'<.+font="[46]".+\n', r'', xml_text)

# consolidate the descriptions that were separated by new lines
while re.search(r'(.+?<i>.+?)</i>.+?\n.+?<i>(.+?\n)', xml_text):
    xml_text = re.sub(r'(.+?<i>.+?)</i>.+?\n.+?<i>(.+?\n)', r'\1 \2', xml_text)

# remove the terms 'ambiente', 'antidopaminérgico', 'antifibrinolítico', 'bacteróide', 'betablocante', 'camada superficial', 'clónico' and
# 'pós-carga' - they don't have descriptions so we will remove them
xml_text = re.sub(r'(<.+>)<b>(.+)</b>(.+)\n(<.+>\(pop\)<.+>)\n', r'', xml_text)


# mark the terms and descriptions with '#T=' and #D=', respectively
xml_text = re.sub(r'.+?<b>(.+)</b>.+?\n', r'#T=\1\n', xml_text)
xml_text = re.sub(r'.+?<i>(.+)</i>.+?\n', r'#D=\1\n', xml_text)

# remove the rest of the XML elements
xml_text = re.sub(r'<.+\n', r'', xml_text)

# after all that, there are 5 lines that are marked as text that shoudn't be:
# '#T=(em português de Portugal)', '#T=Fonte:', '#T=Multilingual Glossary of Technical and Popular', '#T=Languages' and '#T=Observação:'
# there are the first 5 lines, so they can easily be removed
xml_text = re.sub(r'#.+\n', r'', xml_text, 5)

# fix 'pré-medicação', 'infecção cruzada', 'efeito colateral' and 'tremor intencional'
fix_list=[('pré-', 'medicação'), ('infecção', 'cruzada'), ('efeito', 'colateral'), ('tremor', 'intencional')]
for one, two in fix_list:
    if one =="pré-":
        xml_text = re.sub(r'#T='+one+r"\n#T="+two, r'#T='+one+two, xml_text)
    else:
        xml_text = re.sub(r'#T='+one+r"\n#T="+two, r'#T='+one+r' '+two, xml_text)

# visual aid to see how the next step is working
xml_cpy = xml_text
xml_cpy = re.sub(r'(#.=.+)\n(#.=.+)\n', r'\1\n\2\n\n', xml_cpy)
file = open('glossario\glossario.xml', 'w', encoding='utf-8')
file.write(xml_cpy)
file.close()

# now the terms and descriptions are in pairs, but not in order
dictionary = {}
# ':=' is a Walrus Operator, which asigns the result of the condition of the loop to a variable,
# in this case 'pair'
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
        term = description = pair.group(1)[3:]
        xml_text = re.sub(r'^(#.=.+)\n', r'', xml_text)
        print('ERROR:', pair)
    
    if description != term:
        if term in dictionary.keys():
            if type(dictionary.get(term)) == list:
                if description not in dictionary.get(term):
                    dictionary[term] = dictionary[term].append(description)
            else:
                if dictionary.get(term) != description:
                    dictionary[term] = [dictionary[term], description]
        else:
            dictionary[term] = description

for term, des in dictionary.items():
    if not isinstance(des, list):
        dictionary[term] = [des]

file = open('JSONs\glossario.json', 'w', encoding='utf-8')
json.dump(dictionary, file, ensure_ascii=False, indent=4)
file.close()
