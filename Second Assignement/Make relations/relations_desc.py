import json
import spacy

def find_related_terms(data):
    nlp = spacy.load("en_core_web_md") 

    for term in data:
        if "des_en" in data[term]:
            descriptions = data[term]["des_en"]
            if 'relations' in data[term]:
                relations = data[term]['relations']
            else:
                relations = []
                data[term]['relations'] = relations
            nouns = []

            for description in descriptions:
                doc = nlp(description)
                for token in doc:
                    if token.pos_ == "NOUN" or token.pos_ == "ADJ":
                        nouns.append(token.text.lower())

            for noun in nouns:
                if noun in data:
                    if noun not in relations and noun != term:
                        relations.append(noun)

                    if 'relations' in data[noun]:
                        relations2 = data[noun]["relations"]
                        if term not in relations2 and term != noun:  
                            relations2.append(term)
                            data[noun]["relations"] = relations2
                    else:
                        data[noun] = {"relations": [term]}

                    
                

            data[term]["relations"] = (relations)

    return data

with open('Second assignement/jsons/terms_v10.json') as file:
    data = json.load(file)

updated_data = find_related_terms(data)

with open('Second assignement/jsons/terms_v11.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)




