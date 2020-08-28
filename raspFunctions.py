import os
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

class RaspFunctions:

    record = {'Rahil':0,'Ankush':0,'Unknown':0}

    dirpath = os.path.dirname(__file__)
    modelFile = f"{dirpath}/model/res10_300x300_ssd_iter_140000.caffemodel"
    configFile = f"{dirpath}/model/deploy.prototxt.txt"
    model = cv2.dnn.readNetFromCaffe(configFile, modelFile)

    rec = cv2.face.LBPHFaceRecognizer_create()
    rec.read(f"{dirpath}/recognizer/trainingdata.yml")
    print('Neural Network loaded..')

    ena,in1,in2 = 2,3,4 
    pir = 11

    def setGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        #DC motor
        GPIO.setup(ena,GPIO.OUT)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        #PIR
        GPIO.setup(pir, GPIO.IN)  

    def readPIR(self):
        self.detectedCount = 0
        while True:
            if GPIO.input(pir):
                self.detectedCount += 1
                
            if detectedCount > 10000:
                return True

    def readCamera(self):
        self.cap = cv2.VideoCapture(0)
        self.counts = {'Rahil':0, 'Ankush':0, 'Unknown':0}
        self.maxcount = 0
        self.person = None
        print('Detecting Face')

        while True:
            _, self.frame = self.cap.read()
            try:
                self.res, self.text, self.pts = self.detectface(self.frame)
            except:
                print('No face detected')
                continue

            self.counts[self.res] += 1
            self.personName = max(self.counts,key=self.counts.get)
            self.maxcount = self.counts[self.personName]

            if self.maxcount > 30:
                break
            
            cv2.waitKey(1)
            cv2.imwrite("detected.jpg", self.frame)
        self.cap.release()
        self.Authenticate(self.personName)

    def Authenticate(self,personName):
        if self.personName in ['Rahil','Ankush']:
            print(f'Welcome {self.personName}!!')
            self.openDoor()
            RaspFunctions.record[self.personName] += 1
        else:
            print('Access Denied')
            RaspFunctions.record['Unknown'] += 1
            self.sendNotification(personName)

    def openDoor(self):
        pwm = GPIO.PWM(ena,100)
        pwm.start(0)
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        pwm.ChangeDutyCycle(25)
        sleep(2)
        GPIO.output(in1,GPIO.LOW)
        sleep(10)
        self.closeDoor()

    def closeDoor(self):
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        pwm.ChangeDutyCycle(25)
        sleep(2)
        GPIO.output(in2,GPIO.LOW)
        print('Door closed.')

    def sendNotification(self,personName):
        sender = 'codingbug.py@gmail.com'
        receiver = 'photogenicbug@gmail.com'
        password = '*********'

        message = f"Unknown Person Detected at {datetime.datetime.now()}"
        server = smtplib.SMTP_SSL(host='smtp.gmail.com',port=465)
        server.login(sender,password)

        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Message from Door Unlocking System'
        msg.attach(MIMEImage(open(r'detected.jpg','rb').read(),name='detectedface'))
        msg.attach(MIMEText(message,'plain'))

        server.send_message(msg)
        print('Email sent')
        server.quit()

    def detectface(self,img):
        self.img = img
        (h,w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img,(300,300)),scalefactor=1.0,size=(300,300),
                                    mean=(104.0,177.0,123.0))
        self.model.setInput(blob)
        detections = self.model.forward()
        for i in range(detections.shape[2]):
            confidence = detections[0,0,i,2]
            if confidence > 0.5:
                box = detections[0,0,i,3:7] * np.array([w,h,w,h])
                (startX, startY, endX, endY) = box.astype("int")
                pts = (startX, startY, endX, endY)
                face = img[startY:endY,startX:endX]
                gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                res, text = self.recognizeface(gray)
        return res, text, pts

    def recognizeface(self,face):
        self.face = face
        self.id = 0
        self.id, self.diff = self.rec.predict(self.face)
        # print(self.diff, self.id)
        if self.diff < 55:
                if self.id == 1:
                    self.id = 'Rahil'
                elif self.id == 2:
                    self.id = 'Ankush'
        else:
            self.id = 'Unknown'
        text = '{} {:.2f}'.format(self.id,self.diff)
        return self.id, text