import os,cv2,pytesseract,re
import numpy as np
from PIL import Image
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_data(img_file):
	def get_text(imgfile):
	    img = cv2.imread(imgfile)
	    grayimg=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	    tempfile = "{}.png".format(os.getpid())
	    cv2.imwrite(tempfile, grayimg)
	    text = pytesseract.image_to_string(Image.open(tempfile))
	    os.remove(tempfile)
	    return text

	def getEno(text):
	    x=re.findall('[0-9]{4}\/[0-9]{5}\/[0-9]{5}',text)
	    if len(x)>0:
	        return x[0]

	def getPhone(text):
	    x=re.findall(r'[0-9]{10}',text)
	    return x[len(x)-1]

	def getAno(text):
	    return re.findall('[0-9]{4}[ ][0-9]{4}[ ][0-9]{4}',text)[0]

	def getDOB(text):
	    x=re.findall('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',text)
	    return x[len(x)-1]

	def getGender(text):
	    if text.find('Male\n')==-1 and text.find('MALE\n')==-1 :
	        return 'Female'
	    else:
	        return 'Male'

	imgfile=img_file
	text=get_text(imgfile)
	aadhar_details={'Enrollment No':getEno(text),
					'Phone':getPhone(text),
					'Aadhar No':getAno(text),
					'DOB':getDOB(text),
					'Gender':getGender(text)}

	return aadhar_details