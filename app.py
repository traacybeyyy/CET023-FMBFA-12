from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])  ## GET and POST from front end
def index(): 
    return(render_template("index.html")) ## html file for front end

@app.route("/main", methods=["GET","POST"])   
def main(): 
    r = request.form.get("q")  ## receive what front end post to backend. random convention: frontend = q, backend = r. refer to PyPi to find out the naming convention
    return(render_template("main.html", r=r)) ## right r = r above (backend), left r is the frontend r  

@app.route("/prediction", methods=["GET","POST"])   
def prediction(): 
    return(render_template("prediction.html")) ## right r = r above (backend), left r is the frontend r  

@app.route("/dbs_price", methods=["GET","POST"])   
def dbs_price(): 
    q = float(request.form.get("q"))  ## receive what front end post to backend. random convention: frontend = q, backend = r. refer to PyPi to find out the naming convention
    return(render_template("dbs_price.html", r=(q*-50.6)+90.2)) ## right r = r above (backend), left r is the frontend r  

if __name__ == "__main__":  
    app.run()
