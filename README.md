# RaspberryPi-Garage-System
This is a project to demonstrate the use of OCR (Optical Character Recognition) to identify number plates using image processing. 

## Welcome to the RaspberryPi Garage System. In this program we will build a garage system using a RaspberryPi and an image processing library known as OpenALPR (Automatic License Plate Recognition) to detect the number plate using image processing. 

### Things you will need: 
* RaspberryPi (This demonstration uses a RaspberryPi 3 Model B+)
* Resistors
* Jumper Cables
* Servo Motor
* Ultrasonic Sensor
* PIR Motion Sensor
* Raspberry Pi Camera or Web Cam
* A garage model (Which you can make out of a shoe box or something...)

### The project uses a PIR Motion Sensor to detect any motion (in this case when the car arrives at the garage door) and then runs a command to take a photo of the number plate. It then uses the openALPR cloud service to recognize and extract the number from the number plate and stores it into a result.json file. The number plate value is then retrieved from the result.json file and is then verified with the number plates that are allowed. If the number plate matches then the servo motor rotates (immitating the opening of the door). The ultrasonic sensor will then detect the distance of the car and will shut the door automatically when the threshold distance between the car and sensor is crossed. The program also keeps a log of all the number plates that were detected along with the time it was taken in the log.txt file.

### Programming Language : Python

## Let's Began!
Make the connections to the RaspberryPi as shown in the following schematic diagram (or make your own connection and modify in the program as you please). 
The GPIO pins used for the components are as follows: 
* PIR Motion Sensor - GPIO14
* Servo Motor - GPIO4
* Ultrasonic Sensor : Trigger - GPIO8 , Echo - GPIO25

#### Please create a Garage OCR System folder on the Desktop of the RaspberryPi and place all the files in that folder. Run the **garage.py** to start the program. Please refer to the program to understand the syntax below.

```python 
os.system('sudo fswebcam car.jpg') #If using webcam 
os.system('sudo raspistill -o car.jpg') #If using RaspberryPi Camera 
```



