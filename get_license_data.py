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

	def getDLNODOI(text):
	    DLNO=re.findall('[A-Z]{2}[0-9]{2}[ ][0-9]{11}',text)[0]
	    DOI=re.findall('[0-9]{2}-[0-9]{2}-[0-9]{4}',text)[0]
	    return DLNO,DOI
	    

	def getName(text):
	    start=end=text.find('Name ')+ len('Name ')+1
	    while (text[end]!='\n'):
	        end+=1
	    return text[start:end]

	def getExpiry(text):
	    return re.findall('[0-9]{2}-[0-9]{2}-[0-9]{4}',text)[1]
	    
	def getDOB(text):
	    x=re.findall('[0-9]{2}-[0-9]{2}-[0-9]{4}',text)
	    return x[len(x)-1]

	def getAddress(text):
	    start=text.find('Add ')+len('Add ')+1
	    end=text.find('PIN')
	    add=''
	    while start!=end:
	        if text[start]=='\n':
	            start+=1
	            continue
	        add+=text[start]
	        start+=1
	    return add

	imgfile=img_file
	text=get_text(imgfile)
	dl,doi=getDLNODOI(text)
	license_details={'DL No':dl,
		'DOI':doi,
		'Address':getAddress(text),
		'DOB':getDOB(text),
		'Name':getName(text),
		'Expiry Date':getExpiry(text)}

	return license_details
