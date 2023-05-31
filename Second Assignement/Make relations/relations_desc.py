import json
import spacy

def find_related_terms(data):
    nlp = spacy.load("en_core_web_md") 

    for term in data:
        if "des_en" in data[term]:
            descriptions = data[term]["des_en"]
            relations = data[term]["relations"]
            nouns = []
            adjectives = []

            for description in descriptions:
                doc = nlp(description)
                for token in doc:
                    if token.pos_ == "NOUN":  # Noun check
                        nouns.append(token.lemma_.lower())
                    elif token.pos_ == "ADJ":  # Adjective check
                        adjectives.append(token.lemma_.lower())

            for noun in nouns:
                if noun in data and noun not in relations and noun != term:
                    data[term]["relations"].append(noun)
                    data[noun]["relations"].append(term)

            for adj in adjectives:
                if adj in data and adj not in relations and adj != term:
                    data[term]["relations"].append(adj)
                    data[adj]["relations"].append(term)

    return data

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/test.json') as file:
    data = json.load(file)

updated_data = find_related_terms(data)

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/test2.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)




