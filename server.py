from flask import Flask, render_template, request,make_response, redirect, url_for, send_from_directory
import numpy as np
import cv2
from datetime import datetime
import pandas as pd
import os
import string
import copy
from PIL import Image
glob_file= "XXXX"
glob_file_name="XXX"
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")





@app.route('/result', methods=['POST'])
def result():
    response = make_response()
    file=request.files['file']
    filepath = datetime.now().strftime("%Y%m%d%H%M%S") +".csv"
    file_name=file.filename[:-4]
    file.save("./static/"+filepath)
    global glob_file
    global glob_file_name
    glob_file_name =file_name
    glob_file = filepath

    return render_template("download_csv.html")

@app.route("/download", methods=["POST"])
def download():
    ret_filepath = glob_file
    ret_filename=glob_file_name
    response = make_response()
    response.data = open("./static/"+ret_filepath, "rb").read()
    response.minetype="text/csv"
    downloadFileName =  ret_filename+ '.csv'
    response.headers['Content-Disposition'] = 'attachment; filename=' + downloadFileName



if __name__ == "__main__" :
    app.debug = True
    app.run(host="localhost")