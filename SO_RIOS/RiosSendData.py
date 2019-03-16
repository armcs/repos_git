#from picamera import PiCamera,Color
from time import sleep
import zmq
import sys
from random import random
import base64
import time,datetime

class RiosSendData:

 def sendData(self):
  port = "3000"
  if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

  if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

  context = zmq.Context()
  print "Connecting to server..."
  socket = context.socket(zmq.REQ)
  socket.connect ("tcp://52.173.88.125:%s" % port)

  #camera=PiCamera()
  #inicial
  #x=time.strftime('%d %b %Y,%H:%M:%S')
  #print x

    #camera.start_preview()
  #  sleep(3)
    #camera.resolution=(512,512)
    #camera.annotate_text_size=10
    #camera.annotate_background=Color('white')
    #camera.annotate_foreground=Color('black')
    #camera.annotate_text=x
    #camera.capture("/home/adsoft/docker/gce-oreilly/ch8/zmq/client-server/imagen"+x+".png")
    #camera.stop_preview()

    #image=open("imagen"+x+".png","rb")
  image=open("imgrios.jpg","rb")

  image_read=image.read()
#    envis=base64.encodestring(image_read)
 #   temperature = random.uniform(20, 40)
#    tem = str(temperature)
   # print ("State temperature : %.3fC" %temperature)
  print("enviando imagen.jpg")

  pack = (image_read)

    #for dato in pack:
  socket.send(image_read)
  message=socket.recv()

  vars = "|"+message+"|T100|P80|A130|"
  print vars
  socket.send(vars)
  message=socket.recv()
  print message

  socket.close()
  return message
