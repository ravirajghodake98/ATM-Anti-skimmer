from tkinter import*
from PIL import Image, ImageTk
import time
import cv2
import os
import csv
from twilio.rest import Client
import numpy as np
import serial
from random import randint

sr = serial.Serial('COM14', 9600)

os.system("sudo modprobe bcm2835-v4l2")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX



# names related to ids
names = ['None', 'A', 'B', 'I', 'Z', 'W'] 


#twilio service account
account_sid = "ACbda5dda45b72b0b00d388d74dbf71c1c"
auth_token = "675814775fef507fc133cdd83989e748"

root = Tk()

frame1 = Frame(root)
frame2 = Frame(root)

frame1.pack(side = TOP)
frame2.pack(side = TOP)

im =Image.open('sample.jpg')
im = ImageTk.PhotoImage(im)
rad = 0

def faceRecognition(rid):
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height

    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    name = "unknown"
    #iniciate id counter
    id = 0
    global rad
    while True:
        ret, img =cam.read()
##        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                name = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, name, (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  

        if(name != "unknown"):
            cv2.imwrite('image.jpg',img)
            image = Image.open("image.jpg")
            photo1 = ImageTk.PhotoImage(image)
            photo.config(im=photo1)
            photo.image = photo1
            if (int(rid) == id):
                status.config(text = 'Welcome '+name)
                rad = randint(1111,9999)
                print("OTP ",rad)
            ##    client = Client(account_sid, auth_token)
            ##    client.messages.create(
            ##        to = '+91',
            ##        from_ = "+12566078246",
            ##        body = rad)
                ok['state'] = 'normal'
                status.config(text = 'Enter your OTP')
                os.system('start 3.mp3')
    
                break
            else:
                status.config(text = 'Face and ID is missmatch.')
                break
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    cam.release()
    cv2.destroyAllWindows()

def start():
    
    sr.write('s'.encode())
    print('Start')
    status.config(text = 'Please scan your RFID card.')
    os.system('start 1.mp3')
    data = sr.readline().decode()
    print(data)
##    print('1')
    while(data[0] != 'f'):
        data = sr.readline().decode()
        print(data)
    rid = data[1]
    faceRecognition(rid)
    

def OK():
    global rad
    Otp = otp.get()
    if(int(Otp) == rad):
        status.config(text = 'Please collect your cash.')
        os.system('start 4.mp3')
        image = Image.open("sample.jpg")
        photo1 = ImageTk.PhotoImage(image)
        photo.config(im=photo1)
        photo.image = photo1
        otp.delete(0, 'end')
        ok['state'] = 'disabled'
        sr.write('y'.encode())
    else:
        status.config(text = 'OTP not match.')
        otp.delete(0, 'end')
        sr.write('n'.encode())
    
#---------------------------------------------------------------------------------------

title = Label(frame1, text = 'ATM Anti-Skinner with Face recognition :',font= "Helvetica 16 bold italic", width=50,height=3)
title.grid(row = 0, column = 0)

photo = Label(frame1, image=im ,font= 30, width=400,height=450)
photo.grid(row = 1, column = 0)

status = Label(frame1, text = ' ',font= 30, width=20,height=3)
status.grid(row = 1, column = 1)

otp = Entry(frame2,font=('courier',15),width=20)
otp.grid(row = 2, column = 0)

ok = Button(frame2, text = 'OK',font= 30, width=10,height=1,state= 'disabled' ,command = OK)
ok.grid(row = 3, column = 0)

sms = Button(frame1, text = 'Start',font= 30, width=10,height=1, command = start)
sms.grid(row = 2, column = 1)

root.mainloop()
