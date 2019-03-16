# coding=utf-8
from Tkinter import *
import tkMessageBox
from RiosGeolocation import *
from RiosWebData import *
from RiosSendData import *
from RiosWeather import *
from RiosConfig import *
from RiosDetect import *
#download and install pillow:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
from PIL import Image, ImageTk

#from picamera import PiCamera
#from picamera.array import PiRGBArray#38
#from time import sleep

#import numpy as np
#import cv2


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    
    # config vars
    cloud_api = "";
    appname = "";
    deviceId = "";
    ip = "0.0.0.0";
    port = 3000;
    timer = 0;

    # device info
    description = ""
    address = ""
    lat = 0.0
    lng = 0.0

    
    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master
        
        self.init_config();
        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

        
        

    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget    
        self.master.title(self.appname)

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a menu instance
        mainmenu = Menu(self.master)
        self.master.config(menu=mainmenu)

        # create the file object)
        MR3 = Menu(mainmenu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        MR3.add_command(label="Get Context", command=self.getContext)
        MR3.add_command(label="Start SendData", command=self.sendData)

        MR3.add_command(label="Exit", command=self.client_exit)

        #added "file" to our menu
        mainmenu.add_cascade(label="File", menu=MR3)

        # create the file object)
        setup = Menu(mainmenu)

        # adds a command to the menu option, calling it exit, and the
        mainmenu.add_cascade(label="Setup", menu=setup)

        setup.add_command(label="Parameters", command=self.showImg)

        
        self.button = Button(root, text="Iniciar", command = self.detc_Mov)
        self.button.pack()

    def detc_Mov(self):
       #tkMessageBox.showinfo("Rios III", "Hello Rios III")
        #rios = RiosDetect()
        #global a
        #a = 1
        #if a == 1:
            rios = RiosDetect()
            rios.det_body()
            self
            #rios.sendData()
      
        #self.getGeolocation();
        #self.getWeather();        
 
    def init_config(self):
        MR3Config = RiosConfig();
        myData = MR3Config.getConfigData();
        #tkMessageBox.showinfo("FitoSmart - Config", myData)
        self.cloud_api = myData['cloud_api'];
        self.appname = myData['appname'];
        self.deviceId = myData['deviceid'];
        self.ip = myData['ip'];
        self.port = myData['port'];
        self.timer = myData['timer'];
        #print self.appname

   # def validate(self, new_text):
    #    if not new_text: # the field is being cleared
     #       self.entered_number = 0
      #      return True

    #    try:
     #       self.entered_number = int(new_text)
      #      return True
       # except ValueError:
        #    return False


    def showImg(self):
        load = Image.open("imgrios.jpg")
        render = ImageTk.PhotoImage(load)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=50)
        #img.grid(row=1, column=1)
        

    def sendData(self):
        self.showImg();
        RiosD = RiosSendData();
        myMsg = RiosD.sendData();
        #tkMessageBox.showinfo("FitoSmart - sendData", myMsg)

   
    def getDeviceData(self):
        myDeviceData = RiosWebData();
        
        myDevData = myDeviceData.getDeviceData(self.cloud_api, self.deviceId);
        data =  myDevData[0]

        self.description = data['descripcion']
        self.address =  data['calle'] + ", " + data['colonia'] + " " + data['ciudad'] +  " " + data['estado'] + " " + "mexico"
        #self.address =   data['estado'] + "+" + "mexico"

        lblDeviceName = Label(self, text=self.deviceId + " : " + self.description)
        lblDeviceName.pack()

        myGeolocation = RiosGeolocation();
        
        lat, lng = myGeolocation.getGeolocation(self.address);
        self.lat = lat
        self.lng = lng
        #tkMessageBox.showinfo("FitoSmart - Geolocation", myMsg)
        
         
        lblAddress = Label(self, text= "Ubicacion: lat: " + str(self.lat) + " lng: " + str(self.lng) + " - " + self.address)
        lblAddress.pack()



        #return myMsg

        #tkMessageBox.showinfo("FitoSmart - WebData", myMsg)

    def getContext(self):
        self.   getDeviceData();
        myWeather = RiosWeather();
        
        myMsg = myWeather.getWeather(self.lat, self.lng);
        #tkMessageBox.showinfo("FitoSmart - Weather", myMsg)
        lblContext = Label(self, text=myMsg)
        lblContext.pack()


    def client_exit(self):
        exit()

# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()


root.geometry("608x480")

#creation of an instance
app = Window(root)


#mainloop 
root.mainloop()  
