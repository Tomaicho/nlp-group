import re
import json

with(open("./enfermagem/Dicionario_de_termos_medicos_e_de_enfermagem_new.xml",  encoding="utf-8") as file):
    lines = file.readlines()


dict = {}
for line in lines:
    split = line.split('@')
    pt = split[0]
    des = split[1].strip()
    dict[pt] = des


    

with(open(".\JSONs\Dicionario_de_termos_medicos_e_de_enfermagem_new.json", "w",  encoding="utf-8") as dict_json):
    json.dump(dict,dict_json,indent=6, ensure_ascii=False)