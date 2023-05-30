import json

with open('jsons/terms_v5.json') as file:
    dic = json.load(file)

print(f'Lenght before: {len(dic)}')

for term in list(dic):
    if term in dic:
        term_dic = dic.pop(term)
        terms_casefold = [i.casefold() for i in dic.keys()]
        terms_normal = list(dic.keys())
        if term.casefold() in terms_casefold: #true if duplicate
            index = terms_casefold.index(term.casefold())
            duplicate_term = terms_normal[index]
            dup_term_dic = dic.pop(duplicate_term)
            if duplicate_term[:1].isupper: # change variable assignment so that the upper case term is retained while lower case term is poped
                term, duplicate_term = duplicate_term, term
                term_dic, dup_term_dic = dup_term_dic, term_dic

            for key in dup_term_dic.keys():
                if key in ['des_en', 'des_pt', 'relations']:
                    if key not in term_dic:
                        term_dic[key] = dup_term_dic[key]
                    else:
                        term_dic[key] += dup_term_dic[key]
                else:
                    if key not in term_dic:
                        term_dic[key] = dup_term_dic[key]
                    elif term_dic[key].lower() != dup_term_dic[key].lower():
                        term_dic[key] += ', ' + dup_term_dic[key]
            
            dic[term] = term_dic
        else:
            dic[term] = term_dic
    else: print('Term not found: ', term)

print(f'Lenght after: {len(dic)}')

from more_itertools import locate

def find_indices(list_to_check, item_to_find):
    indices = locate(list_to_check, lambda x: x == item_to_find)
    return list(indices)

for term, term_dic in dic.items():   #remove relations to self
    if 'relations' in term_dic:
        new_relations = []
        relations_casefold = [relation.casefold() for relation in term_dic['relations']]
        relations_normal = term_dic['relations']
        if term.casefold() in relations_casefold:
            indices = find_indices(relations_casefold, term.casefold())
            new_relations = [relations_normal[i] for i in range(len(relations_normal)) if i not in indices]
        dic[term]['relations'] = new_relations



with open('jsons/terms_v6.json', 'w') as file:
    dic = json.dump(dic, file, ensure_ascii=False, indent=6)