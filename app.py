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
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("index.html")





@app.route('/result', methods=['POST'])
def result():
    response = make_response()
    file=request.files['file']
    filepath = "./uploads"+datetime.now().strftime("%Y%m%d%H%M%S") +".csv"
    global glob_file=filepath

    return render_template("download_csv.html")

@app.route("/download", methods=["POST"])
def download():
    response = make_response()

    return glob_file
#     response.data(csv_file)
#     downloadFileName = file.filename[:-4] +".csv"
#     response.headers["Content-Disposition"] = "attachment; filename=" + downloadFileName
#     return response
    if file == "XXXX":
        return "no!"
    else:
        return "done"


#
#     return 0
#
# def predict(data):#ここで機械学習の処理を行う
#
#     return data

#     return

if __name__ == "__main__" :
    app.debug = True
    app.run(host="localhost")