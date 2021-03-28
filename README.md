# RPM
This code is for Video-KYC web application Problem Statement where we have to verify the government documents uploaded by the user are fraud or not. 


We first get all the required documents(aadhar card mandatory). Then scan aadhar QR code and verify it with the data extracted from aadhar image using pytesseract. If matching, we send an OTP to the registered phone no on the aadhar card,

After OTP verfication, we capture live images of the user , create a model based on these images and then use the model to predict whether or not the aadhar,pan and dl images match te live feed. If yes , then KYC is complete

**STEPS**
1)Home page. Click start to go ahead
![image](https://user-images.githubusercontent.com/66548981/112753999-bfa6b600-8ff7-11eb-8a15-48fe7c71be79.png)

2)Upload Documents. Here we take the documents from user in jpg format. The documents should be clear.
![image](https://user-images.githubusercontent.com/66548981/112754031-e5cc5600-8ff7-11eb-8ecf-3819c1a13f57.png)
 
3)OTP Verfication. Otp send on the number
![image](https://user-images.githubusercontent.com/66548981/112754116-54111880-8ff8-11eb-8f17-d5af647a2bd5.png)

4)Video KYC. On pressing start, the program will click images of the user and a create a CNN model.
![image](https://user-images.githubusercontent.com/66548981/112754139-6db26000-8ff8-11eb-8bee-8699fefb306f.png)

Clicking images 
![image](https://user-images.githubusercontent.com/66548981/112754180-92a6d300-8ff8-11eb-83e2-3320dfbe3852.png)

Making model
![image](https://user-images.githubusercontent.com/66548981/112754237-ca157f80-8ff8-11eb-841d-471ccc264fe3.png)

After test image
![image](https://user-images.githubusercontent.com/66548981/112754339-38f2d880-8ff9-11eb-94ed-85538a634bf3.png)
