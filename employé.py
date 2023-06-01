import shutil
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
import re
import cv2
from tkinter.ttk import Combobox
import re
import mysql.connector
from datetime import datetime, timedelta
from calendar import monthrange
import tkinter.font as tkFont

import pathlib
import sqlite3 

root = Tk()
root.title('CamPoint')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
# root.state('zoomed')
root.resizable(False, False)


def on_closing():
    if messagebox.askokcancel("Quit", "Voulez-vous quitter cette page ?"):
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

button_quit = Button(root, text="X",
                     font=("TKHeadingFont", 15),
                     bg="#FA270F",
                     fg='white',
                     cursor="hand2",
                     activebackground="#C6BEBD",
                     activeforeground="black",
                     anchor="center",
                     command=lambda: [cv2.destroyAllWindows(), root.destroy()]
                     )
button_quit.grid(row=0, column=1, padx=30, pady=20)

def signin():
    employee_id = user.get()

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anis1234",
            database="firstp"
        )

        cursor = db.cursor()

        # Check if the employee ID exists in the database
        query = "SELECT * FROM employer WHERE id = %s"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        if result:
            # Employee ID exists in the database
            root.withdraw()

            r = Toplevel(root)
            r.title('accueil')
            r.geometry('925x500+200+100')
            image_icon = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
            r.iconphoto(False, image_icon)

            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database="firstp"
            )

            cur = db.cursor()



                    
            query = "SELECT Nomemployer, prenom, titre, age, email, tel, salaire FROM employer WHERE id = %s"
            cur.execute(query, (employee_id,))
            employee_data = cur.fetchone()
            
            cur.close()
            db.close()
            
            
            
            
            labels = ["Nom", "Prénom", "Titre", "Âge", "Email", "Téléphone", "Salaire"]
            for i in range(len(labels)):
                Label(r, text=labels[i]).grid(row=i, column=0, sticky=W)
            
            for i in range(len(employee_data)):
                Label(r, text=employee_data[i]).grid(row=i, column=1, sticky=W)
            
            
            # Rest of your code for the home page

        else:
            messagebox.showerror("Error", "Invalid ID")

    except Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if db.is_connected():
            cursor.close()
            db.close()


image_icon = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
root.iconphoto(False, image_icon)
img = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='CamPoint', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)


def on_entry_click(event):
    if user.get() == 'id':
        user.delete(0, END)
        user.configure(fg='black')


def on_exit(event):
    if user.get() == '':
        user.insert(0, 'id')
        user.configure(fg='gray')


user = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'id')
user.bind('<FocusIn>', on_entry_click)
user.bind('<FocusOut>', on_exit)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)


Button(frame, width=39, pady=7, text='Confirmer', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=150)


root.mainloop()
