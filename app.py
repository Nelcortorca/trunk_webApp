from flask import Flask, render_template, request,make_response, redirect, url_for, send_from_directory
import numpy as np
from datetime import datetime
import pandas as pd
import os
import string
import copy
from prediction import pred

glob_file= "XXXX"
glob_file_name="XXX"
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")





@app.route('/result', methods=['POST'])
def result():
    file=request.files['file']
    filepath = datetime.now().strftime("%Y%m%d%H%M%S") +".csv"
    file_name=file.filename
    file.save("./static/"+filepath)


    global glob_file
    global glob_file_name
    glob_file_name =file_name
    glob_file = pred("./static/"+filepath)

    return render_template("download_csv.html")

@app.route("/download", methods=["POST"])
def download():
    ret_filepath = glob_file
    ret_filename=glob_file_name
    response = make_response()
    response.data = open(ret_filepath, "rb").read()
    response.minetype="text/csv"
    downloadFileName =  ret_filename
    response.headers['Content-Disposition'] = 'attachment; filename=' + "predicted_"+downloadFileName
    return response


if __name__ == "__main__" :
    app.debug = True
    app.run(host="localhost")