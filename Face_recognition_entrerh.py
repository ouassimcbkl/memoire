from asyncio.windows_events import NULL
from turtle import width
import numpy as np
import cv2
import os
import pickle
import mysql.connector
from datetime import datetime


db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "anis1234",
  database='firstp'
)
cur = db.cursor()
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face-trainner.yml")
name=NULL
labels={"person_name": 1}
with open("labels.pickle",'rb') as f :
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = [] 
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def markdb(n,t):
    req = "SELECT id FROM employer WHERE Nomemployer= %s"
    req2 = "SELECT * FROM entrer WHERE date= %s AND idemp= %s"
    name=n.split()
    print(name)
    res=cur.execute(req,name)
    nom = cur.fetchone()
    print(nom)
    for item in nom:
        k = item
    #print(k)
    temp=(t,k)
    res=cur.execute(req2,temp)
    T = cur.fetchone()
    #print(nom)
    #print(T)
    if T==None :
        now = datetime.now()
        date=now.strftime('%Y-%m-%d')
        heure=now.strftime('%H:%M:%S')
        if now.hour >= 9 :
            req3="INSERT INTO entrer (idemp,date,heure,retard) VALUES (%s,%s,%s,%s)"
            Trrue="true"
            TT=(k,date,heure,Trrue)
            res=cur.execute(req3,TT)
            db.commit()
            print(n)
            return True
        else:
            req3="INSERT INTO entrer (idemp,date,heure) VALUES (%s,%s,%s)"
            TT=(k,date,heure)
            res=cur.execute(req3,TT)
            db.commit()
            print(n)
            return True



var = False
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        #print(x,y,w,h)
        roi_gray=gray[y:y+h, x:x+w] 
        roi_color=frame[y:y+h, x:x+w] 

        
        id_,conf = recognizer.predict(roi_gray)
        if conf>=45 and conf <=85 :
            #print(id_)
            #print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        img_item="my-image.png" 
        if(name!=NULL):
            now = datetime.now()
            date=now.strftime('%Y-%m-%d')
            var=markdb(name,date) 
            
            #markAttendance(name)
        cv2.imwrite(img_item, roi_gray)

        color = (255,0,0)
        stroke=2 
        width= x + w
        height = y + h
        cv2.rectangle(frame, (x,y),(width,height), color,stroke)

    cv2.imshow('frame',frame)
    if var==True:
        break
        cap.release()
        cv2.destroyAllWindows()
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
