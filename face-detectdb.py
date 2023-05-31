import os
import cv2
import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
def face():
 face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
 cap = cv2.VideoCapture(0)
 x = 0

 db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anis1234",
    database='firstp'
 )

 root = tk.Tk()
 root.title('Login')
 root.geometry('925x500+200+100')
 root.configure(bg="#fff")
 root.resizable(False, False)

 def add_data():
    nom = first_name_entry.get()
    prenom = last_name_entry.get()
    titre = spec_entry.get()
    age = age_spinbox.get()
   

    # Save the image path in the database
    label = nom.replace(" ", "-").lower()
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    os.makedirs(os.path.join(image_dir, label), exist_ok=True)
    image_path = os.path.join(image_dir, label, f"{x}.png")

    query = "INSERT INTO employer (Nomemployer, photoemployer, prenom, titre, age) VALUES (%s, %s, %s, %s, %s,)"
    values = (nom, image_path, prenom, titre, age)

    try:
        cur = db.cursor()
        cur.execute(query, values)
        db.commit()
        messagebox.showinfo("Success", "Data added to the database")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to add data to the database: {error}")
    finally:
        cur.close()

 def delete_data():
    nom = first_name_entry.get()
    prenom = last_name_entry.get()
    titre = spec_entry.get()
    age = age_spinbox.get()

    query = "DELETE FROM employer WHERE Nomemployer = %s AND Prenom = %s AND Titre = %s AND Age = %s"
    values = (nom, prenom, titre, age)

    try:
        cur = db.cursor()
        cur.execute(query, values)
        db.commit()
        messagebox.showinfo("Success", "Data deleted from the database")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Failed to delete data from the database: {error}")
    finally:
        cur.close()

 def start_face_detection():
    global x
    nom = first_name_entry.get()
    label = nom.replace(" ", "-").lower()
    pathh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", label)
    os.makedirs(pathh, exist_ok=True)

    while True:
        ret, img = cap.read()
        if not ret:
            print("Error: Cannot access the camera.")
            break

        cv2.imshow('img', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        col = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_col = col[y:y+h, x:x+w]
            cv2.imshow('img', img)
            x += 1
            cv2.imwrite(os.path.join(pathh, f"{x}.png"), roi_gray)
            cv2.imwrite(os.path.join(pathh, f"{x}_col.png"), roi_col)

        if len(faces) == 0:
            print("No faces detected.")

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    train_faces_db()

 def train_faces_db():
    # Add code to retrieve image files from the directory where face images were saved
    # Iterate over the image files and process each image to extract facial features
    # Use the extracted facial features to train a face recognition model or update an existing model
    # Update the database with the trained or updated face recognition data
    pass

 def start_face_detection_and_add_data():
    add_data()
    start_face_detection()

 frame = tk.Frame(root)
 frame.grid(row=1, column=4, padx=20, pady=10)

 user_info_frame = tk.LabelFrame(frame, text="Information sur l'employer")
 user_info_frame.grid(row=0, column=0, padx=10, pady=10)

 first_name_label = tk.Label(user_info_frame, text="Nom")
 first_name_label.grid(row=0, column=0)
 last_name_label = tk.Label(user_info_frame, text="Prenom")
 last_name_label.grid(row=0, column=1)

 first_name_entry = tk.Entry(user_info_frame)
 last_name_entry = tk.Entry(user_info_frame)
 first_name_entry.grid(row=1, column=0)
 last_name_entry.grid(row=1, column=1)

 spec_label = tk.Label(user_info_frame, text="specialite")
 spec_entry = tk.Entry(user_info_frame)
 spec_label.grid(row=0, column=2)
 spec_entry.grid(row=1, column=2)

 age_label = tk.Label(user_info_frame, text="Age")
 age_spinbox = tk.Spinbox(user_info_frame, from_=18, to=60)
 age_label.grid(row=2, column=0)
 age_spinbox.grid(row=3, column=0)


 ajoutB = tk.Button(root, text='Ajouter', command=start_face_detection_and_add_data)
 ajoutB.grid(row=2, column=2, padx=20, pady=10)

 supprimerB = tk.Button(root, text='Supprimer', command=delete_data)
 supprimerB.grid(row=2, column=3, padx=20, pady=10)

 root.mainloop()

 db.close()
