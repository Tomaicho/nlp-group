from flask import Flask, render_template, request
import json

app = Flask(__name__)

with open("./trabalho-grupo/webpage/terms.json", encoding="utf-8") as file:
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
    return render_template("term.html", designation = t, value= db.get(t,"None"))

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

if __name__ == '__main__':
    app.run(host="localhost", port=3000, debug=False)