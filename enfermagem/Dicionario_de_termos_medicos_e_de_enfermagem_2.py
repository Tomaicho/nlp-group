import re
import json

with(open("nlp-group\enfermagem\Dicionario_de_termos_medicos_e_de_enfermagem_new.xml",  encoding="utf-8") as file):
    new_xml = file.read()

list = re.split(r"<b>",new_xml)

dict = {}
for term in list[1:]:
    term = re.split(r"</b>-?",term)
    pt = term[0].strip().replace("\n"," ")
    des = term[1].strip().replace("\n"," ")
    dict[pt] = des


    

with(open("nlp-group\JSONs\Dicionario_de_termos_medicos_e_de_enfermagem_new.json", "w",  encoding="utf-8") as dict_json):
    json.dump(dict,dict_json,indent=6, ensure_ascii=False)