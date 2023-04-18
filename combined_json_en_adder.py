
from deep_translator import GoogleTranslator
import json

translator_pt_to_en = GoogleTranslator(source='pt', target='en')

with(open("JSONs\combined.json",  encoding="utf-8") as file):
    combined = json.load(file) 

for term in combined:
    print(term)
    if "en" not in combined[term]:
        combined[term]["en"] = translator_pt_to_en.translate(term)
        with(open("JSONs\combined2.json", "w",  encoding="utf-8") as file):
            json.dump(combined,file,indent=6, ensure_ascii=False) 