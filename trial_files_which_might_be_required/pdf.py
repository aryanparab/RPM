#Make the necessary imports

import numpy as np

import re
import cv2
import os
import textract
from PIL import Image 
import pytesseract 
import sys 
from pdf2image import convert_from_path 
from pathlib import Path
# from nltk.corpus import stopwords
# import nltk
# nltk.download()
# nltk.download('stopwords')

pdf = [] 
final = [] 
corpus1=[]
jjj2=[] 
jjjj2=[]
#Taking inputs and calling the above created functuon to output the prediciton.

pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_DIR = Path(__file__).resolve().parent
def fileget(text1):
    

    path=text1
    for f in os.listdir(path):
        if f.endswith('.pdf') or f.endswith('.xlsx') or f.endswith('.docx') or f.endswith('.pptx') or f.endswith('.png') or f.endswith('.jpg') :

            pdf.append(f)
            path1 = os.path.join(BASE_DIR,f)
            if f.endswith('.png') or f.endswith('.jpg'):
                img=cv2.imread(path1)
                text=pytesseract.image_to_string(img)
            else:
                text = textract.process(path1)
                text = b''.join([text])
                inter = text.decode("utf-8")
            if "\x0c\x0c\x0c\x0c\x0c" in inter:
                pages=convert_from_bytes(path1,poppler_path=r'poppler-0.68.0\bin')
                image_counter=1
                text = ""

                docs = []
                for page in pages:
                    filename= "page_"+str(image_counter)+".jpg"
                    page.save(path+filename,'JPEG')
                    image_counter=image_counter+1
                
                    filename=path+"page_"+str(image_counter)+".jpg"
                    text = text + str(((pytesseract.image_to_string(Image.open(filename)))))
                    docs.append(filename)
                for doc in docs:
                 os.remove(doc)
                #text=b''.join([text])
                inter=text
                
                
                
            final.append(inter)    
    

     
    for i in final:
        jjjj2.append(i.split('\n'))
     
    
    return jjjj2


def main():
 
    print(fileget(BASE_DIR))    
    

      #st.success("The Given output is {}".format(output))
    


      
    
      

if __name__=="__main__":
    main()
