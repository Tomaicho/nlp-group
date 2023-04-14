from flask import Flask, render_template
import json
app = Flask(__name__)

file = open("C:\Users\DIGUEST-ASUS\Desktop\PLNEB\First assignment\nlp-group\webpage\terms.json", encoding="utf-8")

db = json.load(file) 

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/terms")
def terms():
    return render_template("terms.html", designations=db.keys())


@app.route("/term/<t>")
def term(t):
    return render_template("term.html", designation = t, value= db.get(t,"None"))

app.run(host="localhost", port=3000, debug=True)
