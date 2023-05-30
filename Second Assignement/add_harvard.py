import json

with(open("jsons/terms_v1.json",  encoding="utf-8") as file):
    terms_v1 = json.load(file) 

with(open("jsons/harvard_terms.json",  encoding="utf-8") as file):
    dic_harvard = json.load(file) 

new_terms_added = 0
des_en_added = 0
for term, des_en in dic_harvard.items():
    print(term)
    if term in terms_v1:
        if 'des_en' in terms_v1[term]:
            terms_v1[term]['des_en'].append(des_en.strip())
        elif 'des_en' not in terms_v1[term]:
            terms_v1[term]['des_en'] = [des_en.strip()]
        des_en_added += 1
        print('Added des_en to: ', term)
    elif term not in terms_v1:
        terms_v1[term] = {'des_en':[des_en.strip()]}
        new_terms_added += 1
        print('Added new term:', term)
        
print('Des_en added: ', des_en_added)
print('New terms added: ', new_terms_added)
with open('jsons/terms_v2.json','w') as file:
    json.dump(terms_v1,file, indent=6, ensure_ascii=False)
   