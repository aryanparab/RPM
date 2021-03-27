import cv2
import numpy as np
from datetime import datetime

widthImg = 480
heightImg = 640

frameWidth = 640
frameHeight = 480



def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) #number of corner points

            if  area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area

    #cv2.drawContours(imgContour, biggest , -1,(255,0,0),20)
    return biggest

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations =2)
    imgThres = cv2.erode(imgDial,kernel,iterations =1)
    return imgThres

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2))
    myPointsNew = np.zeros((4,1,2),np.int32)

    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]

    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew

def getWarp(img,biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0],[widthImg , 0],[0,heightImg],[widthImg,heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput = cv2.warpPerspective(img,matrix,(widthImg,heightImg))

    imgCropped = imgOutput[20:imgOutput.shape[0]-20,20:imgOutput.shape[1]-20]
    imgCropped = cv2.resize(imgCropped,(widthImg,heightImg))

    return imgCropped

if __name__ == '__main__':
    img= cv2.imread('trial_files_which_might_be_required\\adhar.jpeg')
    cv2.resize(img,(widthImg,heightImg))
    imgContour = img.copy()

    imgThres = preProcessing(img)

    biggest = getContours(imgThres)
    imgWarped = imgContour
    if biggest.size != 0 :
        imgWarped = getWarp(img,biggest)
    else:
        pass

    cv2.imwrite("Document_scanner"+".jpg",imgWarped)

 