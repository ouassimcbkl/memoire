from tokenize import String
import mysql.connector
from datetime import datetime, timedelta
from calendar import monthrange
import shutil
import tkinter as tk
from tkinter import messagebox
import os

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anis1234",
    database='firstp'
)

root = tk.Tk()
root.title('login')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
root.resizable(False, False)

lb = tk.Label(root, text='Entrer le nom :')
lb.grid(row=0, column=0, padx=5, pady=5)
entryName = tk.Entry(root)
entryName.grid(row=0, column=1, padx=5, pady=5)

lbP = tk.Label(root, text='Entrer le prénom :')
lbP.grid(row=1, column=0, padx=5, pady=5)
entryP = tk.Entry(root)
entryP.grid(row=1, column=1, padx=5, pady=5)


cur = db.cursor()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")


def Verif():
    name = entryName.get()
    label = name.replace(" ", "-").lower()
    print(label)
    labell = label.split()
    req = "SELECT * FROM employer WHERE Nomemployer = %s"
    cur.execute(req, labell)
    nomm = cur.fetchone()
    print(nomm)
    if nomm is None:
        print("Entrer un nom déjà disponible")
    else:
        Delete(labell, label)


def Delete(name, label):
    req2 = "DELETE FROM employer WHERE Nomemployer = %s"
    cur.execute(req2, name)
    pathh = os.path.join(image_dir, label)
    shutil.rmtree(pathh)
    db.commit()


    
suppB = tk.Button(root, text='supprimer', bg="red", command=Verif)
suppB.grid(row=2, column=0, padx=18, pady=18)



root.mainloop()
