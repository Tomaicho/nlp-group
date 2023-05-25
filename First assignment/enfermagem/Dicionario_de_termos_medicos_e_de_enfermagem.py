import re
import json

with(open("./enfermagem/Dicionario_de_termos_medicos_e_de_enfermagem.xml", encoding="utf-8") as file):
    xml = file.read()

new_xml = re.sub(r'<text.+height="\d+" ',"",xml)                       
new_xml = re.sub(r"</text>","", new_xml)
new_xml = re.sub(r"<page.+>","", new_xml)
new_xml = re.sub(r"<b>(.+)</b>",r"\1", new_xml) #Removes all bold identifications
new_xml = re.sub(r"<i>(.*)</i>",r"\1", new_xml) #Removes all italic identifications
new_xml = re.sub(r'\nfont="\d+">fi\nfont="\d+"> ',"fi", new_xml) #Deals with the words cut in the -fi- syllable
new_xml = re.sub(r'font="\d+">○\n',"", new_xml) 
new_xml = re.sub(r"\n\s<fontspec.*","", new_xml)
new_xml = re.sub(r'font="\d+">Sou Enfermagem.*\n',"", new_xml)
new_xml = re.sub(r"\n?</page>\n?","", new_xml)
new_xml = re.sub(r'\nfont="(20|6|19)">.+',"", new_xml) #Remove 3 capital letters (like chapter markings) and page numbers and remove lines with -
new_xml = re.sub(r'\nfont="\d+"> \n',"\n", new_xml) #Remove empty lines
new_xml = re.sub(r'-\nfont="\d+">(.)',r"\1", new_xml) #Join words separated by - in different lines
new_xml = re.sub(r'(font="(24|10)">.+)\nfont="(24|10)">(.+)',r"\1\4", new_xml) #Join terms separated in different lines
new_xml = re.sub(r'font="(24|10)">(.+)',r"\2@", new_xml) #Marks terms
new_xml = re.sub(r'\nfont="\d+">(.)',r" \1", new_xml) #Joins description all in one line



with(open("./enfermagem/Dicionario_de_termos_medicos_e_de_enfermagem_new.xml", "w",  encoding="utf-8") as new_file):
    new_file.write(new_xml)


