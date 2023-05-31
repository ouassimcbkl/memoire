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

import pathlib
import sqlite3 

root = Tk()
root.title('login')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
# root.state('zoomed')
root.resizable(False, False)
def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
         root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
button_quit = Button(root,text="X",
          font=("TKHeadingFont",15),
          bg="#FA270F",
          fg='white',
          cursor="hand2",
          activebackground="#C6BEBD",
          activeforeground="black",
          anchor="center",
          command=lambda: [cv2.destroyAllWindows(), root.destroy()]
            )
button_quit.grid(row=0, column=1,padx=30,pady=20)


def rotard():
 doot = Tk()
 doot.title('retard')
 doot.geometry('925x500+200+100')
 doot.configure(bg="#fff")
 doot.resizable(False, False)


 def moi():
    
    frame = Frame(doot, bg="#e0eaf5")
    frame.pack(pady=20)
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
     )


    cur = db.cursor()
    now = datetime.now()
    S = now.strftime('%Y-%m-%d')
    today_date = datetime.now().date()
    year = today_date.year
    month = today_date.month
    days_in_month = monthrange(year, month)[1]
    next_month = today_date - timedelta(days=days_in_month)
    SSSS = next_month.strftime('%Y-%m-%d')
    value = (S, SSSS)
    req3 = "SELECT employer.Nomemployer, COUNT(entrer.id) FROM entrer, employer WHERE retard ='true' AND entrer.idemp = employer.id AND date <= %s AND date >= %s GROUP BY employer.Nomemployer"

    cur.execute(req3, value)
    nom = cur.fetchall()
    print(nom)

    result_label = Label(frame, text="Nomber de retard par mois :", font=("Arial", 14), bg="#e0eaf5")
    result_label.pack()

    for row in nom:
        employer_name = row[0]
        entry_count = row[1]
        result_text = f"Employer: {employer_name}, Entry Count: {entry_count}"
        result_entry = Label(frame, text=result_text, font=("Arial", 12), bg="#e0eaf5")
        result_entry.pack(pady=5)

    
 moi()

 
 def retard ():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
    )
    
    frame = Frame(doot, bg="#e0eaf5")
    frame.pack(pady=20)

    def refresh_data():
        # Perform the refresh logic here
        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        print("Refreshing data for date:", current_date)

        # Execute your SQL queries or update the display as needed

        # Clear the previous data and display the refreshed data
        result_label.config(text="Retard aujourdhui: " + current_date)

    cur = db.cursor()
    now = datetime.now()
    S = now.strftime('%Y-%m-%d')
    print(S)
    SS = S.split()
    req = "SELECT ALL employer.Nomemployer FROM entrer, employer WHERE date = %s and retard ='true' and entrer.idemp = employer.id"
    req3 = "SELECT ALL * FROM entrer WHERE retard ='true'"
    req2 = "SELECT * FROM entrer WHERE date = %s AND idemp = %s"

    res = cur.execute(req, SS)
    nom = cur.fetchall()
    print(nom)

    # Create a Label to display the data
    refresh_button = Button(frame, text="Refresh", command=refresh_data, font=("Arial", 12), bg="#4299e1", fg="#ffffff")
    refresh_button.pack()

    result_label = Label(frame, text="Data will be displayed here.", font=("Arial", 14), bg="#e0eaf5")
    result_label.pack(pady=10)

    # Create a separate Label for each row of data and pack them into the root window
    for row in nom:
        row_label = Label(frame, text=row, font=("Arial", 12), bg="#e0eaf5")
        row_label.pack(pady=5)


    doot.mainloop()
 retard()


def absence():
 noot = tk.Tk()
 noot.title('abssence')
 noot.geometry('925x500+200+100')
 noot.configure(bg="#fff")
 noot.resizable(False, False)
 
def now():
    # Create the Tkinter window
    noot = tk.Tk()
    noot.title('absence')
    noot.geometry('925x500+200+100')
    noot.configure(bg="#fff")
    noot.resizable(False, False)

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
    )
    cur = db.cursor()

    # Function to delete an employee from the database and Treeview
    def delete_employee(event):
        # Get the selected item from the Treeview
        selected_item = tree.focus()
        if not selected_item:
            return

        # Retrieve the employee ID from the selected item
        employee_id = tree.item(selected_item)['values'][0]

        # Confirmation dialog for deleting the employee
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this employee?")

        if confirm:
            try:
                # Delete the employee from the database
                delete_query = "DELETE FROM employer WHERE id = %s"
                cur.execute(delete_query, (employee_id,))
                db.commit()

                # Delete the employee from the Treeview
                tree.delete(selected_item)
            except mysql.connector.Error as error:
                messagebox.showerror("Error", str(error))

    # Fetch data from the database
    now = datetime.now()
    S = now.strftime('%Y-%m-%d')
    today_date = datetime.now().date()
    value = (S,)

    req2 = "SELECT employer.Nomemployer, COUNT(entrer.id) FROM employer LEFT JOIN entrer ON employer.id = entrer.idemp WHERE NOT EXISTS (SELECT * FROM entrer WHERE entrer.idemp = employer.id AND date = %s) GROUP BY employer.Nomemployer"
    cur.execute(req2, value)
    absent_employees = cur.fetchall()

    # Create a Treeview widget
    tree = ttk.Treeview(noot, columns=("Name"), show="headings")

    tree.column("Name", width=100)
    


    # Insert data into the Treeview
    for employee in absent_employees:
        tree.insert("", tk.END, values=employee + ("Delete",), tags=("Delete",))

    # Add horizontal scrollbar
    hsb = ttk.Scrollbar(noot, orient="horizontal", command=tree.xview)
    hsb.pack(fill=tk.X, side=tk.BOTTOM)
    tree.configure(xscrollcommand=hsb.set)

    tree.pack(fill=tk.BOTH, expand=True)

    noot.mainloop()





def mois():
# Create the Tkinter window
  toot = tk.Tk()
  toot.title('abssence')
  toot.geometry('925x500+200+100')
  toot.configure(bg="#fff")
  toot.resizable(False, False)

# Connect to the MySQL database
  db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anis1234",
    database='firstp'
   )
  cur = db.cursor()

# Function to delete an employee from the database and Treeview
 
# Fetch data from the database
  now = datetime.now()
  S = now.strftime('%Y-%m-%d')
  today_date = datetime.now().date()
  year = today_date.year
  month = today_date.month
  days_in_month = monthrange(year, month)[1]
  next_month = today_date - timedelta(days=days_in_month)
  SSSS = next_month.strftime('%Y-%m-%d')
  value = (S, SSSS)
  now = datetime.now()
  S=now.strftime('%Y-%m-%d')
  print(S)
  SS=S.split()
  dd="SELECT DATEDIFF(CURDATE(), DATE_FORMAT(CURDATE(), '%Y-%m-01')) AS difference_en_jours"
  req2 = "SELECT Nomemployer FROM employer WHERE NOT EXISTS ( SELECT * FROM entrer WHERE entrer.idemp = employer.id and date=%s )"
  qqqq = "SELECT employer.Nomemployer, ( %s - COUNT(entrer.id)) AS nombre_absences FROM employer LEFT JOIN entrer ON employer.id = entrer.idemp AND entrer.date >= DATE_FORMAT(CURDATE(), '%Y-%m-01') GROUP BY employer.id, employer.Nomemployer;"
  cur.execute(dd)
  result = cur.fetchall()
  my_tuple = [(29,)]
  liste = [my_tuple[0][0]]
  print(liste)
  cur.execute(qqqq,liste)
  result = cur.fetchall()
  print(result)
  res=cur.execute(req2,SS)
  nom = cur.fetchall()
  print(nom)
  set_tuple1 = set(item[0] for item in nom)

# Ajouter la colonne "True" à tuple2 si la valeur correspondante existe dans tuple1
  tuple2_with_column = [(item[0], item[1], True) if item[0] in set_tuple1 else item for item in result]
  tuple22_with_column = [(item[0], item[1], True if item[0] in set_tuple1 else False) for item in result]
  print(tuple22_with_column)
  tree = ttk.Treeview(toot, columns=("Name", "Absences", "Absent"), show="headings")

  tree.column("Name", width=300)
  tree.column("Absences", width=150)
  tree.column("Absent", width=100)

  tree.heading("Name", text="Name")
  tree.heading("Absences", text="Absences")
  tree.heading("Absent", text="Absent")

# Insert data into the Treeview
  for row in tuple22_with_column:
    tree.insert("", tk.END, values=row )

# Add horizontal scrollbar
  hsb = ttk.Scrollbar(toot, orient="horizontal", command=tree.xview)
  hsb.pack(fill=tk.X, side=tk.BOTTOM)
  tree.configure(xscrollcommand=hsb.set)

# Add vertical scrollbar
  vsb = ttk.Scrollbar(toot, orient="vertical", command=tree.yview)
  vsb.pack(fill=tk.Y, side=tk.RIGHT)
  tree.configure(yscrollcommand=vsb.set)



# Display the number of absences
  label_count = tk.Label(toot, text="Number of absences within the last 30 days: {}".format(len(result)), font=('calibre', 14, 'bold'), bg="#fff")
  label_count.pack()

# Display the Treeview widget
  tree.pack(fill=tk.BOTH, expand=True)

  toot.mainloop()

 
def signin():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == 'aaaa':
        root.withdraw()

        r = Toplevel(root)
        r.title('acceuil')
        r.geometry('925x500+200+100')
        image_icon = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\peter-dinklage\\1.png")
        r.iconphoto(False, image_icon)
  

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
        s.configure("Treeview.Heading", foreground='#57a1f8', font=('Helvetica', 11, "bold"))

# Define number of columns
        tree["columns"] = ("id", "nom", "prenom", "age", "titre")

# Assign the width, minwidth, and anchor to the respective columns
        tree.column("id", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("nom", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("prenom", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("age", width=150, minwidth=150, anchor=tk.CENTER)
        tree.column("titre", width=150, minwidth=150, anchor=tk.CENTER)

# Assign the heading names to the respective columns
        tree.heading("id", text="Id", anchor=tk.CENTER)
        tree.heading("nom", text="Nom", anchor=tk.CENTER)
        tree.heading("prenom", text="Prénom", anchor=tk.CENTER)
        tree.heading("age", text="Age", anchor=tk.CENTER)
        tree.heading("titre", text="Spécialitée", anchor=tk.CENTER)
        t = 1;  
        for row in rows:
          if t % 2 == 0:
              tree.insert('', "end", text="", values=row, tags=("even",),iid=row[0])
              t=t+1
          else:
              tree.insert('', "end", text="", values=row, tags=("odd",),iid=row[0])
              t=t+1

        tree.tag_configure("even", foreground='#57a1f8', background="black")
        tree.tag_configure("odd", foreground="black", background='#57a1f8')
        def get_selected_item(event):
            selected_item = tree.selection()[0]
            item_id = selected_item
            print("ID sélectionné :", item_id)
        def open_edit_window(event):
            selected_item = tree.selection()[0]
            item_values = tree.item(selected_item, "values")

            # Créer une nouvelle fenêtre pour l'édition
            edit_window = tk.Toplevel(r)

            # Créer les champs de modification des colonnes
            id_label = tk.Label(edit_window, text="ID:")
            id_label.pack()
            id_entry = tk.Entry(edit_window)
            id_entry.insert(0, item_values[0])
            id_entry.pack()

            nom_label = tk.Label(edit_window, text="Nom:")
            nom_label.pack()
            nom_entry = tk.Entry(edit_window)
            nom_entry.insert(0, item_values[1])
            nom_entry.pack()

            prenom_label = tk.Label(edit_window, text="Prénom:")
            prenom_label.pack()
            prenom_entry = tk.Entry(edit_window)
            prenom_entry.insert(0, item_values[2])
            prenom_entry.pack()

            age_label = tk.Label(edit_window, text="Âge:")
            age_label.pack()
            age_entry = tk.Entry(edit_window)
            age_entry.insert(0, item_values[3])
            age_entry.pack()

            titre_label = tk.Label(edit_window, text="Titre:")
            titre_label.pack()
            titre_entry = tk.Entry(edit_window)
            titre_entry.insert(0, item_values[4])
            titre_entry.pack()

        # Créer la fenêtre principale
        r = tk.Tk()

        # Créer le Treeview
        tree = ttk.Treeview(r)
        tree["columns"] = ("id", "nom", "prenom", "age", "titre")

        # ...

        # Lier la fonction à l'événement de sélection d'une ligne
        tree.bind("<<TreeviewSelect>>", open_edit_window)

        # ...

        # Afficher le Treeview
        tree.pack()
# Lier la fonction à l'événement de sélection d'une ligne
        tree.bind("<<TreeviewSelect>>", get_selected_item)

# Afficher le Treeview
        tree.pack()
        

        hsb = ttk.Scrollbar(r, orient="horizontal")
        hsb.configure(command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        hsb.pack(fill=tk.X, side=tk.BOTTOM)

        vsb = ttk.Scrollbar(r, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=tk.Y, side=tk.RIGHT)


        insertbutton = tk.Button(r,text="Ajout ou Supp",command=face)
        insertbutton.configure(font =('calibri', 14, 'bold'),bg='#57a1f8',fg='white',border=0)
        insertbutton.place(x=150,y=260)


        reterdtbutton = tk.Button(r,text="afficher retard",command=rotard)
        reterdtbutton.configure(font =('calibri', 14, 'bold'), bg='#57a1f8',fg='white',border=0)
        reterdtbutton.place(x=300,y=260)

        absentbutton = tk.Button(r,text="afficher absence",command=mois)
        absentbutton.configure(font =('calibri', 14, 'bold'),bg='#57a1f8',fg='white',border=0)
        absentbutton.place(x=450,y=260)


        abss = tk.Button(r,text="abssence",command=now)
        abss.configure(font =('calibri', 14, 'bold'), bg='#57a1f8',fg='white',border=0)
        abss.place(x=600,y=260)


      



        tree.pack()

        

        




     

    elif username!='aa'and password!='a':
        messagebox.showerror("invalid","invalid username and password")

    elif  password!='a':
        messagebox.showerror("invalid","invalid  password")

    elif username!='aa':
        messagebox.showerror("invalid","invalid username ")        



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
 boot.title('list')
 boot.geometry('925x500+200+100')
 boot.configure(bg="#fff")
 boot.resizable(False, False)

 def add_data():
    nom = first_name_entry.get()
    prenom = last_name_entry.get()
    titre = spec_entry.get()
    age = age_spinbox.get()
    email = email_entry.get()
    tel = tel_entry.get()

    # Save the image path in the database
    label = nom.replace(" ", "-").lower()
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    os.makedirs(os.path.join(image_dir, label), exist_ok=True)
    image_path = os.path.join(image_dir, label, f"{x}.png")

    query = "INSERT INTO employer (Nomemployer, photoemployer, prenom, titre, age, email,tel ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (label, image_path, prenom, titre, age, email, tel )

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
    email = email_entry.get()
    tel = tel_entry.get()


    query = "DELETE FROM employer WHERE Nomemployer = %s AND prenom = %s AND titre = %s AND age = %s AND email = %sAND tel = %s"
    values = (nom, prenom, titre, age, email ,tel )

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
    
      exec(open("./faces-train.py").read())
 
 path = "C:\\Users\Anis_\\OneDrive\\Bureau\\Desktop - 8 (1).png"
 img = ImageTk.PhotoImage(Image.open(path))
 panel = Label(root, image=img)
 panel.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
 def vall():
    nom = first_name_entry.get()
    prenom = last_name_entry.get()
    titre = spec_entry.get()
    age = age_spinbox.get()
    email=email_entry.get()
    phone_number = tel_entry.get()
    if ((len(nom)>0)and(len(prenom)>0)and(len(titre)>0)and(len(age)>1)and(len(email)>0)and(len(phone_number)>0)) :
        return True
    else:
        messagebox.showerror("Erreur", "Veuillez compléter toutes les cases, s'il vous plaît.")
        return False
 def validate_email():
    email=email_entry.get()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        print("Adresse e-mail valide.")
    else:
        print("Adresse e-mail invalide.")
 
 def valtel():
    phone_number = tel_entry.get()
    regex = r"^(0|\+213)(5|6|7)[0-9]{8}$"

    if re.match(regex, phone_number):
        print("Numéro de téléphone valide")
        return True
   
    else:
        messagebox.showerror("Erreur", "Le numéro doit comporter 13 chiffres.")
        print("Numéro de téléphone invalide")
        return False
 def validen():
    phone_number = tel_entry.get()
    regex = r"^(0|\+213)(5|6|7)[0-9]{8}$"
    email=email_entry.get()
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    age = age_spinbox.get()
    intage = int(age)
    if re.match(regex, phone_number) and re.match(pattern, email) and  intage>=18 :
        return True
    else:
        if re.match(pattern, email)==None:
           messagebox.showerror("Erreur", "La syntaxe de l'e-mail est incorrecte.") 
           return False
        else:
            if re.match(regex, phone_number)==None:
                messagebox.showerror("Erreur", "La syntaxe du numéro de téléphone est incorrecte") 
                return False
            else :
                if intage<18:
                    messagebox.showerror("Erreur", "L'âge doit être supérieur à 18 ans.") 
                    return False

 def start_face_detection_and_add_data():
    sur=False
    suur=False
    suur=vall()
    if suur==True:
        sur=validen()
        if sur==True:
            add_data()
            start_face_detection()
        
    
 

    # Label Frame
 frame1 = LabelFrame(boot, text="Register", font=('arial', 20, 'bold'), bd=20, relief='ridge', bg='sky blue', fg='black')
 frame1.place(x=280, y=20)

    # Labels
 first_name_label = Label(frame1, text="Nom employer", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 first_name_label.grid(row=0, column=0, padx=20, pady=10)

 last_name_label = Label(frame1, text="Prénom employer", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 last_name_label.grid(row=1, column=0, padx=20, pady=10)

 spec_label = Label(frame1, text="Spécialitée", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 spec_label.grid(row=2, column=0, padx=20, pady=10)

 email_label = Label(frame1, text="Email", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 email_label.grid(row=3, column=0, padx=20, pady=10)

 tel_label = Label(frame1, text="Télléphone", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 tel_label.grid(row=4, column=0,
                 padx=20, pady=10)

 age_label = Label(frame1, text="Age", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 age_label.grid(row=5, column=0, padx=20, pady=10)

    # Entry
 first_name_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 first_name_entry.grid(row=0, column=1, pady=10)
 last_name_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 last_name_entry.grid(row=1, column=1, pady=10)
 spec_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 spec_entry.grid(row=2, column=1, pady=10)

 email_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 email_entry.grid(row=3, column=1, pady=10)
 


             
 
 tel_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 tel_entry.grid(row=4, column=1, pady=10)

 tel_entry.insert(0, "+213")

# Function to handle the entry focus
# def handle_entry_focus(event):
 #   if tel_entry.get() == "":
  #      tel_entry.delete(0, '+213')

# Bind the focus event to the entry widget
 #tel_entry.bind("<FocusIn>", handle_entry_focus)
 
   #email


    # Spinbox
 age_spinbox = Spinbox(frame1, from_=18, to=65, width=5, font=('arial', 14, 'bold'))
 age_spinbox.grid(row=5, column=1, pady=10)

    # Buttons
 add_button = Button(frame1, text='Add', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=start_face_detection_and_add_data)
 add_button.grid(row=6, column=0, pady=10)
 delete_button = Button(frame1, text='Delete', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=delete_data)
 delete_button.grid(row=6, column=1, pady=10)


 

 db.close()


image_icon=PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
root.iconphoto(False,image_icon)
img = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480, y=70)

heading=Label(frame,text='sign in',fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)
###-----------------------------------

def on_entry_click(event):
    if user.get() == 'Username':
        user.delete(0, END)
        user.configure(fg='black')

def on_exit(event):
    if user.get() == '':
        user.insert(0, 'Username')
        user.configure(fg='gray')

user = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_entry_click)
user.bind('<FocusOut>', on_exit)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_password_entry_click(event):
    if code.get() == 'Password':
        code.delete(0, END)
        code.configure(show='*', fg='black')

def on_password_exit(event):
    if code.get() == '':
        code.insert(0, 'Password')
        code.configure(show='', fg='gray')

code = Entry(frame, width=25, fg='gray', border=0, bg='white', show='', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_password_entry_click)
code.bind('<FocusOut>', on_password_exit)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

##-------------------------------------

Button(frame,width=39,pady=7,text='sign in',bg='#57a1f8',fg='white',border=0, command=signin).place(x=35,y=204)


root.mainloop()


