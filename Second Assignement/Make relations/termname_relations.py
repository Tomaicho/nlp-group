import re, json, spacy

def combinations(combination_list):
    lenght = len(combination_list)
    combined_list = []

    for first_word in range(lenght):
        combination = ''
        for last_word in range(first_word, lenght):
            combination += ' ' + str(combination_list[last_word])
            combined_list.append(combination[1:])
    combined_list.pop(lenght-1)
    return combined_list

file = open('Second assignement/Website/terms_v9_original.json', 'r', encoding='utf-8')
dictionary = json.load(file)
file.close()

nlp = spacy.load("en_core_web_sm")

for search_term, search_value in dictionary.items():
    frase = nlp(search_term)

    if len(frase) > 1:
        combination_list = combinations(frase)
        for segment in combination_list:
            space = " "
            # segments with only one word are converted to their lemma
            if space not in segment:
                segment = nlp(segment)
                segment = segment[0].lemma_
            if segment in dictionary.keys():

                found_term = segment
                found_value = dictionary[found_term]

                try:
                    if found_term not in search_value["relations"]:
                        search_value["relations"].append(found_term)
                except:
                    search_value["relations"] = [found_term]
                
                try:
                    if search_term not in found_value["relations"]:
                        found_value["relations"].append(search_term)
                except:
                    found_value["relations"] = [search_term]

                dictionary[search_term] = search_value
                dictionary[found_term] = found_value

file = open('Second assignement/jsons/terms_v10.json', 'w', encoding='utf-8')
json.dump(dictionary, file, ensure_ascii=False, indent=6)
file.close()