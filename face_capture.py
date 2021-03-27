# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
import numpy as np
from pathlib import Path
import os 

def perform():
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
            
        return cropped_face

    cap = cv2.VideoCapture(0)
    count =0 

    while (cap.isOpened()):
        success , img = cap.read()
        if face_extraction(img) is not None :
            count = count+1
            face = cv2.resize(face_extraction(img),(224,224))
            
            file_name= str(count)+'.jpg'
            if count <150 :
                file_name_path = os.path.join(BASE_DIR,'faces','train','person',file_name)
            #'C:/Users/parab/Desktop/python/opencv/images/face_recog_train/aryan/'
            else:
                file_name_path = os.path.join(BASE_DIR,'faces','test','person',file_name)
            cv2.imwrite(file_name_path,face)
            
            cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_SCRIPT_COMPLEX,1,(0,255,0),2)
            cv2.imshow('Face Cropper',face)
            
        else:
            print("Face not Found")
            pass
        
        
        if cv2.waitKey(1) == 1000 or count == 200:
            break

    cap.release()
    cv2.destroyAllWindows()


