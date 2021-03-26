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


# import tensorflow as tf
# from tensorflow import keras
# from keras.preprocessing import image
# from keras.preprocessing.image import ImageDataGenerator

# datagen = ImageDataGenerator(rotation_range=10, width_shift_range=0.1, 
#                              height_shift_range=0.1,shear_range=0.15, 
#                              zoom_range=0.3, horizontal_flip=True)

# path1 = os.path.join(BASE_DIR,'faces','train','person')
# save_here_1 = path1
# save_here_2 = os.path.join(BASE_DIR,'faces','test','person')
# #'C:/Users/parab/Desktop/python/opencv/images/face_recog_train/others/'

# import os


# for img in os.listdir(path1):
   
#     image_path = path1+img
#     image = cv2.imread(image_path)
#     img = face_extraction(image)
#     img1 = cv2.resize(img,(224,224))
#     img1 = np.array([img1])
#     datagen.fit(img1)
    
#     for x, val in zip(datagen.flow(img1,                    #image we chose
#         save_to_dir=save_here,     #this is where we figure out where to save
#          save_prefix='aug',        # it will save the images as 'aug_0912' some number for every new augmented image
#         save_format='jpg'),range(200)) :     # here we define a range because we want 10 augmented images otherwise it will keep looping forever I think
#         pass
#     for x, val in zip(datagen.flow(img1,                    #image we chose
#         save_to_dir=save_here,     #this is where we figure out where to save
#          save_prefix='aug',        # it will save the images as 'aug_0912' some number for every new augmented image
#         save_format='jpg'),range(200)) :     # here we define a range because we want 10 augmented images otherwise it will keep looping forever I think
#         pass
'''
path1 = 'C:/Users/parab/Desktop/python/opencv/images/Others/'
save_here ='C:/Users/parab/Desktop/python/opencv/images/mask_nomask_test/test_mask/'
cap = cv2.VideoCapture(0)
i=75
while (cap.isOpened()):
    success , img = cap.read()
    img1 = cv2.resize(img,(400,400))
    cv2.imwrite(save_here+str(i)+".jpg",img1)
    i = i+1
    if i ==100:
        break
cap.release()
cv2.destroyAllWindows()'''
