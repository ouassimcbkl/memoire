from tkinter import *
from tkinter import messagebox
from datetime import date
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import mysql.connector
from mysql.connector import Error
import tkinter
from PIL import Image, ImageTk
import os
import cv2
from tkinter.ttk import Combobox
from datetime import datetime, timedelta
from calendar import monthrange

root = Tk()
root.title('login')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
root.resizable(False, False)


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

    boot = tk.Tk()
    boot.title('Login')
    boot.geometry('925x500+200+100')
    boot.configure(bg="#fff")
    boot.resizable(False, False)

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

        query = "INSERT INTO employer (Nomemployer, photoemployer, prenom, titre, age) VALUES (%s, %s, %s, %s, %s)"
        values = (nom, image_path, prenom, titre, age)

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database='firstp'
            )
            cur = db.cursor()
            cur.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Data added to the database")
        except Error as error:
            messagebox.showerror("Error", f"Failed to add data to the database: {error}")
        finally:
            if db.is_connected():
                cur.close()
                db.close()

    def delete_data():
        nom = first_name_entry.get()
        prenom = last_name_entry.get()
        titre = spec_entry.get()
        age = age_spinbox.get()

        query = "DELETE FROM employer WHERE Nomemployer = %s AND prenom = %s AND titre = %s AND age = %s"
        values = (nom, prenom, titre, age)

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database='firstp'
            )
            cur = db.cursor()
            cur.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Data deleted from the database")
        except Error as error:
            messagebox.showerror("Error", f"Failed to delete data from the database: {error}")
        finally:
            if db.is_connected():
                cur.close()
                db.close()

    def start_face_detection():
        nonlocal x
        nom = first_name_entry.get()
        label = nom.replace(" ", "-").lower()
        pathh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", label)
        os.makedirs(pathh, exist_ok=True)

        while True:
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                cv2.imwrite(f"{pathh}/{x}.png", roi_gray)

                color = (255, 0, 0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

            cv2.imshow('frame', frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        # Increase the counter after face detection
        x += 1

    def register_face():
        nonlocal x
        if len(first_name_entry.get()) == 0:
            messagebox.showwarning("Warning", "Please enter your name")
        else:
            start_face_detection()

    background_image = ImageTk.PhotoImage(file='C:/Users/ANIS/Desktop/my work3/background.jpg')
    background_label = Label(boot, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    first_name = Label(boot, text="Nom : ", font=('calibre', 10, 'bold'), bg="#fff")
    first_name.place(x=50, y=200)
    first_name_entry = Entry(boot, font=('calibre', 10, 'normal'), width=20)
    first_name_entry.place(x=200, y=200)

    last_name = Label(boot, text="Prénom : ", font=('calibre', 10, 'bold'), bg="#fff")
    last_name.place(x=400, y=200)
    last_name_entry = Entry(boot, font=('calibre', 10, 'normal'), width=20)
    last_name_entry.place(x=550, y=200)

    spec = Label(boot, text="Titre : ", font=('calibre', 10, 'bold'), bg="#fff")
    spec.place(x=50, y=250)
    spec_entry = Entry(boot, font=('calibre', 10, 'normal'), width=20)
    spec_entry.place(x=200, y=250)

    age_label = Label(boot, text="Age :", font=('calibre', 10, 'bold'), bg="#fff")
    age_label.place(x=400, y=250)
    age_spinbox = Spinbox(boot, from_=18, to=100, font=('calibre', 10, 'normal'), width=18)
    age_spinbox.place(x=550, y=250)

    insertbutton = Button(boot, text="Inserer les données", command=add_data, font=('calibre', 10, 'bold'))
    insertbutton.place(x=50, y=300)
    deletebutton = Button(boot, text="Supprimer les données", command=delete_data, font=('calibre', 10, 'bold'))
    deletebutton.place(x=200, y=300)
    register_button = Button(boot, text="Capturer une photo", command=register_face, font=('calibre', 10, 'bold'))
    register_button.place(x=50, y=350)

    boot.mainloop()


def add_image():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
    )

    def show_image():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return
        item_values = treeview.item(selected_item)
        image_path = item_values['values'][2]
        if image_path:
            image = Image.open(image_path)
            image.show()
        else:
            messagebox.showwarning("Warning", "No image found")

    def browse_file():
        file_path = filedialog.askopenfilename(initialdir="/", title="Select Image", filetypes=(("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")))
        image_path_entry.delete(0, END)
        image_path_entry.insert(END, file_path)

    def add_image_to_db():
        nom = emp_name.get()
        image_path = image_path_entry.get()

        query = "UPDATE employer SET photoemployer = %s WHERE Nomemployer = %s"
        values = (image_path, nom)

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database='firstp'
            )
            cur = db.cursor()
            cur.execute(query, values)
            db.commit()
            messagebox.showinfo("Success", "Image added to the database")
        except Error as error:
            messagebox.showerror("Error", f"Failed to add image to the database: {error}")
        finally:
            if db.is_connected():
                cur.close()
                db.close()

    background_image = ImageTk.PhotoImage(file='C:/Users/ANIS/Desktop/my work3/background.jpg')
    background_label = Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label = Label(root, text="Ajouter une image", font=('calibre', 20, 'bold'), bg="#fff")
    label.pack(pady=20)

    treeframe = Frame(root, bd=4, relief=RIDGE, bg="white")
    treeframe.place(x=400, y=120, width=500, height=400)

    scroll_x = Scrollbar(treeframe, orient=HORIZONTAL)
    scroll_y = Scrollbar(treeframe, orient=VERTICAL)

    treeview = ttk.Treeview(treeframe, columns=("ID", "Nom", "Chemin de l'image"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.config(command=treeview.xview)
    scroll_y.config(command=treeview.yview)
    treeview.heading("ID", text="ID")
    treeview.heading("Nom", text="Nom")
    treeview.heading("Chemin de l'image", text="Chemin de l'image")
    treeview['show'] = 'headings'
    treeview.pack(fill=BOTH, expand=1)

    query = "SELECT idemployer, Nomemployer, photoemployer FROM employer"
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anis1234",
            database='firstp'
        )
        cur = db.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            treeview.insert('', END, values=row)
    except Error as error:
        messagebox.showerror("Error", f"Failed to fetch data from the database: {error}")
    finally:
        if db.is_connected():
            cur.close()
            db.close()

    show_button = Button(root, text="Afficher l'image", command=show_image, font=('calibre', 10, 'bold'))
    show_button.place(x=250, y=220)

    emp_name_label = Label(root, text="Nom de l'employé : ", font=('calibre', 10, 'bold'), bg="#fff")
    emp_name_label.place(x=50, y=300)
    emp_name = Entry(root, font=('calibre', 10, 'normal'), width=20)
    emp_name.place(x=200, y=300)

    image_path_label = Label(root, text="Chemin de l'image : ", font=('calibre', 10, 'bold'), bg="#fff")
    image_path_label.place(x=50, y=350)
    image_path_entry = Entry(root, font=('calibre', 10, 'normal'), width=30)
    image_path_entry.place(x=200, y=350)
    browse_button = Button(root, text="Parcourir", command=browse_file, font=('calibre', 10, 'bold'))
    browse_button.place(x=450, y=345)
    add_image_button = Button(root, text="Ajouter l'image", command=add_image_to_db, font=('calibre', 10, 'bold'))
    add_image_button.place(x=200, y=400)


def display_pages(page):
    for widget in root.winfo_children():
        widget.destroy()
    if page == 1:
        face()
    elif page == 2:
        add_image()


btn_face = Button(root, text="Page 1: Reconnaissance faciale", command=lambda: display_pages(1), font=('calibre', 12, 'bold'))
btn_face.pack(pady=20)
btn_add_image = Button(root, text="Page 2: Ajouter une image", command=lambda: display_pages(2), font=('calibre', 12, 'bold'))
btn_add_image.pack(pady=20)

root.mainloop()
