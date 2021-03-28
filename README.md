# RPM
This code is for Video-KYC web application Problem Statement where we have to verify the government documents uploaded by the user are fraud or not. 

We first get all the required documents(aadhar card mandatory). Then scan aadhar QR code and verify it with the data extracted from aadhar image using pytesseract. If matching, we send an OTP to the registered phone no on the aadhar card,

After OTP verfication, we capture live images of the user , create a model based on these images and then use the model to predict whether or not the aadhar,pan and dl images match te live feed. If yes , then KYC is complete
