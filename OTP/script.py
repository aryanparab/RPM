from flask import *
import os
from twilio.rest import Client
import random

app = Flask(__name__)      
app.secret_key = 'otp'
@app.route('/')
def home():
  return render_template('login.html')
 
@app.route('/getOTP', methods = ['POST'])
def getOTP():
    number = request.form['number']
    val = getOTPApi(number)
    if val:
        return render_template('enterOTP.html')

@app.route('/validateOTP', methods = ['POST'])
def validateOTP():
    otp = request.form['otp']
    if 'response' in session:
        s = session['response']
        session.pop('response', None)
        if s == otp:
            return 'Thank you!'
        else:
            return 'Invalid OTP.'

def generateOTP():
    return random.randrange(100000,999999)

def getOTPApi(number):
    account_sid = 'ACe2c51fb68e84115334fa1f4027defb7c'
    auth_token = 'd0a85e04b3bac757396b9453f889203c'
    client = Client(account_sid, auth_token)
    otp=generateOTP()
    session['response'] = str(otp)
    body='Your OTP for KYC verification is: ' + str(otp)
    message = client.messages.create(
                            body=body,
                            from_='+18477529086',
                            to=number
                         )

    if message.sid:
        return True
    else:
        False

if __name__ == '__main__':
  app.run(debug=True)