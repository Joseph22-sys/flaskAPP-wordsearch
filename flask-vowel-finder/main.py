from flask import Flask, render_template, request, redirect
from vowelfinder import search4letters
import mysql.connector 


dbconfig = { 
            'host': '127.0.0.1', 
            'user': 'root', 
            'password': 'personal_tin', 
            'database': 'vsearchdb', 
        }
         

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()


app = Flask(__name__)

def log_request(req: 'flask_request', res: str) -> None:
    """Log details of the web request and the results."""
    try:
        browser_string = req.user_agent.browser or 'Unknown'
        
        _SQL = """insert into log (phrase, letters, ip, browser_string, results) 
                  values (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'], req.form['letter'], 
                              req.remote_addr,browser_string, res))
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Error logging request: {e}")
    


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
    result = str(search4letters(phrase, letter))
    log_request(request,result)
    return render_template("result.html", phrase=phrase, letter=letter, page_title="Result", result=result)


    
@app.route("/viewlogs")
def viwelog():
    _SQL = """select * from log"""
    cursor.execute(_SQL)
    return cursor.fetchall()


if __name__ == "__main__":
    app.run(debug=True)


