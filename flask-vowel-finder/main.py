from flask import Flask, render_template, request, redirect
from vowelfinder import search4letters

app = Flask(__name__)

def log_request(req:'flask_request', res: str) -> None: 
    with open('vsearch.log', 'a') as log: 
        print(f"The IP Address {req.remote_addr} using the browser name {req.user_agent} inputted {req.form} and the Result was {res}", file=log, sep="|")

@app.route("/")
def home():
    return redirect("/entry")

@app.route("/entry")
def entry():
    return render_template("entry.html", page_title="Entry")

@app.route("/result", methods=["POST"])
def results():
    phrase = request.form["phrase"]
    letter = request.form["letter"]
    result = search4letters(phrase, letter)
    log_request(request, result) 
    return render_template("result.html", phrase=phrase, letter=letter, page_title="Result", result=result)

@app.route("/logWriter")
def log_writer():
    with open("vsearch.log", "r") as log_file:
        content = log_file.readline()
    return content

if __name__ == "__main__":
    app.run(debug=True)

