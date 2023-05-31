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
            nouns_lem = []
            adjectives_lem = []

            for description in descriptions:
                doc = nlp(description)
                for token in doc:
                    if token.pos_ == "NOUN":  # Noun check
                        nouns.append(token.text.lower())
                        nouns_lem.append(token.lemma_.lower())
                    elif token.pos_ == "ADJ":  # Adjective check
                        adjectives.append(token.text.lower())
                        adjectives_lem.append(token.lemma_.lower())
                print(nouns)
                print(nouns_lem)
                print(adjectives)
                print(adjectives_lem)

            for noun in nouns:
                for key in data.keys():
                    if key.lower() == noun and key.lower() not in relations and key != term:
                        data[term]["relations"].append(key)
                        data[key]["relations"].append(term)

            for adj in adjectives:
                for key in data.keys():
                    if key.lower() == adj and key.lower() not in relations and key != term:
                        data[term]["relations"].append(key)
                        data[key]["relations"].append(term)

    return data

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/test.json') as file:
    data = json.load(file)

updated_data = find_related_terms(data)

with open('C:/Users/tomas/Desktop/Mestrado/1A_2S/Processamento Linguagem Natural/nlp-group/Second assignement/jsons/test2.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)




