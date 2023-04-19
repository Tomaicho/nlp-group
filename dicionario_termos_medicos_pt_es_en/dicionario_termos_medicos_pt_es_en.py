import re
import json

with(open("XMLs/dicionario_termos_medicos_pt_es_en.xml", encoding="utf-8") as file):
    xml = file.read()

new_xml = re.sub(r"<text.+?>","",xml)                       
new_xml = re.sub(r"</text>","", new_xml)
new_xml = re.sub(r"<page.+>","", new_xml)
new_xml = re.sub(r"(<b>.+</b>\n)+</page>",r"", new_xml)     #remove side notch(portugues-ingles-espanhol) and </page>
new_xml = re.sub(r"<b>\d+</b>","", new_xml)                 #remove page number
new_xml = re.sub(r"<b>[A-Z]</b>","", new_xml)               #remove big letters in the beggining of each chapter
new_xml = re.sub(r"\n<i>.+</i>","", new_xml)
new_xml = re.sub(r"</b>\n<b>"," ", new_xml)
new_xml = re.sub(r"-\n","", new_xml) 
new_xml = re.sub(r"\n\n","\n", new_xml) 
new_xml = re.sub(r"\(\n?[^\)]*\n?\+\n?[^\)]*\n?\)","", new_xml)
new_xml = re.sub(r"</b>","", new_xml)


with(open("XMLs/dicionario_termos_medicos_pt_es_en_new.xml", "w",  encoding="utf-8") as new_file):
    new_file.write(new_xml)


#	<fontspec id="28" size="10" family="NMNMLP+SSymbol" color="#131413"/> extraordinary exception -> manually deleted