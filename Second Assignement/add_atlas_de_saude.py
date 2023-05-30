import json

with open('jsons/atlas_de_saude_terms.json') as file:
    atlas_de_saude = json.load(file)

with(open("terms_v4.json") as file):
    terms_v4 = json.load(file) 

new_des_pt_added = 0
des_pt_added = 0
for term_pt, dic in atlas_de_saude.items():
    print(term_pt)
    des_pt = dic['page']
    for term_en, dic_v4 in terms_v4.items():
        if 'pt' in dic_v4 and term_pt in dic_v4['pt']:
            if 'des_pt' in dic_v4:
                terms_v4[term_en]['des_pt'].append(des_pt)
                des_pt_added += 1
                print('Added des_en to: ', term_pt)
            else:
                terms_v4[term_en]['des_pt'] = [des_pt]
                new_des_pt_added += 1
                print('New des pt added to: ', term_pt)

        
print('Des_pt added: ', des_pt_added)
print('New des pt added: ', new_des_pt_added)
with open('jsons/terms_v5.json','w') as file:
    json.dump(terms_v4, file, indent=6, ensure_ascii=False)

#Des_pt added:  0
#New des pt added:  1 (Alzheimer)