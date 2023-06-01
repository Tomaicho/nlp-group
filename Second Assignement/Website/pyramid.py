import json
from collections import Counter

with open("jsons/terms_v9.json") as file:
    db = json.load(file)

#important_terms = ["Anatomy", "Physiology", "Disease", "Diagnosis", "Treatment", "Medication", "Surgery", "Patient", "Doctor", "Nurse", "Hospital", "Medical research", "Immunology", "Cardiology", "Oncology", "Pediatrics", "Neurology", "Psychiatry", "Epidemiology", "Public health"]
#important_terms_in_db = [x for x in important_terms if x in db] #['Anatomy', 'Physiology', 'Disease', 'Diagnosis', 'Medication', 'Surgery', 'Doctor', 'Nurse', 'Hospital', 'Immunology', 'Cardiology', 'Pediatrics', 'Neurology', 'Psychiatry', 'Epidemiology']

# Do we actually need the pyramid? Best would be to just start with the most important terms in a list. Then on click display the relations
'''
#Top-Down
def make_layer(upstream_layer):
    new_layer = set()
    for term in upstream_layer:
        if db.get(term) is not None:
            dic = db.get(term)
            if dic.get('relations') is not None:
                for relation in dic.get('relations'):
                    relation_Upper = relation[:1].upper()+relation[1:]
                    if relation in db:
                        new_layer.add(relation)
                    elif relation_Upper in db:
                        new_layer.add(relation_Upper)
    return new_layer

def pyramid(peak, layers):
    layer = peak
    for i in range(layers):
        layer = make_layer(layer)
        print(f"""Size of {i}th layer is {len(layer)}
Keys of this layer are: {layer}""", end='\n\n')
                 
pyramid(important_terms_in_db, 10)

'''
#Bottom-Up:
def make_layer(sub_layer):
    relations = [] 
    layer = {}
    for term, dic in sub_layer.items():
        if dic.get('relations') is not None:
            relations.extend([x for x in dic.get('relations')])
    fraction = round(0.314 * len(relations))
    relations_counter = Counter(relations).most_common(fraction)
    for term, count in relations_counter:
        if term in db:
            layer[term] = db[term]
    return layer

def pyramid(database, layers):
    layer = database
    for i in range(layers):
        layer = make_layer(layer)
        print(f"""Size of {i}th layer is {len(layer)}
Keys of this layer are: {layer.keys()}""")
        

pyramid(db, 20)
