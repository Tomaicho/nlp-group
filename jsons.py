import json
with open('./Second Assignement/Website/terms_v9_modified.json') as file:
    db = json.load(file)
    print(len(db))