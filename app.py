"""
Author:Efe Akaröz
Date: 3 April 2023
"""


from flask import Flask, render_template, request, abort
import json
import os
import random
from werkzeug.utils import secure_filename
import time

config = json.loads(open("config.json", "r").read())
ALLOWED_EXTENSIONS = config["allowed_extensions"]
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS




app = Flask(__name__)


@app.route("/")
def index():
    return render_template(config["homepage"])


@app.route("/upload", methods=["POST"])
def uploadIt():
    logger = open("file.log", "a")
    if request.method == "POST":
        try:
            ip = request.environ['REMOTE_ADDR'].split(",")[0]
            # ip=request.remote_addr
        except:
            ip = request.environ['HTTP_X_FORWARDED_FOR'].split(",")[0]
        try:
          file = request.files['file']
        except:
          return {"err":"Please specify 'file'."}
        if file and allowed_file(file.filename):
            originalFile = secure_filename(file.filename)
            ext = originalFile.split(".")[1]

            filename = ""
            for i in range(10):
                ca = random.choice(alphabet)
                filename = filename+ca
                addNorNot = random.randint(0, 1)
                if addNorNot == 1:
                    filename = filename + str(random.randint(12, 120))

            try:
                file.save("static/"+filename+"."+ext)
                logger.write(f"UPLOAD {ip} | "+originalFile+" @" +
                             str(time.time())+" as "+filename+"."+ext+"\n")
                return {"file": filename+"."+ext, "time": time.time(), "ctime": time.ctime(time.time())}

            except Exception as e:
                return {"err": str(e)}
        else:
          return {"err":"File type is not allowed in this server","allowedFileTypes":ALLOWED_EXTENSIONS,"maxSize":"10MB"}
    logger.close()
@app.route("/delete/<filename>", methods=["DELETE"])
def deleteit(filename):
    logger = open("file.log", "a")
    try:
        ip = request.environ['REMOTE_ADDR'].split(",")[0]
        # ip=request.remote_addr
    except:
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(",")[0]

    if "*" in filename or ".." in filename or "/" in filename:
        return abort(403)
    try:
        open(f"static/{filename}", "r")
    except:
        return {"err": "File does not exist"}
    os.system(f"rm static/{filename}")
    logger.write(f"DELETE {ip} | {filename} {time.time()}  \n")
    return {"message": "Delete Successfull", "filename": filename}

    logger.close()
if __name__ == "__main__":
  app.run(debug=True,port="2012")
