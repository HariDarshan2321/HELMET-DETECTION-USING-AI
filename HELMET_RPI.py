import os
import sys
import time
import serial
import RPi.GPIO as GPIO
import Adafruit_DHT
import http.client
import urllib
from twilio.rest import Client
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#****************************************************

account_sid ="AC81d25aa600de5577bc705b04ad27e6c6" 	# Put your Twilio account SID here
auth_token ="68d2633de98f9c2dbaa2cf15984c6550" 	        # Put your auth token here
client = Client(account_sid, auth_token)

#****************************************************

TH_pin = 16
TH_name = Adafruit_DHT.DHT11

MQ2_PIN = 20
GPIO.setup(MQ2_PIN,GPIO.IN)

MQ135_PIN = 21
GPIO.setup(MQ135_PIN,GPIO.IN)

PRESSURE_PIN=26

gTEMP = 0
gMQ2 = 0
gMQ135 = 0
#********************************************
def RCtime (PRESSURE_PIN):
    reading = 0
    GPIO.setup(PRESSURE_PIN, GPIO.OUT)
    GPIO.output(PRESSURE_PIN, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(PRESSURE_PIN, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while (GPIO.input(PRESSURE_PIN) == GPIO.LOW):
        reading += 1
    return reading
#********************************************



while True:
    
    #****DHT11***********************************
    humidity , temperature = Adafruit_DHT.read_retry(TH_name,TH_pin)
    gTEMP=temperature
    print ("TEMP : ", temperature)
    print ("HUM : ", humidity)
    time.sleep(1)

    #****MQ2***********************************
    MQ2_val = GPIO.input(MQ2_PIN)
    if( MQ2_val == False ):
        gMQ2=1
        print("MQ2 is detected")
        time.sleep(1)
    else:
        gMQ2=0
        print("MQ2 is not detected")
        time.sleep(1)

    #****MQ135***********************************
    MQ135_val = GPIO.input(MQ135_PIN)
    if( MQ135_val == True ):
        gMQ135=1
        print("MQ135 is detected")
        time.sleep(1)
    else:
        gMQ135=0
        print("MQ135 is not detected")
        time.sleep(1)

    #****PRESSURE***********************************
    pressure_val=RCtime(PRESSURE_PIN)   # Read RC timing using pin #27
    print (pressure_val)
    if(pressure_val>1000000):
        print("pressure is more")
        time.sleep(1)
    else:
        print("pressure is normal")
        time.sleep(1)
    print(" ")


    

    import speech_recognition as sr  #library for performing speech recognition
    recording = sr.Recognizer()
    #recognizing speech from an audio source
    with sr.Microphone() as source:
        recording.adjust_for_ambient_noise(source)
        print("Please Say something:")
        audio = recording.listen(source)       #recognized speech from microphone
        try:
            #print("You said: \n" + recording.recognize_google(audio))  #speech received
            mailtext=recording.recognize_google(audio)
            print(mailtext)
            
            if(mailtext=="help"):

                print("voice command received")
                #this message alert for if voice detected "HELP"
                
                message = client.api.account.messages.create(
                            to="+918849943354", 	# Put your cellphone number here
                            from_="+12627358199", 	# Put your Twilio number here
                            body="Need Help")
                time.sleep(3)
                
                print("message sent")
            else:
                
                print("voice command not received")
                
        except Exception as e:
            print(e)


    params = urllib.parse.urlencode({'field1': gTEMP,'field2': gMQ2,'field3': gMQ135,'key':'EXUY7G01VYMO76JK'})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = http.client.HTTPConnection("api.thingspeak.com:80")
    try:
      conn.request("POST", "/update", params, headers)
      response = conn.getresponse()
      data = response.read()
      print (data)
      conn.close()
      time.sleep(2)
    except:
      print ("connection failed")
      print ("")
      time.sleep(1)

#******************************************************************


  
