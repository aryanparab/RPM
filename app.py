from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import requests
import os
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER= os.path.join(BASE_DIR,'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home_page():
	return render_template('home_demo.html')

@app.route("/kyc",methods=['POST','GET'])
def check_kyc():
	if request.method == "POST":
		f = request.files["aadhar"]
		if f == '':
			return render_template('kyc_demo.html',context='Please upload a file')
		f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
		return render_template('kyc_demo.html',context='File Uploaded Successfully')
	else:
		return render_template('kyc_demo.html',context = '')

@app.route("/aboutus")
def aboutus():
	return render_template('aboutus_demo.html')

if __name__ == '__main__':
	app.run(debug=True)