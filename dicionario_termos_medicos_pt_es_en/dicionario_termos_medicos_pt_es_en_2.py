import re
import json

with(open("XMLs/dicionario_termos_medicos_pt_es_en_new.xml",  encoding="utf-8") as file):
    new_xml = file.read()

list = re.split(r"<b>",new_xml)

dict = {}
for i in list[1:]:
    print(i)
    term = re.split("</b>\nU|E",i)
    print('pppp',term)
    pt = term[0].strip()
    en = term[1].strip()
    es = term[2].strip()

    dict[pt]={"pt":pt, "en":en, "es":es}

with(open("JSONs/dicionario_termos_medicos_pt_es_en_new.json", "w",  encoding="utf-8") as dict_json):
    json.dump(dict,dict_json,indent=6, ensure_ascii=False)