from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("Website/terms_v9.json") as file:
    db = json.load(file)

keys = list(db.keys())
keys = [term.strip() for term in keys]
keys = sorted(keys, key=str.casefold)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/terms")
def terms():
    return render_template("terms.html", designations=keys)

@app.route("/term/<t>")
def term(t):
    relations = []
    dic = db.get(t)
    if dic.get('relations') is not None:
        relations = dic.get('relations')
        relations_in_db = [term for term in relations if term in db]
        for relation in relations_in_db:
            relations.append(relation)
    
    return render_template("term.html", designation = t, relations=relations, value= db.get(t,"None"))

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

@app.route('/categories/<term>')
def categories(term):
    important_terms = ['anatomy', 'bacteria', 'blood', 'cancer', 'cell', 'diagnosis', 'disease', 'dna', 'drug', 'epidemic',
    'fever', 'gene', 'heart', 'hormone', 'immune', 'infection', 'inflammation', 'injury', 'kidney', 'liver',
    'lung', 'microscope', 'nerve', 'organ', 'pain', 'pathology', 'patient', 'pharmacy', 'physician', 'radiation',
    'research', 'surgery', 'symptom', 'therapy', 'tissue', 'treatment', 'vaccine', 'virus', 'wound']
    important_terms_in_db = [term for term in important_terms if term in db]
    new_relations = set()
    if term =='base':
        new_relations = set(important_terms_in_db)
    else:
        dic = db.get(term)
        if dic.get('relations') is not None:
            relations = dic.get('relations')
            relations_in_db = [term for term in relations if term in db]
            for relation in relations_in_db:
                new_relations.add(relation)
    
    new_relations = sorted(list(new_relations))
        
    return render_template('categories.html', terms = new_relations)

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=False)

