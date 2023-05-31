import mysql.connector
import os
import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 

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

    query = "INSERT INTO employer (nom, photoemployer, prenom, titre, age) VALUES (%s, %s, %s, %s, %s,)"
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

    query = "DELETE FROM employer WHERE nom = %s AND prenom = %s AND titre = %s AND age = %s"
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

def select_data(tree):
    curItem = tree.focus()
    values = tree.item(curItem, "values")
    print(values)
    f = tk.Frame(r, width=400, height=320, background="grey")
    f.place(x=100, y=250)
    l1 = tk.Label(f, text="Nom", width=8, font=('Times', 11, 'bold'))
    e1 = tk.Entry(f, textvariable=name, width=25)
    l1.place(x=50, y=30)
    e1.place(x=170, y=30)

    l2 = tk.Label(f, text="Prénom", width=8, font=('Times', 11, 'bold'))
    e2 = tk.Entry(f, textvariable=gender, width=25)
    l2.place(x=50, y=70)
    e2.place(x=170, y=70)

    l4 = tk.Label(f, text="Age", width=8, font=('Times', 11, 'bold'))
    l4.place(x=50, y=150)
    e4 = tk.Entry(f, textvariable=email, width=25)
    e4.place(x=170, y=150)

    l5 = tk.Label(f, text="Specialitee", width=8, font=('Times', 11, 'bold'))
    l5.place(x=50, y=190)
    e5 = tk.Entry(f, textvariable=image, width=25)
    e5.place(x=170, y=190)
    e5.delete(0, tk.END)

    e1.insert(0, values[1])
    e2.insert(0, values[2])
    e4.insert(0, values[3])
    e5.insert(0, values[4])

    def update_data():
        nonlocal e1, e2, e4, e5, curItem, values
        s_name = name.get()
        g = gender.get()
        e = email.get()
        p = image.get()

        tree.item(curItem, values=(values[0], s_name, g, e, p))
        conn.execute(
            "UPDATE employer SET nom=%s, prenom=%s, age=%s, titre=%s WHERE id=%s",
            (s_name, g, e, p, values[0])
        )
        db.commit()
        messagebox.showinfo("Success", "Employer data updated")
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        e4.delete(0, tk.END)
        e5.delete(0, tk.END)
        f.destroy()

    savebutton = tk.Button(f, text="Update", command=update_data)
    savebutton.place(x=100, y=270)
    cancelbutton = tk.Button(f, text="Cancel", command=f.destroy)
    cancelbutton.place(x=200, y=270)

r = tk.Tk()
r.geometry("600x600")
r.title("User Details")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anis1234",
    database="firstp"
)

conn = db.cursor()
conn.execute("SELECT * FROM employer ORDER BY id")
rows = conn.fetchall()

tree = ttk.Treeview(r)
tree['show'] = 'headings'

s = ttk.Style(r)
s.theme_use("clam")
s.configure(".", font=('Helvetica', 11))
s.configure("Treeview.Heading", foreground='red', font=('Helvetica', 11, "bold"))

# Define number of columns
tree["columns"] = ("id", "nom", "prenom", "age", "titre")

# Assign the width, minwidth, and anchor to the respective columns
tree.column("id", width=50, minwidth=50, anchor=tk.CENTER)
tree.column("nom", width=100, minwidth=100, anchor=tk.CENTER)
tree.column("prenom", width=50, minwidth=50, anchor=tk.CENTER)
tree.column("age", width=150, minwidth=150, anchor=tk.CENTER)
tree.column("titre", width=150, minwidth=150, anchor=tk.CENTER)

# Assign the heading names to the respective columns
tree.heading("id", text="Id", anchor=tk.CENTER)
tree.heading("nom", text="Nom", anchor=tk.CENTER)
tree.heading("prenom", text="Prénom", anchor=tk.CENTER)
tree.heading("age", text="Age", anchor=tk.CENTER)
tree.heading("titre", text="Spécialitée", anchor=tk.CENTER)

for row in rows:
    if row[0] % 2 == 0:
        tree.insert('', "end", text="", values=row, tags=("even",))
    else:
        tree.insert('', "end", text="", values=row, tags=("odd",))

tree.tag_configure("even", foreground="black", background="white")
tree.tag_configure("odd", foreground="white", background="black")

hsb = ttk.Scrollbar(r, orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill=tk.X, side=tk.BOTTOM)

vsb = ttk.Scrollbar(r, orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(fill=tk.Y, side=tk.RIGHT)

tree.pack()

name = tk.StringVar()
gender = tk.StringVar()
email = tk.StringVar()
image = tk.StringVar()

insertbutton = tk.Button(r, text="Insert", command=face)
insertbutton.configure(font=('calibri', 14, 'bold'), bg='green', fg='white')
insertbutton.place(x=200, y=260)

updatebutton = tk.Button(r, text="Update", command=lambda: select_data(tree))
updatebutton.configure(font=('calibri', 14, 'bold'), bg='blue', fg='white')
updatebutton.place(x=400, y=260)

r.mainloop()
