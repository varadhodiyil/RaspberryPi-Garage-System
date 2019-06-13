# RaspberryPi-Garage-System

## Welcome to the RaspberryPi Garage System. In this program we will build a garage system using a RaspberryPi and an image processing library known as OpenALPR (Automatic License Plate Recognition) to detect the number plate using image processing. You will have to register for the [openALPR cloud service](https://cloud.openalpr.com/). The registration is free and provides 2000 free detections every month.

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
Make the connections to the RaspberryPi as shown in the following schematic diagram: ![schematic diagram](https://github.com/MoizSM/RaspberryPi-Garage-System/blob/master/Connection%20Schematic.PNG) (or make your own connection and modify in the program as you please). 
The GPIO pins used for the components are as follows: 
* PIR Motion Sensor - GPIO14
* Servo Motor - GPIO4
* Ultrasonic Sensor : Trigger - GPIO8 , Echo - GPIO25

## [OpenALPR Documentation](http://doc.openalpr.com/)
## [OpenALPR Cloud API](http://doc.openalpr.com/cloud_api.html)

#### Please create a Garage OCR System folder on the Desktop of the RaspberryPi and place all the files in that folder. Run the **garage.py** to start the program. Please refer to the program to understand the syntax below.

The command below will take a photo and store it as a car.jpg file which is sent to the openALPR cloud service.
```python 
os.system('sudo fswebcam car.jpg') #If using webcam 
os.system('sudo raspistill -o car.jpg') #If using RaspberryPi Camera 
```
This command will run the openALPR cloud service and send the car.jpg file to detect the number plate and store the data into a **result.json** file which is located in **/Number Plate/result.json**. I have used the bash command. You can refer to the [Cloud API](http://doc.openalpr.com/cloud_api.html) and use the code sample you want. You will have to use your private key which you will get after you resgister. Refer to [this](https://cloud.openalpr.com/cloudapi/) page to get your **Secret Key** under the **Cloud API Credentials**. Put your secret key in the command below.
```python
os.system('sudo curl -X POST "https://api.openalpr.com/v2/recognize?secret_key=PUT YOUR SECRET KEY HERE&recognize_vehicle=1&country=ae&return_image=0&topn=10" -F image=@/home/pi/Desktop/Garage OCR System/car.jpg> ~/Desktop/Garage OCR System/Number Plate/result.json')
```
The initial distance is stored in a variable **total** which is 5 cm. The distance between the ultrasonic sensor and the object in from of it is continously being detected and stored in the variable **total**. While the distance measured is greater than 3.5 cm the servo motor will not rotate i.e the door will not shut. You can modify these values as per your requirements in the syntax below
```python
	total = 5 #Assigning starting distance for ultrasonic sensor
		while total > 3.5:
```
The rest of the commands are almost self explanatory and the description is commented beside the command in the program. 
