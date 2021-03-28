from flask import Flask, render_template, url_for, request, redirect, session
import numpy as np
import requests
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import face_capture
import model
import get_aadhar_text,get_pan_data , get_license_data, get_qr_details
import cv2
import send_otp
from flask_session import Session
import json
from fuzzywuzzy import fuzz

app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

BASE_DIR = Path(__file__).resolve().parent

file_to_store_upload_docs = 'images'
if os.path.isdir(os.path.join(BASE_DIR,file_to_store_upload_docs)) != True :
	os.mkdir(os.path.join(BASE_DIR,file_to_store_upload_docs))

UPLOAD_FOLDER= os.path.join(BASE_DIR,file_to_store_upload_docs)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg']
file_dict ={0:'aadhar',1:'passport',2:'pan',3:'dl'}


face_classifier = cv2.CascadeClassifier('haarcasacde_facefrontal_default.xml')
def face_extraction(img):
    faces = face_classifier.detectMultiScale(img,1.3,5)
        
    if faces is ():
        print("no face")
        return None
        
    for (x,y,w,h) in faces :
        x=x-10
        y=y-10
        cropped_face = img[y:y+h+50 , x:x+w+50]
            
    return cropped_face


@app.route("/")
def home_page():
	return render_template('home.html',context='')

@app.route('/success')
def success():
	return render_template('success.html',context = session.get('messages'))

@app.route('/fail')
def fail():
	return render_template('fail.html',context = session.get('messages'))

@app.route('/kyc_video',methods=['POST','GET'])
def check_video_face():
	obj = make_model()
	if request.method == "POST":
		if not os.path.exists('sface_recong.h5'):

			face_capture.perform()
			val,session['messages'] = obj.train_model()
		else:
			val,session['messages'] = obj.start()
		if val :
			
			return redirect(url_for('success'))
		else :

			return redirect(url_for('fail'))
	else:
		return render_template('video_kyc.html',context =session.get('messages'))

def check_fileextension(file):
	if  file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg'):
		return True
	else:
		return False

@app.route("/kyc",methods=['POST','GET'])
def check_kyc():
	if request.method == "POST":
		new_file = open("new_file.txt",'wt')
		f_aadhar = request.files["aadhar"]
		f_passport = request.files["passport"]
		f_pan = request.files["pan"]
		f_dl = request.files["dl"]
		files = [f_aadhar,f_passport,f_pan,f_dl]
		no_of_files = 0
		file_names = []
		for no,f in enumerate(files):
			
			if f.filename == '' and no == 0 :

				return render_template('kyc_docs.html',context='Please upload Your Aadhar Card file ')
		
			elif check_fileextension(f.filename):
				no_of_files = 1
				f.filename = file_dict[no]+'.jpg'
				file_names.append(f.filename)
				f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
				if no == 0:
					img = cv2.imread('images/aadhar.jpg')
					img = face_extraction(img)
					aadhar_data = get_aadhar_text.get_data(os.path.join(BASE_DIR,'images',file_names[0]))
					session['aadhar_phoneno'] = aadhar_data['Phone']
					try:
						cv2.imwrite('images/aadhar_face_extract.jpg',img)
					except:
						return render_template('kyc_docs.html',context='Upload proper documents')

					print(aadhar_data)
					new_file.write(str(aadhar_data))
				elif no == 1 and f.filename != '':
					img = cv2.imread('images/passport.jpg')
					img = face_extraction(img)
					try:
						cv2.imwrite('images/face_extract.jpg',img)
					except:
						return render_template('kyc_docs.html',context='Upload proper documents')
				elif no == 2 and f.filename != '':
					img = cv2.imread('images/pan.jpg')
					img = face_extraction(img)
					pan_data = get_pan_data.get_data(os.path.join(BASE_DIR,'images',file_names[2]))
					try:
						cv2.imwrite('images/pan_face_extract.jpg',img)
					except:
						return render_template('kyc_docs.html',context='Upload proper documents')

					print(pan_data)
					new_file.write(str(pan_data))
				elif no == 3 and f.filename != '':
					img = cv2.imread('images/dl.jpg')
					img = face_extraction(img)
					dl_data = get_license_data.get_data(os.path.join(BASE_DIR,'images',file_names[3]))
					try:
						cv2.imwrite('images/dl_face_extract.jpg',img)
					except:
						return render_template('kyc_docs.html',context='Upload proper documents')
					print(dl_data)
					new_file.write(str(dl_data))
		
			elif no_of_files == 0:
			
				return render_template('kyc_docs.html',context='Enter jpg or pdf')
		new_file.close()
		if no_of_files > 0:
	
			print(aadhar_data)
			try:
				qr_data = get_qr_details.get_data(os.path.join(BASE_DIR,'images','aadhar.jpg'))
				print('QR data:  ',qr_data)
				status=validate_aadhar(aadhar_data,qr_data)
				if status['status']=="VERIFIED":
					return redirect(url_for('otp_thing'))
				else:
					return render_template('kyc_docs.html',context = status)
			except:
				return redirect(url_for('otp_thing'))
	else:
		return render_template('kyc_docs.html',context = '')

	
@app.route('/otpgenerate',methods = ['POST','GET'])
def otp_thing():
	phoneno = session.get('aadhar_phoneno')
	try:
		correct_otp = send_otp.generate(session.get('aadhar_phoneno'))
	except:
		return render_template('home.html',context='Cant generate otp because of some problem')
	count = 3
	if request.method == 'POST':
		otp_entered = request.form['otp']
		if otp_entered != correct_otp and count > 3:
			count -=1
			return render_template('kyc_otp.html',context='Incorrect OTP.{} more tries remaining'.format(count))
		if count >=0 :
			session['messages'] = 'OTP verfication complete!!'
			return 	redirect(url_for('check_video_face'))
		else:
			return render_template('home.html',context='OTP Not matching.Please start again')
	else:

		return render_template('kyc_otp.html',context='',no=phoneno)

def validate_aadhar(aadhar_details,qr_details):
    if fuzz.partial_ratio(aadhar_details['Aadhar No'],qr_details['Aadhar No'])<80:
        print("INVALID AADHAR NO")
        status="INVALID AADHAR NO"
    elif fuzz.partial_ratio(aadhar_details['DOB'],qr_details['DOB'])<80:
        print("INVALID DOB")
        status="INVALID DOB"
    elif fuzz.partial_ratio(aadhar_details['Gender'],qr_details['Gender'])<80:
        print("INVALID GENDER")
        status="INVALID GENDER"
    else:
        print("VERIFIED")
        status="VERIFIED"
    context={'status':status}
    return context

@app.route("/aboutus")
def aboutus():
	return render_template('aboutus_demo.html')

if __name__ == '__main__':
	app.run(debug=True)