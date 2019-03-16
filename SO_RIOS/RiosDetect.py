from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
import numpy as np
import cv2
import zmq
import time,datetime
import sys
from RiosSendData import *
import json



class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class RiosDetect:

 

  def sendData(self):
     
      context = zmq.Context()
    # print "Connecting to server..."
      socket = context.socket(zmq.REQ)
      socket.connect ("tcp://104.154.71.6:3000" )
      load = open("/home/pi/Desktop/sistema_optico/SO_RIOS/imgrios.jpg","r")
      img_read = load.read()
      socket.send(img_read)
      message = socket.recv()

       
      today = '%s' % datetime.datetime.now()
      print today

      data_vars = Object()       

      data_vars.code_device = 1
      data_vars.fecha = today
      data_vars.urlImage = message
  
      data_vars.values = Object() 
      data_vars.values.NV = 9.5
      data_vars.values.FL = 25.5
      data_vars.values.HM = 14.44
      data_vars.values.TM = 24.0
      data_vars.values.PT = 45.7
      data_vars.values.AT = 2022
      data_vars.values.PH = 5.1
      data_vars.values.OR = 458
      data_vars.values.LAT = 95.44
      data_vars.values.LONG = -32.75
      
      vars = data_vars.toJSON()
      print vars

      socket.send(vars)
      message=socket.recv()
      print message

      return message
            #self.showImg()
     

  def det_body(self):
     
    
    camera = PiCamera()
    camera.resolution= (640,416)
    rawCapture = PiRGBArray(camera)

    upperbody = cv2.CascadeClassifier('haarcascade_upperbody.xml')
    lowerbody = cv2.CascadeClassifier('haarcascade_lowerbody.xml')
    fullbody = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    face_detect = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    #eye_detect = cv2.CascadeClassifier('haarcascade_eye.xml')
      
    for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port= True):
        imaT = frame.array
        image = cv2.resize(imaT,None,None,0.9,0.9,cv2.INTER_LINEAR)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
        upper = upperbody.detectMultiScale(gray,1.3,5)
        face = face_detect.detectMultiScale(gray,1.2,3)
        body = fullbody.detectMultiScale(gray,1.1,3)
        lower = lowerbody.detectMultiScale(gray,1.1,3)
        cara = 0

           
        for (x,y,w,h) in body:
             cv2.rectangle(image,(x,y),(x+w,y+h),(0,200,0),1)
             #cv2.putText(image, "Se detecto algo", (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255))
             #cv2.imwrite('/home/pi/Desktop/sistema_optico/SO_RIOS/Imagenes/imgrios.jpg',imaT)
             #self.sendData()


        for (x,y,w,h) in lower:
              cv2.rectangle(image,(x,y),(x+w,y+h),(50,50,255),1)
           
        for (x,y,w,h) in face:
             cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
             cv2.putText(image, "Se detecto algo", (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255))                                
              
             cv2.imwrite('/home/pi/Desktop/sistema_optico/SO_RIOS/imgrios.jpg',imaT)
             date=time.strftime('%d %b %Y,%H:%M:%S')
             print(date)
             self.sendData()
             
        for (x,y,w,h) in upper:
              cv2.rectangle(image,(x,y),(x+w,y+h),(200,0,100),1)
            #roi_color = image[y:y+h,x:x+w]
              cv2.putText(image, "Se detecto algo", (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255))
              cv2.imwrite('/home/pi/Desktop/sistema_optico/SO_RIOS/imgrios.jpg',imaT)
              #date=time.strftime('%d %b %Y,%H:%M:%S')
             # print(date)
              self.sendData()
              
              for (x,y,w,h) in face:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
                cv2.putText(image, "Se detecto algo", (10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255))                                
                cv2.imwrite('/home/pi/Desktop/sistema_optico/SO_RIOS/imgrios.jpg',imaT)
                #date=time.strftime('%d %b %Y,%H:%M:%S')
               # print(date)
                self.sendData()

             #socket.send(img_read)
             #recv = socket.recv()
            #self.showImg()


            
        #cv2.imshow("captura", image)
        cv2.imshow("Frame", imaT)
       # cv2.imshow("gris", gray)

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        #socket.close()
 
        if key == ord("q"):
           break

    cv2.destroyAllWindows()
    camera.close()
