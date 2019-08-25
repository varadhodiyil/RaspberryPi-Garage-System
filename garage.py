#This program uses openALPR to detect number plates. The program is written to operate on the Raspberry Pi. Please refer to the README.md file for more details.

import RPi.GPIO as GPIO
import json
import time
import random
import urllib
import os
import datetime

#Setting up ports
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)	

#Assigning Ports for all the components
PIR = 14 #PIR Motion Sensor
MOT = 4 #Servo Motor
LED = 23 #Led Light 
TRIG = 8 #Ultrasonic Sensor Trigger
ECHO = 25 #Ultrasonic Sensor Echo

#Taking systen time and date for log record
currentDT = datetime.datetime.now()

#Setting up LED light
GPIO.setup(LED, GPIO.OUT)	

#Setting up motor
GPIO.setup(MOT, GPIO.OUT)
p = GPIO.PWM(MOT, 50)

#Motion sensor is taking input 0 or 1 based on weather motion was detected or not
GPIO.setup(PIR, GPIO.IN)

#Setting up ultrasonic sensor 
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG,0)
GPIO.setup(ECHO, GPIO.IN)
time.sleep(0.1)

def ret_num_plate():
	os.system('sudo fswebcam car.jpg')
	time.sleep(1)
	#Bash command to use the openALPR cloud service for number plate recognition.
	os.system('sudo curl -X POST "https://api.openalpr.com/v2/recognize?secret_key=PUT YOUR SECRET KEY HERE&recognize_vehicle=1&country=ae&return_image=0&topn=10" -F image=@/home/pi/Desktop/Garage OCR System/car.jpg> ~/Desktop/Garage OCR System/Number Plate/result.json')
	time.sleep(1)
	f = open("/home/pi/Desktop/Garage OCR System/Number Plate/result.json" , 'r')
	val = f.read() #Read number plate details from result.json file
	f.close()
	time.sleep(1)
	x = json.loads(val)
	if not x["results"]: #If no number plate was detected
		detectMotion()
	else:
		for i in x["results"]:
		 res = i["plate"] #Storing the number plate value from the JSON file into res
	 
	print("The number plate found is " + res)

	#Store plate number in text file to keep log of all the number plates scanned
	f = open("/home/pi/Desktop/Garage OCR System/Number Plate/log.txt" , "a")
	f.write("\n" + str(currentDT) + " : " + res)
	f.close()
	time.sleep(1)
	print("Stored")

	#Confirmation if plate is allowed
	if(res == "O-74775"): #Number plates that are allowed 
		print("Entry Allowed")
		#Rotating the motor to open the garage door
		#------------------------------------------
		p.start(2.0) 
		p.ChangeDutyCycle(0.5)
		time.sleep(0.5) 
		#-------------------------------------------
				
		total = 5 #Assigning starting distance for ultrasonic sensor
		while total > 3.5:
			
			time.sleep(0.5)

			#Using ultrasonic sensor to detect if car has eneter the garage upon which the door will automaticall close. 
			#-----------------------------------------------------
			GPIO.output(TRIG,1)
			time.sleep(0.00001)
			GPIO.output(TRIG,0)

			while GPIO.input(ECHO) == 0:
				pass
			start = time.time()

			while GPIO.input(ECHO) == 1:
				pass
			stop = time.time()
			
			total = (stop - start) * 17000
			print(total)
			
		print("The final distance is ", total)
		p.ChangeDutyCycle(7.5)
		time.sleep(0.5)		
		#-------------------------------------------------------------
				
	else:
		print("Not Allowed") #If number plate does not match
		
#Detecting motion and activating the Garage OCR System		
def detectMotion():
	while True:
		z = GPIO.input(PIR) #Assigning intial state of PIR to z
		if z == 0:
			print("No motion detected")
			time.sleep(0.5)
		elif z == 1:
			print("Motion Detected\n")
			ret_num_plate() #If motion is detected call the function which activates the number plate recognition functionality
			break
			
detectMotion() #Call the function to activate the PIR motion sensor to detect if car has arrived

p.stop()
GPIO.cleanup()