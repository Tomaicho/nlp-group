import re
import json

with(open("XMLs/dicionario_termos_medicos_pt_es_en_new.xml",  encoding="utf-8") as file):
    new_xml = file.read()

list = re.split(r"<b>",new_xml)

dict = {}
for i in list[1:]:
    print(i)
    term = re.split("\nU\n|\nE\n",i)
    pt = term[0].strip().replace("\n"," ")
    en = term[1].strip().replace("\n"," ")
    es = term[2].strip().replace("\n"," ")

    dict[pt]={"pt":pt, "en":en, "es":es}

with(open("JSONs/dicionario_termos_medicos_pt_es_en_new.json", "w",  encoding="utf-8") as dict_json):
    json.dump(dict,dict_json,indent=6, ensure_ascii=False)