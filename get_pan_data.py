import os,cv2,pytesseract,re
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

	def getPAN(text):
	    return re.findall('[A-Z]{5}[0-9]{4}[A-Z]{1}',text)[0]

	def getDOB(text):
	    return re.findall('[0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9]',text)[0]

	imgfile=img_file
	text=get_text(imgfile)
	pan_details={'PAN Number':getPAN(text),
		'DOB':getDOB(text)}

	return pan_details