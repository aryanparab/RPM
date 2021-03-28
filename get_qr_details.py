import os,cv2,pytesseract,re
import numpy as np
from PIL import Image
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from pyzbar.pyzbar import decode

def get_data(img_file):
    def getQRAno(text):
        x=re.findall('[0-9]{12}',text)
        if len(x)>0:
            try :
                return re.findall('[0-9]{12}',text)[0]
            except:
                return ''
        return ''

    def getQRDOB(text):
        x=re.findall('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',text)
        if len(x)>0:
            return x[len(x)-1]
        return ''

    def getQRName(text):
        x=re.findall('[0-9]{2}\/[0-9]{2}\/[0-9]{4}',text)
        if len(x)>0:
            return x[len(x)-1]
        return ''

    def getQRGender(text):
        if text=='':
            return ''
        index=text.find('gender="')+len('gender="')
        if text[index]=='M':
            return 'Male'
        elif text[index]=='F':
            return 'Female'
        else:
            return ''
    imgfile=img_file
    qrtext=decode(Image.open(imgfile))
    if len(qrtext)==0:
        qrtext=''
    else:
        qrtext=qrtext[0].data.decode('utf-8')
    qr_details={'Aadhar No':getQRAno(qrtext),'DOB':getQRDOB(qrtext),'Gender':getQRGender(qrtext)}
    return qr_details
