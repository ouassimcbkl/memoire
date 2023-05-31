import cv2
import os
import numpy as np
from PIL import Image
import pickle
import mysql.connector

db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "anis1234",
  database='firstp'
)
print(db)
cur = db.cursor()
sql = "INSERT INTO employer (titre,Nomemployer,prenom,age,email,tel,Photoemployer) VALUES (%s, %s,%s, %s,%s, %s,%s)"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR ,"images")
#print(image_dir)
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root,dirs,files in os.walk(image_dir):
    for file in files :
        if file.endswith("png") or file.endswith("jpg") :
            path = os.path.join(root,file)
            label = os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            #print(label,path)
            print(path)
            if not label in label_ids:
                value = (label, root)
                valuee = label.split()
                #print(valuee)
                req = "SELECT * FROM employer WHERE Nomemployer= %s"
                res=cur.execute(req,valuee)
                nom = cur.fetchone()
                print(nom)
                if nom==None :
                    cur.execute(sql, value)
                    db.commit()
                label_ids[label]=current_id
                current_id +=1


                id_=label_ids[label]
                #print(label_ids)
                #y_labels.append(label)
                #x_train.append(path)
                pil_image = Image.open(path).convert("L") #importer limage et la mettre en gris
                #size=(550,550)
                #final_image = pil_image.resize(size, Image.Resampling.LANCZOS)
                #image_array = np.array(final_image,"uint8")
                image_array = np.array(pil_image,"uint8")
                #print(image_array)
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
                #print(faces)

                for(x,y,w,h) in faces :
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)
                    #print(faces)
                
print(y_labels)
print(x_train)

with open("labels.pickle",'wb') as f :
     pickle.dump(label_ids,f)
recognizer.train(x_train, np.array(y_labels))
recognizer.save("face-trainner.yml")
