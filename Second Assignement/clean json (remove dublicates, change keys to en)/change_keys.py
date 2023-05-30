import json

with open('jsons/terms_v0.json') as file:
    dict = json.load(file)

new_dict ={}
# change term key from pt to en
for term, value in dict.items():
    en_terms = value['en'].split(',')
    for en_term in en_terms:
        new_dict[en_term.strip()] = value

# change 'des' to 'des_pt'
for term, value in new_dict.items():
    if 'des' in value:
        des_pt = value.pop('des')
        new_dict[term]['des_pt'] = des_pt
    

with open('jsons/terms_v1.json', 'w') as file:
    json.dump(new_dict, file, ensure_ascii=False, indent=6)
