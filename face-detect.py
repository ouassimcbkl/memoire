import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
path="images/Anis/"
cap=cv2.VideoCapture(0)
x=0
while(True):
       ret,img = cap.read()
       if(ret==0):
           print("erreur la camera ne s'allume pas")
           break
       else:
            cv2.imshow('img',img)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces=face_cascade.detectMultiScale(gray,1.3,5)

            col=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            for(x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray=gray[y:y+h, x:x+w] 
                roi_col=col[y:y+h, x:x+w] 
                cv2.imshow('img',img)
                x+=1
                cv2.imwrite(path + str(x)+".png",roi_gray)
                cv2.imwrite(path + str(x)+".png",roi_col)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                 break
cap.release()
cv2.destroyAllWindows()