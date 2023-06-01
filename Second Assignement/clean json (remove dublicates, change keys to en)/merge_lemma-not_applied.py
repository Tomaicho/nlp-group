import json
import spacy

def merge_lemma(old_data):
    nlp = spacy.load("en_core_web_md") 
    data = {}
    for term, dic in old_data.items():
        print(term)
        term = term.lower()
        av = nlp(term)
        term_lemma = ''
        for token in av:
            term_lemma += ' '+token.lemma_
        print(term_lemma,end='\n\n')
        if term_lemma not in data:
            data[term_lemma] = dic
        elif  term_lemma in data and term==term_lemma:
            for key in dic.keys():
                if key in ['des_en', 'des_pt', 'relations']:
                    if key not in data[term_lemma]:
                        data[term_lemma][key] = dic[key]
                    else:
                        data[term_lemma][key] += dic[key]
                else: #translations
                    data[term_lemma][key] = dic[key]

        elif  term_lemma in data and term!=term_lemma:
            for key in dic.keys():
                if key in ['des_en', 'des_pt', 'relations']:
                    if key not in data[term_lemma]:
                        data[term_lemma][key] = dic[key]
                    else:
                        data[term_lemma][key] += dic[key]

    return data
        

with open('jsons/terms_v7.json') as file:
    data = json.load(file)

updated_data = merge_lemma(data)

with open('jsons/terms_v8.json','w') as file:
    json.dump(updated_data, file, indent=6, ensure_ascii=False)




