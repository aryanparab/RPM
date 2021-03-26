from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import requests
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import face_capture
import model

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

file_to_store_upload_docs = 'images'
if os.path.isdir(os.path.join(BASE_DIR,file_to_store_upload_docs)) != True :
	os.mkdir(os.path.join(BASE_DIR,file_to_store_upload_docs))

UPLOAD_FOLDER= os.path.join(BASE_DIR,file_to_store_upload_docs)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']

@app.route("/")
def home_page():
	return render_template('home_demo.html')

def check_fileextension(file):
	if file.split(".")[1] in ALLOWED_EXTENSIONS:
		return True
	else:
		return False
@app.route("/kyc",methods=['POST','GET'])
def check_kyc():
	if request.method == "POST":
		f = request.files["aadhar"]

		if f == '' :
			return render_template('kyc_demo.html',context='Please upload a file')
		
		elif check_fileextension(f.filename):
			f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
			face_capture.perform()
			model.make_model()
			return render_template('kyc_demo.html',context='File Uploaded Successfully')
		
		else:
			return render_template('kyc_demo.html',context='Enter jpg or pdf')

	else:
		return render_template('kyc_demo.html',context = '')

@app.route("/aboutus")
def aboutus():
	return render_template('aboutus_demo.html')

if __name__ == '__main__':
	app.run(debug=True)