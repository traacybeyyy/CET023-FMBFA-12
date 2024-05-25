from flask import Flask, render_template, request
import google.generativeai as palm
import replicate
import os 
import sqlite3 
import datetime 
# from flask import Markup
from markupsafe import Markup 

flag = 1 ## to prevent repeated fetching attempts resulting in None in subsequent tries when retrieving name
name = ""

makersuite_api = os.getenv("MAKERSUITE_API_TOKEN")
palm.configure(api_key=makersuite_api)

model = {"model" : "models/chat-bison-001"}
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])  ## GET and POST from front end
def index(): 
    return(render_template("index.html")) ## html file for front end

@app.route("/main", methods=["GET","POST"])   
def main(): 
    global flag, name 
    if flag == 1: ## fetch once only so that when returning to main page it will still be there
        name = request.form.get("q") ## get the name (input)  ## receive what front end post to backend. random convention: frontend = q, backend = r. refer to PyPi to find out the naming convention
        current_time = datetime.datetime.now()
        conn = sqlite3.connect('log.db')
        c = conn.cursor()
        c.execute("insert into user (name, time) values (?,?)", (name ,current_time))
        conn.commit()
        c.close()
        conn.close()
        flag = 0 
    return(render_template("main.html", r=name)) ## right r = r above (backend), left r is the frontend r  

@app.route("/prediction", methods=["GET","POST"])   
def prediction(): 
    return(render_template("prediction.html")) ## right r = r above (backend), left r is the frontend r  

@app.route("/dbs_price", methods=["GET","POST"])   
def dbs_price(): 
    q = float(request.form.get("q"))  ## receive what front end post to backend. random convention: frontend = q, backend = r. refer to PyPi to find out the naming convention
    return(render_template("dbs_price.html", r=(q*-50.6)+90.2)) ## right r = r above (backend), left r is the frontend r  

@app.route("/generate_text", methods=["GET","POST"]) 
def generate_text(): 
    return(render_template("generate_text.html")) 

@app.route("/text_result_makersuite", methods=["GET","POST"])   
def text_result_makersuite(): 
    q = request.form.get("q")
    r = palm.chat(**model, messages = q)
    return(render_template("text_result_makersuite.html", r=r.last)) 

@app.route("/generate_image", methods=["GET","POST"]) 
def generate_image(): 
    return(render_template("generate_image.html")) 

@app.route("/image_result", methods=["GET","POST"])   
def image_result(): 
    q = request.form.get("q")
    r = replicate.run("stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
                    input = {"prompt":q}
                    )
    return(render_template("image_result.html", r=r[0])) 

@app.route("/log", methods=["GET","POST"]) 
def log(): 
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute("select * from user")
    r = ""
    for row in c:
       r += str(row) + "<br>"
    print(r)
    r = Markup(r)
    c.close()
    conn.close()
    return(render_template("log.html", r=r)) 

@app.route("/delete", methods=["GET","POST"]) 
def delete(): 
    conn = sqlite3.connect('log.db')
    c = conn.cursor()
    c.execute("delete from user")
    conn.commit()
    c.close()
    conn.close()
    return(render_template("delete.html")) 

@app.route("/end", methods=["GET","POST"]) 
def end(): 
    global flag 
    flag = 1 
    return(render_template("index.html"))


if __name__ == "__main__":  
    app.run()
