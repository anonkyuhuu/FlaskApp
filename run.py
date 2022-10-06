from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import shutil

try: shutil.rmtree("__pycache__")
except: pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///employes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db = SQLAlchemy(app)

class Employe(db.Model):
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  email = db.Column(db.String)
  phone = db.Column(db.String)
  
  def __init__(self, name, email, phone):
    self.name = name
    self.email = email
    self.phone = phone

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "GET":
    all_data = Employe.query.all()
    return render_template("index.html", employes=all_data)
  else:
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    myData = Employe(name, email, phone)
    db.session.add(myData)
    db.session.commit()
    return redirect("/")
 
@app.route("/edit/<id>", methods=["POST", "GET"])
def edit(id):
  if request.method == "POST":
    update = Employe.query.get(request.form.get("id"))
    update.name = request.form["name"]
    update.email = request.form["email"]
    update.phone = request.form["phone"]
    db.session.commit()
    return redirect("/")
  else:
    employes = Employe.query.all()
    return render_template("index.html", employes=employes)

@app.route("/delete/<id>")   
def deletes(id):
  deleted = Employe.query.get(id)
  db.session.delete(deleted)
  db.session.commit()
  return redirect("/")
  
  
if __name__ == "__main__":
  db.create_all()
  app.run(host="0.0.0.0",port=5000, debug=True)

#MADE BY ANONK
