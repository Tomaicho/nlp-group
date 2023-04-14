import re
import json

with(open("nlp-group\enfermagem\Dicionario_de_termos_medicos_e_de_enfermagem.xml", encoding="utf-8") as file):
    xml = file.read()

new_xml = re.sub(r"<text.+?>","",xml)                       
new_xml = re.sub(r"</text>","", new_xml)
new_xml = re.sub(r"<page.+>","", new_xml)
new_xml = re.sub(r"\n<i>(.*)</i>",r"\1", new_xml)
new_xml = re.sub(r"\nfi\n\s","fi", new_xml)
new_xml = re.sub(r"○\n","", new_xml) 
new_xml = re.sub(r"\n\s<fontspec.*","", new_xml)
new_xml = re.sub(r"\nSou Enfermagem.*\n","", new_xml)
new_xml = re.sub(r"\n?</page>\n?","", new_xml)
new_xml = re.sub(r"\n[A-Z]{3}","", new_xml)
new_xml = re.sub(r"\n\s\n","", new_xml)
new_xml = re.sub(r"\n\s?\d{2,3}\n","", new_xml)
new_xml = re.sub(r"<b>([A-Z]?[^A-Z]*)</b>",r"\1", new_xml)
new_xml = re.sub(r"-?</b>\n<b>","", new_xml)
new_xml = re.sub(r"</b><b>","", new_xml)
new_xml = re.sub(r"\n[^<]","", new_xml)
# new_xml = re.sub(r"<b>\s*?([^A-Z])",r"\1", new_xml)
# new_xml = re.sub(r"([A-Z|)])\s</b>",r"\1</b>", new_xml)
# new_xml = re.sub(r"([^A-Z|)])</b>",r"\1", new_xml)

with(open("nlp-group\enfermagem\Dicionario_de_termos_medicos_e_de_enfermagem_new.xml", "w",  encoding="utf-8") as new_file):
    new_file.write(new_xml)


#	<fontspec id="28" size="10" family="NMNMLP+SSymbol" color="#131413"/> extraordinary exception -> manually deleted