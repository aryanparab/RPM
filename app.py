from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import requests
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import face_capture
import model
import get_aadhar_text

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

file_to_store_upload_docs = 'images'
if os.path.isdir(os.path.join(BASE_DIR,file_to_store_upload_docs)) != True :
	os.mkdir(os.path.join(BASE_DIR,file_to_store_upload_docs))

UPLOAD_FOLDER= os.path.join(BASE_DIR,file_to_store_upload_docs)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
file_dict ={0:'aadhar',1:'pan',2:'dl'}

@app.route("/")
def home_page():
	return render_template('home.html')



@app.route('/kyc_video',methods=['POST','GET'])
def check_video_face():
	if request.method == "POST":
		face_capture.perform()
		model.make_model()

		return render_template('video_kyc.html',context = "Model created Successfully")
	else:
		return render_template('video_kyc.html',context ='')

def check_fileextension(file):
	if file.endswith('.pdf') or file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
		return True
	else:
		return False

@app.route("/kyc",methods=['POST','GET'])
def check_kyc():
	if request.method == "POST":
		f_aadhar = request.files["aadhar"]
		f_pan = request.files["pan"]
		f_dl = request.files["dl"]
		files = [f_aadhar,f_pan,f_dl]
		no_of_files = 0
		file_names = []
		for no,f in enumerate(files):
			
			if f.filename == '' and no == 0:

				return render_template('kyc_docs.html',context='Please upload Aadhar Card file')
		
			elif check_fileextension(f.filename):
				no_of_files = 1
				f.filename = file_dict[no]+'.jpg'
				file_names.append(f.filename)
				f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
				
			elif no_of_files == 0:
				aadhar_data = ()
				return render_template('kyc_docs.html',context='Enter jpg or pdf')

		if no_of_files > 0:
			aadhar_data = get_aadhar_text.get_data(os.path.join(BASE_DIR,'images',file_names[0]))
			print(aadhar_data)
			return redirect(url_for('check_video_face'))
		
	else:
		return render_template('kyc_docs.html',context = '')

	

@app.route("/aboutus")
def aboutus():
	return render_template('aboutus_demo.html')

if __name__ == '__main__':
	app.run(debug=True)