import json
import spacy

def delte_LOCs(old_data):
    nlp = spacy.load("en_core_web_md") 
    data = {}
    for term, dic in old_data.items():
        term = term.lower()
        if 'relations' in dic:
            relations = dic['relations']
            relations_list = []
            for relation in relations:
                relations_list.append(relation.lower())
            dic['relations'] = relations_list

       
        add = True
        av = nlp(term)
        for ent in av.ents:
            if ent.label_ == 'LOC': #ent.label_ == 'GPE' or 
                print(ent.text)
                add = False
        if add == True:
            data[term]= dic
    return data
        


with open('jsons/terms_v7.json') as file:
    data = json.load(file)

updated_data = delte_LOCs(data)

with open('jsons/terms_v8.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)