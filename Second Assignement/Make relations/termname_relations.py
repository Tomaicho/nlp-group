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

file = open('./trabalho-grupo-2/Second Assignement/jsons/terms_v6.json', 'r', encoding='utf-8')
dictionary = json.load(file)
file.close()

nlp = spacy.load("en_core_web_sm")

for search_term, search_value in dictionary.items():
    frase = nlp(search_term)

    if len(frase) > 1:
        # print(f'F {frase} - 1 {frase[0]} - 2 {frase[1]}')
        combination_list = combinations(frase)
        for segment in combination_list:
            if segment in dictionary.keys():
                # print(f'found: {search_term} - {segment}')

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

file = open('./trabalho-grupo-2/Second Assignement/jsons/terms_v7.json', 'w', encoding='utf-8')
json.dump(dictionary, file, ensure_ascii=False, indent=6)
file.close()