from flask import Flask, render_template, request, g
import json, spacy

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

def make_relations(term):
    nlp = spacy.load("en_core_web_sm")

    for search_term, search_value in db.items():
        frase = nlp(search_term)

        if len(frase) > 1:
            # print(f'F {frase} - 1 {frase[0]} - 2 {frase[1]}')
            combination_list = combinations(frase)
            for segment in combination_list:
                if segment in db.keys():
                    # print(f'found: {search_term} - {segment}')

                    found_term = segment
                    found_value = db[found_term]

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

                    db[search_term] = search_value
                    db[found_term] = found_value

app = Flask(__name__)

try:
    with open('./Second Assignement/Website/terms_v9_modified.json') as file:
        db = json.load(file)
except:
    with open('./Second Assignement/Website/terms_v9_original.json') as file:
        db = json.load(file)

try:
    with open('./Second Assignement/Website/category_modified.json') as file:
        important_terms = json.load(file)
except:
    with open('./Second Assignement/Website/category_original.json') as file:
        important_terms = json.load(file)

keys = list(db.keys())
keys = [term.strip() for term in keys]
keys = sorted(keys, key=str.casefold)

@app.before_first_request
def before_first_request():
    app.config['start'] = 46500
    app.config['jump'] = 100
    app.config['length'] = len(db)
    if app.config['start'] + app.config['jump'] > app.config['length']:
        app.config['end'] = app.config['length']
    else:
        app.config['end'] = app.config['start'] + app.config['jump']

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/terms")
def terms():
    keys = list(db.keys())
    keys = [term.strip() for term in keys]
    keys = sorted(keys, key=str.casefold)
    return render_template("terms.html", designations=keys[app.config['start']:app.config['end']], start=app.config['start']+1, end=app.config['end'], length=app.config['length'])

@app.route("/terms/change/<direction>", methods=["GET"])
def change(direction):
    if direction == 'next':
        app.config['start'] = app.config['start'] + app.config['jump']
        app.config['end'] = app.config['start'] + app.config['jump']
        if app.config['end'] > app.config['length']:
            app.config['start'] = app.config['start'] - app.config['jump']
            app.config['end'] = app.config['length']
    elif direction == 'prev':
        app.config['start'] = app.config['start'] - app.config['jump']
        app.config['end'] = app.config['start'] + app.config['jump']
        if app.config['start'] < 0:
            app.config['start'] = 0
            app.config['end'] = app.config['start'] + app.config['jump']
    else:
        index = int(direction)-1
        app.config['start'] = index
        app.config['end'] = app.config['start'] + app.config['jump']
        if app.config['end'] > app.config['length']:
            app.config['start'] = app.config['length'] - app.config['jump']
            app.config['end'] = app.config['length']
        elif app.config['start'] < 0:
            app.config['start'] = 0
            app.config['end'] = app.config['jump']

    return {'success': True}

@app.route("/term/<t>")
def term(t):
    relations_ = []
    dic = db.get(t)
    if dic.get('relations') is not None:
        relations = dic.get('relations')
        relations_in_db = [term for term in relations if term in db.keys()]
        print(relations)
        print(relations_in_db)
        for relation in relations_in_db:
            relations_.append(relation)
    
    return render_template("term.html", designation = t, relations=relations_, value= db.get(t,"None"))

@app.route("/term", methods=["POST"])
def add_term():
    term = request.form["term"]
    pt = request.form["trad-pt"]
    es = request.form["trad-es"]
    de = request.form["trad-de"]
    des_en = request.form["description-en"]
    des_pt = request.form["description-pt"]
    
    if term!='' and term not in db:
        value = {}
        if pt !='':
            value['pt']=pt
        value['en']=term
        if es !='':
            value['es']=es
        if de !='':
            value['de']=de
        if es !='':
            value['es']=es
        if des_en !='':
            value['des_en']=des_en.split('\n')
        if des_pt !='':
            value['des_pt']=des_pt.split('\n')
        db[term.lower().strip()]=value

        file = open('./Second Assignement/Website/terms_v9_modified.json', "w")
        json.dump(db, file, ensure_ascii=False, indent=4)
        file.close()

        app.config['length'] = len(db)

        keys = list(db.keys())
        keys = [term.strip() for term in keys]
        keys = sorted(keys, key=str.casefold)
        return render_template("terms.html", designations=keys[app.config['start']:app.config['end']], start=app.config['start']+1, end=app.config['end'], length=app.config['length'],
                               info_add="The term " + term + " was added!")

    keys = list(db.keys())
    keys = [term.strip() for term in keys]
    keys = sorted(keys, key=str.casefold)
    if term=='':
        info = "The term field needs to be filled!"
    else:
        info = "The term " + term + " already exists!"
    return render_template("terms.html", designations=keys[app.config['start']:app.config['end']], start=app.config['start']+1, end=app.config['end'], length=app.config['length'],
                           info_add=info)

@app.route("/term/<term>", methods=["DELETE"])
def delete_term(term):
    if term in db:
        old_value = db[term]

        del db[term]

        file = open('./Second Assignement/Website/terms_v9_modified.json', "w")
        json.dump(db, file, ensure_ascii=False, indent=4)
        file.close()

        app.config['length'] = len(db)

        return {"success": True, "deleted": {term: old_value}}

    return {"success": False, "info": "The entry " + term + " does not exists!"}

@app.route("/search")
def search():
    search_term = request.args.get('user_input')

    results = []
    if search_term:
        for key in db:
            if search_term.casefold() in key.casefold():
                results.append(key)

    results = [term.strip() for term in results]
    results = sorted(results, key=str.casefold)

    return render_template("search.html", results=results, search_term=search_term)

@app.route('/categories')
def categories():
    important_terms_in_db = [term for term in important_terms if term in db]
    new_relations = set()
    new_relations = set(important_terms_in_db)
    new_relations = sorted(list(new_relations))
        
    return render_template('categories.html', terms = new_relations)

@app.route("/categories", methods=["POST"])
def add_category():
    term = request.form["term"]

    if term not in important_terms:
        important_terms.append(term)

        file = open('./Second Assignement/Website/category_modified.json', "w")
        json.dump(important_terms, file, ensure_ascii=False, indent=4)
        file.close()
        important_terms_in_db = [term for term in important_terms if term in db]
        new_relations = set(important_terms_in_db)
        new_relations = sorted(list(new_relations))
        return render_template("categories.html", terms = new_relations,
                               info_add="The category " + term + " was added!")

    important_terms_in_db = [term for term in important_terms if term in db]
    new_relations = set(important_terms_in_db)
    new_relations = sorted(list(new_relations))
    return render_template("categories.html", terms = new_relations,
                           info_add="The category " + term + " already exists!")

@app.route("/categories/<term>", methods=["DELETE"])
def delete_category(term):
    if term in important_terms:
        old_value = term

        important_terms.remove(term)

        file = open('./Second Assignement/Website/category_modified.json', "w")
        json.dump(important_terms, file, ensure_ascii=False, indent=4)
        file.close()

        return {"success": True, "deleted": {"category": old_value}}

    return {"success": False, "info": "The category " + term + " does not exists!"}

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=False)

