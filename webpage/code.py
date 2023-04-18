from flask import Flask, render_template
import json
app = Flask(__name__)

with(open("webpage\\terms.json", encoding="utf-8") as file):
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

app.run(host="localhost", port=3000, debug=False)

