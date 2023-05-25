'''import spacy
import json

nlp = spacy.load("en_ner_bionlp13cg_md")

with open('terms.json') as file:
    data = json.load(file)

en_terms = []
for term in list(data.keys())[:20]:
    en = data[term]['en']
    en_terms.append(str(en))

print(en_terms,'\n####')

text = ' , '.join(en_terms)
print(text,'\n####')

doc = nlp(text)

for ent in doc.ents:
    print(ent.text, 'label: ', ent.label_)'''
import medspacy
from medspacy.ner import TargetRule
import json

# Load medspacy model
nlp = medspacy.load()
print(nlp.pipe_names)

with open('/Users/florianhetzel/Desktop/PLNEB/Practical/Second assignment/terms.json') as file:
    data = json.load(file)

en_terms = []
for term in list(data.keys())[:20]:
    en = data[term]['en']
    en_terms.append(str(en))

print(en_terms,'\n####')

text = ' , '.join(en_terms)
print(text,'\n####')

# Add rules for target concept extraction
target_matcher = nlp.get_pipe("medspacy_target_matcher")
target_rules = [
    TargetRule("atrial fibrillation", "PROBLEM"),
    TargetRule("atrial fibrillation", "PROBLEM", pattern=[{"LOWER": "afib"}]),
    TargetRule("pneumonia", "PROBLEM"),
    TargetRule("Type II Diabetes Mellitus", "PROBLEM", 
              pattern=[
                  {"LOWER": "type"},
                  {"LOWER": {"IN": ["2", "ii", "two"]}},
                  {"LOWER": {"IN": ["dm", "diabetes"]}},
                  {"LOWER": "mellitus", "OP": "?"}
              ]),
    TargetRule("warfarin", "MEDICATION"),
    TargetRule("absorption", "Biological process"),
    TargetRule('abscess','Patology')
]
target_matcher.add(target_rules)


print('break')

doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)