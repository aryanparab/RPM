import cv2
import numpy as np
from pathlib import Path
import os 

face_classifier = cv2.CascadeClassifier('haarcasacde_facefrontal_default.xml')
BASE_DIR = Path(__file__).resolve().parent
def face_extraction(img):
    faces = face_classifier.detectMultiScale(img,1.3,5)
        
    if faces is ():
        return None
        
    for (x,y,w,h) in faces :
        x=x-10
        y=y-10
        cropped_face = img[y:y+h+50 , x:x+w+50]
    
    cv2.imshow("Result", cropped_face)
    cv2.waitKey(500)
    return cropped_face

if __name__ == "__main__":
	img = cv2.imread('Document_scanner.jpg')
	cv2.imshow("Result", img)
  
	face = cv2.resize(face_extraction(img),(224,224))
	file_name = os.path.join(BASE_DIR,'aadhar_pic.jpg')
	cv2.imwrite(file_name,face)
