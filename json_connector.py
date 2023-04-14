import json

with(open("nlp-group\JSONs\dicionario_termos_medicos_pt_es_en_new.json", encoding="utf-8") as dict_pt_en_es):
    dict_pt_en_es = json.load(dict_pt_en_es)

with(open("nlp-group\JSONs\dictionary.json", encoding="utf-8") as dict_pt_des):
    dict_pt_des = json.load(dict_pt_des)

new_dict = {}
for term in dict_pt_en_es:
    en = dict_pt_en_es[term]["en"]
    es = dict_pt_en_es[term]["es"]
    if term in dict_pt_des:
        des = dict_pt_des[term]
        new_dict[term] = {"des": des, "en": en, "es": es}
    elif term not in dict_pt_des:
        new_dict[term] = {"en": en, "es": es}

for term in dict_pt_des:
    des = dict_pt_des[term]
    if term not in new_dict:
        new_dict[term] = {"des": des}

with(open("nlp-group\JSONs\combined.json", "w",  encoding="utf-8") as file):
    json.dump(new_dict,file,indent=6, ensure_ascii=False)