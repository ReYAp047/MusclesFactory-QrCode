from email.utils import formatdate
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import time
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

                    client.publish("open/door", payload=1, qos=1)
                    #----------------------------------------

                    playsound('welcomme.mp3') 
            else:
                playsound('Expire.mp3') 
        except ValueError:
            playsound('Check.mp3') 
            
            

    cv2.imshow("Freame", frame)

    key = cv2.waitKey(1)

    if key == 0:
        break