import os,cv2,pytesseract,re
import numpy as np
from PIL import Image
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_data(img_file):
	def get_text(imgfile):
	    grayimg = cv2.imread(imgfile)
	    grayimg=cv2.cvtColor(grayimg, cv2.COLOR_BGR2GRAY)
	    kernel = np.ones((1, 1), np.uint8)
	    img = cv2.dilate(grayimg, kernel, iterations=1)
	    img = cv2.erode(img, kernel, iterations=1)
	    th , img = cv2.threshold(img,127,225,cv2.THRESH_TRUNC)
	    tempfile = "{}.png".format(os.getpid())
	    cv2.imwrite(tempfile, img)
	    text = pytesseract.image_to_string(Image.open(tempfile))
	    text = re.sub(r'^[a-zA-z1-9]','',text)
	    os.remove(tempfile)
	    return text

	def getEno(text):
	    start=end=text.find('Enrollment No.: ')+len('Enrollment No.: ')
	    while (text[end]!='\n'):
	        end+=1
	    return text[start:end]   

	def getPhone(text):
		try:
		    if text.find('Mobile No: ')!=-1:
		        start=text.find('Mobile No: ')+ len('Mobile No: ')
		        return text[start:start+10]
		    else:
		        return re.findall(r'(?<!\d)\d{10}(?!\d)',text)[0]
		except:
			return ''

	def getAno(text):
	    start=end=text.find('Your Aadhaar No. :\n\n')+len('Your Aadhaar No. :\n\n')
	    while (text[end]!='\n'):
	        end+=1
	    return text[start:end]

	def getDOB(text):
	    start=end=text.find('DOB : ')+len('DOB : ')
	    while (text[end]!='\n'):
	        end+=1
	    return text[start:end]

	def getGender(text):
	    if text.find('Male\n\n')!=-1:
	        return 'Male'
	    else:
	        return 'Female'

	imgfile=img_file
	text=get_text(imgfile)
	aadhar_details={'Enrollment No':getEno(text),
					'Phone':getPhone(text),
					'Aadhar No':getAno(text),
					'DOB':getDOB(text),
					'Gender':getGender(text)}

	return aadhar_details