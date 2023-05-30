import json

with open('jsons/medi_dict_online_terms.json') as file:
    medi_dic_online = json.load(file)

with(open("jsons/terms_v2.json") as file):
    terms_v2 = json.load(file) 

new_terms_added = 0
des_en_added = 0
for term, dic in medi_dic_online.items():
    print(term)
    des_en = dic['des_en']
    relations = dic['relations']
    if term in terms_v2:
        if 'des_en' in terms_v2[term]:
            terms_v2[term]['des_en'].append(des_en.strip())
        elif 'des_en' not in terms_v2[term]:
            terms_v2[term]['des_en'] = [des_en.strip()]
        des_en_added += 1
        print('Added des_en to: ', term)
        terms_v2[term]['relations'] = relations
    elif term not in terms_v2:
        terms_v2[term] = {'des_en':[des_en.strip()], 'relations':relations}
        new_terms_added += 1
        print('Added new term:', term)
        
print('Des_en added: ', des_en_added)
print('New terms added: ', new_terms_added)
with open('jsons/terms_v3.json','w') as file:
    json.dump(terms_v2,file, indent=6, ensure_ascii=False)