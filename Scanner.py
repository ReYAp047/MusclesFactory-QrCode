from asyncio.windows_events import NULL
from email.utils import formatdate
import cv2
from cv2 import log
import numpy as np
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import time
import paho.mqtt.client as paho
from paho import mqtt

from playsound import playsound

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


font = cv2.FONT_HERSHEY_PLAIN

cap = cv2.VideoCapture(0)


noww = datetime.now()
currentYearString = int(noww.strftime("%Y"))
currentMonthString = int(noww.strftime("%m"))
currentDayString = int(noww.strftime("%d"))



#calification du temps systèeme par période
now = datetime.now()
currentTimeString = now.strftime("%H")
currentTime = int(currentTimeString)
if 6 <= currentTime <= 8:
    periode="one"
elif 8 <= currentTime <= 10:
    periode="Tow"
elif 10 <= currentTime <= 12:
    periode="Three"
elif 12 <= currentTime <= 14:
    periode="Four"
elif 14 <= currentTime <= 16:
    periode="Five"
elif 16 <= currentTime <= 18:
    periode="Six"
elif 18 <= currentTime <= 20:
    periode="Seven"
elif 20 <= currentTime <= 22:
    periode="Eight"
else:
    periode="Nine"

qrdate=""


while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        try:
            data = str(obj.data, 'UTF-8')
            print(data)
            if(len(data)==32):
                docs = db.collection(u'Reservation').where(u'ClientID', u'==', data).where(periode, u'==', True).where(u'Year', u'==', currentYearString).where(u'Month', u'==', currentMonthString).where(u'Date', u'==', currentDayString).stream()
                if(True) : 
                    for doc in docs:
                       
                        reservation = doc.to_dict()
                        print(reservation['One'])
  
                    
                        if(True) :
                            #----------------- Code de connection & envoie-----------------------
                            def on_connect(client, userdata, flags, rc, properties=None):
                                print("CONNACK received with code %s." % rc)
                                
                                # with this callback you can see if your publish was successful
                            def on_publish(client, userdata, mid, properties=None):
                                    print("mid: " + str(mid))
                                
                                # print which topic was subscribed to
                            def on_subscribe(client, userdata, mid, granted_qos, properties=None):
                                    print("Subscribed: " + str(mid) + " " + str(granted_qos))
                                
                                # print message, useful for checking if it was successful
                            def on_message(client, userdata, msg):
                                print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
                                
                                # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
                                # userdata is user defined data of any type, updated by user_data_set()
                                # client_id is the given name of the client
                            client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
                            client.on_connect = on_connect
                                
                                # enable TLS for secure connection
                            client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
                                # set username and password
                            client.username_pw_set("pcFace", "Dali19974")
                                # connect to HiveMQ Cloud on port 8883 (default for MQTT)
                            client.connect("d62d6f41f62b4c0698d334a94fc4c32b.s1.eu.hivemq.cloud", 8883)
                                
                                # setting callbacks, use separate functions like above for better visibility
                            client.on_subscribe = on_subscribe
                            client.on_message = on_message
                            client.on_publish = on_publish
                                
                                # subscribe to all topics of encyclopedia by using the wildcard "#"
                            client.subscribe("open/#", qos=1)
                            valid = " Valid entry for the Client: "+str(data)
                            client.publish("open/door", payload=valid, qos=1)
                            #----------------------------------------

                            playsound('./wlc.mp3') 
                        else:
                            playsound("./timeCheck.mp3")
                else:
                    playsound('./noReservationFound.mp3') 
            else:
                playsound('./notClientQr.mp3')
        except ValueError:
            playsound('./notClientQr.mp3') 
            
            

    cv2.imshow("Freame", frame)

    key = cv2.waitKey(1)

    if key == 0:
        break