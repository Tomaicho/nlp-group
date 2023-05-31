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
            adjectives = []

            for description in descriptions:
                doc = nlp(description)
                for token in doc:
                    if token.pos_ == "NOUN":  # Noun check
                        nouns.append(token.text.lower())
                    elif token.pos_ == "ADJ":  # Adjective check
                        adjectives.append(token.text.lower())

            for noun in nouns:
                if noun in data and noun not in relations and noun != term:
                    relations.append(noun)
                    if 'relations' in data[noun]:
                        relations2 = data[noun]['relations']
                        print(relations2)
                        relations2.append(term)
                        data[noun]["relations"] = relations2
                    else:
                        data[noun] = {'relations': term}

            for adj in adjectives:
                if adj in data and adj not in relations and adj != term:
                    relations.append(adj)
                    if 'relations' in data[adj]:
                        relations2 = data[adj]['relations']
                        relations2.append(term)
                        data[adj]["relations"] = relations2
                    else:
                        data[adj] = {'relations': term}
            data[term]["relations"] = (relations)

    return data

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/terms_v8.json') as file:
    data = json.load(file)

updated_data = find_related_terms(data)

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/terms_v9.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)




