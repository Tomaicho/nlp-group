from collections import Counter
import json

file = open('./Second Assignement/jsons/terms_v11.json', 'r', encoding='utf-8')
database = json.load(file)
file.close()

term_num_relations = {}
for term, value in database.items():
    try:
        term_num_relations[term] = len(value["relations"])
    except:
        term_num_relations[term] = 0

top=10
relation_counter = Counter(term_num_relations)
print(f'Top {top} relations:')
num=0
for relation in relation_counter.most_common(top):
    num += 1
    print(f'{num} - ({relation[1]}) {relation[0]}')