from email.utils import formatdate
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from datetime import datetime

import paho.mqtt.client as paho
from paho import mqtt

from playsound import playsound
font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)

currentDate = datetime.date(datetime.now())

while True:
    _, frame = cap.read()



    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        try:
            qrDateString = str(obj.data, 'UTF-8')
            
            qrDate = datetime.strptime(qrDateString, '%Y-%m-%d').date()
        
            if(currentDate > qrDate) :        
                playsound('welcomme.mp3') 
            else:
                playsound('Expire.mp3') 
        except ValueError:
            playsound('Check.mp3') 
            
            

    cv2.imshow("Freame", frame)

    key = cv2.waitKey(1)

    if key == 0:
        break