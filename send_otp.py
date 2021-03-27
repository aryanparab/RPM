import requests
from random import randint

def generate(no):
	url = "https://www.fast2sms.com/dev/bulk"
	otp = randint(100000,999999)
	payload = "sender_id=FSTSMS&message="+str(otp)+"&language=english&route=p&numbers="+no
	

	headers = {
	'authorization': "ODzgwbE7eBcMSyfVC5oPdApX6ZaWUsYKLqnh0xTjmQJ9HNl23vDtwJRkj5sam698SpEcOCoHKITxhNMn", #AUTH KEY FROM FAST2SMS
	'Content-Type': "application/x-www-form-urlencoded",
	'Cache-Control': "no-cache",
	}

	response = requests.request("POST", url, data=payload, headers=headers)
	print(response.text)
	return(otp)