import json

with(open("JSONs/dicionario_termos_medicos_pt_es_en_new.json", encoding="utf-8") as dict_pt_en_es):
    dict_pt_en_es = json.load(dict_pt_en_es)

with(open("JSONs/dictionary.json", encoding="utf-8") as dict_pt_des):
    dict_pt_des = json.load(dict_pt_des)

with(open("JSONs/Dicionario_de_termos_medicos_e_de_enfermagem_new.json", encoding="utf-8") as dict_pt_des_enf):
    dict_pt_des_enf = json.load(dict_pt_des_enf)

with(open("JSONs\glossario.json", encoding="utf-8") as glossario):
    glossario = json.load(glossario)

new_dict = dict_pt_en_es

for term in dict_pt_des:
    des = dict_pt_des[term]
    term = term.lower()
    if term in new_dict:
        new_dict[term]["des"] = [des]
    if term not in new_dict:
        new_dict[term] = {"pt":term,"des": [des]}

for term in dict_pt_des_enf:
    des = dict_pt_des_enf[term]
    term = term.lower()
    if term in new_dict:
        if "des" in new_dict[term]:
            new_dict[term]["des"].append(des)
        if "des" not in new_dict[term]:
            new_dict[term]["des"] = [des]
    elif term not in new_dict:
        new_dict[term] = {"pt":term,"des": [des]}

for term in glossario:
    des = glossario[term]
    term = term.lower()
    if term in new_dict:
        if "des" in new_dict[term]:
            for i in des:
                new_dict[term]["des"].append(i)
        if "des" not in new_dict[term]:
            new_dict[term]["des"] = des
    elif term not in new_dict:
        new_dict[term] = {"pt":term,"des":des}


with(open("JSONs\combined.json", "w",  encoding="utf-8") as file):
            json.dump(new_dict,file,indent=6, ensure_ascii=False)   

  