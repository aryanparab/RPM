import os,cv2,pytesseract
from PIL import Image
import os
import regex as re
import imutils
import numpy as np
from pdf2image import convert_from_path
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_DIR = Path(__file__).resolve().parent

def get_text(imgfile):
    grayimg = cv2.imread(imgfile)
    grayimg = cv2.cvtColor(grayimg, cv2.COLOR_BGR2GRAY)
    tempfile = "{}.png".format(os.getpid())
    cv2.imwrite(tempfile, grayimg)
    text = pytesseract.image_to_string(Image.open(tempfile))
    text = re.sub(r'^[a-zA-z1-9]','',text)
    os.remove(tempfile)
    return text

texts = []
lst=[]
for i in os.listdir(BASE_DIR):
    try:
        if i.endswith('pdf'):
            lst.append(i)
            image = convert_from_path(os.path.join(BASE_DIR,i),poppler_path='C:\\Users\\Admin\\OneDrive\\Desktop\\poppler-0.68.0\\bin')
            cv2.imwrite('secret.jpg',image)
            texts.append(get_text('secret.jpg'))
        elif i.split(".")[1] in ['png','jpg','jpeg']:
            lst.append(i)
            texts.append(get_text(i))
    except:
        pass
print(lst)
print(texts)