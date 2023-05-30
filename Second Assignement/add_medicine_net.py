import json

with open('jsons/medicine_net_terms.json') as file:
    medicine_net = json.load(file)

with(open("terms_v3.json") as file):
    terms_v3 = json.load(file) 

new_terms_added = 0
des_en_added = 0
for term, dic in medicine_net.items():
    print(term)
    des_en = dic['des_en']
    relations = dic['relations']
    if term in terms_v3:
        if 'des_en' in terms_v3[term]:
            terms_v3[term]['des_en'] += des_en
        elif 'des_en' not in terms_v3[term]:
            terms_v3[term]['des_en'] = des_en
        des_en_added += 1
        print('Added des_en to: ', term)
        if 'relations' in terms_v3[term]:
            terms_v3[term]['relations'] += relations
        elif 'relations' not in terms_v3[term]:
            terms_v3[term]['relations'] = relations

    elif term not in terms_v3:
        terms_v3[term] = {'des_en': des_en, 'relations': relations}
        new_terms_added += 1
        print('Added new term:', term)
        
print('Des_en added: ', des_en_added)
print('New terms added: ', new_terms_added)
with open('jsons/terms_v4.json','w') as file:
    json.dump(terms_v3, file, indent=6, ensure_ascii=False)