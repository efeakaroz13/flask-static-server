from flask import Flask,render_template,request
import json
import os
import random
from werkzeug import secure_filename

config = json.loads(open("config.json","r").read())
ALLOWED_EXTENSIONS = config["allowed_extensions"]

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
  
  
app = Flask(__name__)
@app.route("/")
def index():
  return render_template(config["homepage"])

@app.route("/upload",methods=["POST"])
if request.method == "POST":
  file = request.files['file']
  if file and allowed_file(file.filename):
    
    filename = ""

    try:
        file.save("static/"+filename)
    except Exception as e:
        return {"err":str(e)}
