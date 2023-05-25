from deep_translator import GoogleTranslator
import json

translator_pt_to_de = GoogleTranslator(source='pt', target='de')

with(open("/Users/florianhetzel/Desktop/PLNEB/Practical/Second assignment/terms.json",  encoding="utf-8") as file):
    dict = json.load(file) 

for term in dict:
    print(term)
    if "de" not in dict[term]:
        dict[term]["de"] = translator_pt_to_de.translate(term)
        with(open("terms_with_de.json", "w",  encoding="utf-8") as file):
            json.dump(dict,file,indent=6, ensure_ascii=False) 