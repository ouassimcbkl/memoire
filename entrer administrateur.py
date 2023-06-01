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
        if messagebox.askokcancel("Quit", "Voullez vous quitter cette page ?"):
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

    result_label = Label(frame, text="Nombre de retard par mois :", font=("Arial", 14), bg="#e0eaf5")
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
        print("Actualiser les données", current_date)

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
    refresh_button = Button(frame, text="Actualiser", command=refresh_data, font=("Arial", 12), bg="#4299e1", fg="#ffffff")
    refresh_button.pack()

    result_label = Label(frame, text="Données seront afficher ici.", font=("Arial", 14), bg="#e0eaf5")
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
    tree = ttk.Treeview(noot, columns=("Nom"), show="headings")

    tree.column("Nom", width=100)
    


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
  liste = [result[0][0]+1]
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
  tree = ttk.Treeview(toot, columns=("Nom", "Absences", "Absent"), show="headings")

  tree.column("Nom", width=300)
  tree.column("Absences", width=150)
  tree.column("Absent", width=100)

  tree.heading("Nom", text="Nom")
  tree.heading("Absences", text="Nombre d'absences")
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
  label_count = tk.Label(toot, text="Nombre d'absence dans le mois dernier : ", font=('calibre', 14, 'bold'), bg="#fff")
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
        r.title('accueil')
        r.geometry('925x500+200+100')
        image_icon = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
        r.iconphoto(False, image_icon)




        
        def liste():
            liste_frame = tk.Frame(main_frame)
            db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anis1234",
            database="firstp"
        )

            conn = db.cursor()
            conn.execute("SELECT * FROM employer ORDER BY id")
            rows = conn.fetchall()

            tree = ttk.Treeview(liste_frame)
            tree['show'] = 'headings'

            s = ttk.Style(liste_frame)
            s.theme_use("clam")
            s.configure(".", font=('Helvetica', 11))
            s.configure("Treeview.Heading", foreground='#57a1f8', font=('Helvetica', 11, "bold"))

        # Define number of columns
            tree["columns"] = ("id", "nom", "prenom", "titre", "age")

        # Assign the width, minwidth, and anchor to the respective columns
            tree.column("id", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("nom", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("prenom", width=150, minwidth=100, anchor=tk.CENTER)
            tree.column("titre", width=150, minwidth=150, anchor=tk.CENTER)
            tree.column("age", width=150, minwidth=150, anchor=tk.CENTER)

        # Assign the heading names to the respective columns
            tree.heading("id", text="Id", anchor=tk.CENTER)
            tree.heading("nom", text="Nom", anchor=tk.CENTER)
            tree.heading("prenom", text="Prénom", anchor=tk.CENTER)
            tree.heading("titre", text="Spécialitée", anchor=tk.CENTER)
            tree.heading("age", text="Age", anchor=tk.CENTER)
            t = 1
            for row in rows:
                    if t % 2 == 0:
                        tree.insert('', "end", text="", values=row, tags=("even",), iid=row[0])
                    else:
                        tree.insert('', "end", text="", values=row, tags=("odd",), iid=row[0])
                    t += 1

            tree.tag_configure("even", foreground='#57a1f8', background="black")
            tree.tag_configure("odd", foreground="black", background='#57a1f8')
            def get_selected_item(event):
                    selected_item = tree.selection()[0]
                    item_id = selected_item
                    print("ID sélectionné :", item_id)

        # Lier la fonction à l'événement de sélection d'une ligne
            tree.bind("<<TreeviewSelect>>", get_selected_item)

        # Afficher le Treeview
            tree.pack()

            hsb = ttk.Scrollbar(liste_frame, orient="horizontal")
            hsb.configure(command=tree.xview)
            tree.configure(xscrollcommand=hsb.set)
            hsb.pack(fill=tk.X, side=tk.BOTTOM)

            vsb = ttk.Scrollbar(liste_frame, orient="vertical")
            vsb.configure(command=tree.yview)
            tree.configure(yscrollcommand=vsb.set)
            vsb.pack(fill=tk.Y, side=tk.RIGHT)


            liste_frame.pack(pady=20)


        def ajou():
            home_frame = tk.Frame(main_frame)
            lb = tk.Label(home_frame,text='',font=('Bold',15))
            lb.pack()

            home_frame.pack(pady=20)
            

        def mod():
            mod_frame = tk.Frame(main_frame)
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database='firstp'
            )
            cur = db.cursor()

            # Function to clear all the data in the form
            def clear_data():
                first_name_entry.delete(0, 'end')
                last_name_entry.delete(0, 'end')
                spec_entry.delete(0, 'end')
                email_entry.delete(0, 'end')
                sal_entry.delete(0, 'end')
                tel_entry.delete(0, 'end')
                

            # Function to prefill the form fields with employee data
            def prefill_form():
                # Get the employee ID from the ID entry
                employe_id = id_entry.get()

                # Select query to retrieve employee data
                query = "SELECT Nomemployer, prenom, titre, age, email, tel, salaire FROM employer WHERE id = %s"
                cur.execute(query, (employe_id,))
                employee_data = cur.fetchone()

                if employee_data is None:
                    # ID not found, display error message
                    messagebox.showerror("Error", "ID non trouvé dans la base de données!")

                else:
                    # Fill the form fields with employee data
                    nom = employee_data[0]
                    prenom = employee_data[1]
                    titre = employee_data[2]
                    age = employee_data[3]
                    email = employee_data[4]
                    tel = employee_data[5]
                    salaire = employee_data[6]

                    first_name_entry.delete(0, 'end')
                    last_name_entry.delete(0, 'end')
                    spec_entry.delete(0, 'end')
                    email_entry.delete(0, 'end')
                    sal_entry.delete(0, 'end')
                    tel_entry.delete(0, 'end')
                    age_spinbox.delete(0, 'end')

                    first_name_entry.insert(0, nom)
                    last_name_entry.insert(0, prenom)
                    spec_entry.insert(0, titre)
                    email_entry.insert(0, email)
                    sal_entry.insert(0, salaire)
                    tel_entry.insert(0, tel)
                    age_spinbox.insert(0, age)

            # Function to save the updated data to the database
            def save_data():
                # Get the values from the form fields
                nom = first_name_entry.get()
                prenom = last_name_entry.get()
                titre = spec_entry.get()
                email = email_entry.get()
                tel = tel_entry.get()
                salaire = sal_entry.get()
                age = age_spinbox.get()
                id = id_entry.get()

                reqqq = "UPDATE employer SET Nomemployer = %s, prenom = %s, titre = %s, age = %s, email = %s, tel = %s, salaire = %s WHERE ID = %s"
                listeup = (nom, prenom, titre, age, email, tel, salaire, id)
                cur.execute(reqqq, listeup)
                db.commit()
                
                # Close the database connection
                cur.close()
                db.close()

                # Display a success message
                messagebox.showinfo("Success", "Les données ont été sauvegardées avec succès!")


                # Clear the form fields after saving
                clear_data()

            # Create the main window
          

            # Create the frame
            form_frame = Frame(main_frame)
            form_frame.pack(fill=BOTH, expand=True)

            # Create the LabelFrame for the form
            frame3 = LabelFrame(form_frame, text="Modifier", font=('arial', 20, 'bold'), bd=20, relief='ridge', bg='sky blue', fg='black')
            frame3.place(x=-10, y=2)

            # Create the form labels
            first_name_label = Label(frame3, text="Nom employé", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            first_name_label.grid(row=0, column=0, padx=20, pady=10)

            last_name_label = Label(frame3, text="Prénom employé", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            last_name_label.grid(row=1, column=0, padx=20, pady=10)

            spec_label = Label(frame3, text="Spécialité", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            spec_label.grid(row=2, column=0, padx=20, pady=10)

            email_label = Label(frame3, text="Email", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            email_label.grid(row=3, column=0, padx=20, pady=10)

            tel_label = Label(frame3, text="Téléphone", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            tel_label.grid(row=4, column=0, padx=20, pady=10)

            sal_label = Label(frame3, text="Salaire", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            sal_label.grid(row=5, column=0, padx=20, pady=10)

            age_label = Label(frame3, text="Age", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            age_label.grid(row=6, column=0, padx=20, pady=10)

            # Create the form input fields
            first_name_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            first_name_entry.grid(row=0, column=1, pady=10)

            last_name_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            last_name_entry.grid(row=1, column=1, pady=10)

            spec_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            spec_entry.grid(row=2, column=1, pady=10)

            email_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            email_entry.grid(row=3, column=1, pady=10)

            tel_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            tel_entry.grid(row=4, column=1, pady=10)

            tel_entry.insert(0, "+213")

            sal_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            sal_entry.grid(row=5, column=1, pady=10)

            age_spinbox = Spinbox(frame3, from_=18, to=65, width=5, font=('arial', 14, 'bold'))
            age_spinbox.grid(row=6, column=1, pady=10)

            # Create the ID label and entry for employee search


            add_button = Button(frame3, text='Sauvegarder', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=save_data)
            add_button.grid(row=8, column=0, pady=10)

            # Create the Clear button
            clear_button = Button(frame3, text='Effacer', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=clear_data)
            clear_button.grid(row=8, column=2, pady=10)

            id_label = Label(frame3, text="ID employé", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
            id_label.grid(row=0, column=2, padx=20, pady=10)

            id_entry = Entry(frame3, font=('arial', 14, 'bold'), bd=7, relief='sunken')
            id_entry.grid(row=1, column=2, pady=10)

            # Create the Search and Save buttons
            search_button = Button(frame3, text='Rechercher', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=prefill_form)
            search_button.grid(row=2, column=2, pady=10)

            frame3.pack(fill=BOTH, expand=True)



 
          
            mod_frame.pack(pady=20)


        def retardataire():
            ret_frame = tk.Frame(main_frame)
            lb = tk.Label(ret_frame,text='',font=('Bold',15))
            lb.pack()

            ret_frame.pack(pady=20)

        def les_abssences():
            abs_frame = tk.Frame(main_frame)
            lb = tk.Label(abs_frame,text='',font=('Bold',15))
            lb.pack()

            abs_frame.pack(pady=20)

        def  hide_indicator():
            list_indic.config(bg='#c3c3c3')
            mod_indic.config(bg='#c3c3c3')
            retard_indic.config(bg='#c3c3c3')
            absence_indic.config(bg='#c3c3c3')
            modifier_indic.config(bg='#c3c3c3')


        def supprimerp():
            for frame in main_frame.winfo_children():
                frame.destroy()


        def indicate(lb, page ):
            hide_indicator()
            lb.config(bg='#158aff')
            supprimerp()
            page()



        option_frame = tk.Frame(r,bg='#c3c3c3')

        list_btn = tk.Button(option_frame, text='afficher la liste',font=('Bold',15),fg='#158aff',bd=0,bg='#c3c3c3', command=lambda: indicate(list_indic,liste))
        list_btn.place(x=10, y=100)

        list_indic = tk.Label(option_frame,text='',bg='#c3c3c3')
        list_indic.place(x=3, y=100, width=5, height=40)

        mod_btn = tk.Button(option_frame, text='ajout/supp',font=('Bold',15),fg='#158aff',bd=0,bg='#c3c3c3', command=lambda: (indicate(mod_indic,ajou),face()))
        mod_btn.place(x=10, y=200)

        mod_indic = tk.Label(option_frame,text='',bg='#c3c3c3')
        mod_indic.place(x=3, y=200, width=5, height=40)


        modifier_btn = tk.Button(option_frame, text='modifier',font=('Bold',15),fg='#158aff',bd=0,bg='#c3c3c3', command=lambda: (indicate(modifier_indic,mod)))
        modifier_btn.place(x=10, y=300)

        modifier_indic = tk.Label(option_frame,text='',bg='#c3c3c3')
        modifier_indic.place(x=3, y=300, width=5, height=40)

        retard_btn = tk.Button(option_frame, text='afficher retard',font=('Bold',15),fg='#158aff',bd=0,bg='#c3c3c3',command=lambda: (indicate(retard_indic,retardataire),rotard()))
        retard_btn.place(x=10, y=400)

        retard_indic = tk.Label(option_frame,text='',bg='#c3c3c3')
        retard_indic.place(x=3, y=400, width=5, height=40)


        absence_btn = tk.Button(option_frame, text='afficher absence',font=('Bold',15),fg='#158aff',bd=0,bg='#c3c3c3',command=lambda: (indicate(absence_indic,les_abssences),mois()))
        absence_btn.place(x=10, y=500)

        absence_indic = tk.Label(option_frame,text='',bg='#c3c3c3')
        absence_indic.place(x=3, y=500, width=5, height=40)


        option_frame.pack(side=tk.LEFT)
        option_frame.pack_propagate(False)
        option_frame.configure(width=150, height=500)

        main_frame = tk.Frame(r, highlightbackground='black',highlightthickness=2)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="anis1234",
            database="firstp"
        )

        conn = db.cursor()
        conn.execute("SELECT * FROM employer ORDER BY id")
        rows = conn.fetchall()

        tree = ttk.Treeview(main_frame)
        tree['show'] = 'headings'

        s = ttk.Style(main_frame)
        s.theme_use("clam")
        s.configure(".", font=('Helvetica', 11))
        s.configure("Treeview.Heading", foreground='#57a1f8', font=('Helvetica', 11, "bold"))

    # Define number of columns
        tree["columns"] = ("id", "nom", "prenom", "titre", "age")

    # Assign the width, minwidth, and anchor to the respective columns
        tree.column("id", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("nom", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("prenom", width=150, minwidth=100, anchor=tk.CENTER)
        tree.column("titre", width=150, minwidth=150, anchor=tk.CENTER)
        tree.column("age", width=150, minwidth=150, anchor=tk.CENTER)

    # Assign the heading names to the respective columns
        tree.heading("id", text="Id", anchor=tk.CENTER)
        tree.heading("nom", text="Nom", anchor=tk.CENTER)
        tree.heading("prenom", text="Prénom", anchor=tk.CENTER)
        tree.heading("titre", text="Spécialitée", anchor=tk.CENTER)
        tree.heading("age", text="Age", anchor=tk.CENTER)
        t = 1
        for row in rows:
                if t % 2 == 0:
                    tree.insert('', "end", text="", values=row, tags=("even",), iid=row[0])
                else:
                    tree.insert('', "end", text="", values=row, tags=("odd",), iid=row[0])
                t += 1

        tree.tag_configure("even", foreground='#57a1f8', background="black")
        tree.tag_configure("odd", foreground="black", background='#57a1f8')
        def get_selected_item(event):
                selected_item = tree.selection()[0]
                item_id = selected_item
                print("ID sélectionné :", item_id)

    # Lier la fonction à l'événement de sélection d'une ligne
        tree.bind("<<TreeviewSelect>>", get_selected_item)

    # Afficher le Treeview
        tree.pack()

        hsb = ttk.Scrollbar(main_frame, orient="horizontal")
        hsb.configure(command=tree.xview)
        tree.configure(xscrollcommand=hsb.set)
        hsb.pack(fill=tk.X, side=tk.BOTTOM)

        vsb = ttk.Scrollbar(main_frame, orient="vertical")
        vsb.configure(command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(fill=tk.Y, side=tk.RIGHT)

        
        



            
        
        main_frame.pack(side=tk.LEFT)
        main_frame.pack_propagate(False)
        main_frame.configure(width=774, height=500)
                


    elif username!='admin'and password!='aaaa':
        messagebox.showerror("invalid","invalid nom d'utilisateur and mot de passe")

    elif  password!='':
        messagebox.showerror("invalid","mot de passe incorrecte")

    elif username!='':
        messagebox.showerror("invalid","nom d'utilisateur incorrecte")        



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
    salaire =  sal_entry.get()

    # Save the image path in the database
    label = nom.replace(" ", "-").lower()
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
    os.makedirs(os.path.join(image_dir, label), exist_ok=True)
    image_path = os.path.join(image_dir, label, f"{x}.png")

    query = "INSERT INTO employer (Nomemployer, photoemployer, prenom, titre,salaire , age, email,tel ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (label, image_path, prenom, titre, salaire, age, email, tel )

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
        messagebox.showinfo("Success", "Données ajoutées")
    except Error as error:
        messagebox.showerror("Error", f"Echec d'ajout des données: {error}")
    finally:
        if db.is_connected():
            cur.close()
            db.close()

 def delete_data():
    frame2 = LabelFrame(boot, text="Supression", font=('arial', 20, 'bold'), bd=20, relief='ridge', bg='sky blue', fg='black')
    frame2.place(x=100, y=20)
 
    # Labels
    nom_label = Label(frame2, text="Nom employer", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
    nom_label.grid(row=0, column=0, padx=20, pady=10)

    prenom_label = Label(frame2, text="Prénom employer", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
    prenom_label.grid(row=1, column=0, padx=20, pady=10)
    

    nom_entry = Entry(frame2, font=('arial', 14, 'bold'), bd=7, relief='sunken')
    nom_entry.grid(row=0, column=1, pady=10)
    prenom_entry = Entry(frame2, font=('arial', 14, 'bold'), bd=7, relief='sunken')
    prenom_entry.grid(row=1, column=1, pady=10)
    

    def supp():
        nom = nom_entry.get()
        prenom = prenom_entry.get()

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="anis1234",
                database='firstp'
            )
            cur = db.cursor()
            print(nom)
            print(prenom)
            q="SELECT id FROM employer WHERE Nomemployer= %s AND prenom = %s"
            query = "DELETE FROM employer WHERE Nomemployer = %s AND prenom = %s"
            values = (nom, prenom)
            
            # Execute the delete query with the provided values
            cur.execute(q, values)
            d = cur.fetchone()
            print(d)
            if d!=None:
                dd=d[0]
                print(dd)
                list = values
                list=list+(dd,)
                print(list)
                qq="INSERT INTO archive ( nom, prenom,id) VALUES (%s,%s,%s)"     
                cur.execute(qq, list)
                db.commit()
                cur.execute(query, values)
                db.commit()

                # Remove the specific employee's directory based on their name
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                image_dir = os.path.join(BASE_DIR, "images", nom.lower().replace(" ", "-"))
                print(image_dir)
                shutil.rmtree(image_dir)
                
                # Show a success message
                messagebox.showinfo("Success", "suppression reussit")
            else:   
                messagebox.showerror("Error", "Entrer un employée deja existant") 
        except mysql.connector.Error as error:
            # Show an error message if the deletion fails
            messagebox.showerror("Erreur", f"Echec de suppression des données : {error}")
        finally:
            if db.is_connected():
                cur.close()
                db.close()

        # Close frame2 after successful deletion
        frame2.destroy()

    supp_button = Button(frame2, text='Supprimer', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=supp)
    supp_button.grid(row=2, column=0, padx=20, pady=10)

    def close_frame2():
        frame2.destroy()  # Destroy the frame2 widget

    cancel_button = Button(frame2, text='Annuler', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=close_frame2)
    cancel_button.grid(row=2, column=1, padx=20, pady=10)

 def start_face_detection():
    global x
    nom = first_name_entry.get()
    label = nom.replace(" ", "-").lower()
    pathh = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", label)
    os.makedirs(pathh, exist_ok=True)

    while True:
        ret, img = cap.read()
        if not ret:
            print("Erreur : la camera ne s'allume pas.")
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
        
 frame1 = LabelFrame(boot, text="Enregistrer", font=('arial', 20, 'bold'), bd=20, relief='ridge', bg='sky blue', fg='black')
 frame1.place(x=200, y=2)

 first_name_label = Label(frame1, text="Nom employé", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 first_name_label.grid(row=0, column=0, padx=20, pady=10)

 last_name_label = Label(frame1, text="Prénom employé", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 last_name_label.grid(row=1, column=0, padx=20, pady=10)

 spec_label = Label(frame1, text="Spécialité", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 spec_label.grid(row=2, column=0, padx=20, pady=10)

 email_label = Label(frame1, text="Email", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 email_label.grid(row=3, column=0, padx=20, pady=10)

 tel_label = Label(frame1, text="Téléphone", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 tel_label.grid(row=4, column=0, padx=20, pady=10)

 sal_label = Label(frame1, text="Salaire", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 sal_label.grid(row=5, column=0, padx=20, pady=10)

 age_label = Label(frame1, text="Age", font=('arial', 14, 'bold'), bg='sky blue', fg='black')
 age_label.grid(row=6, column=0, padx=20, pady=10)

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

 sal_entry = Entry(frame1, font=('arial', 14, 'bold'), bd=7, relief='sunken')
 sal_entry.grid(row=5, column=1, pady=10)


 age_spinbox = Spinbox(frame1, from_=18, to=65, width=5, font=('arial', 14, 'bold'))
 age_spinbox.grid(row=6, column=1, pady=10)

 def clear_data():
    # Function to clear all the data
    first_name_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    spec_entry.delete(0, 'end')
    email_entry.delete(0, 'end')
    sal_entry.dele(0, 'end')
    tel_entry.delete(+213, 'end')
    

 refresh_icon = "\u21BA"

# Create a custom font for the refresh icon
 refresh_font = tkFont.Font(family="Arial", size=14, weight="bold")

# Create the Refresh button with the refresh icon
 refrech_button = Button(frame1, text=refresh_icon, width=10, font=refresh_font, bd=4, relief='raised', bg='white', fg='black', command=clear_data)
 refrech_button.grid(row=7, column=1, pady=10)
 add_button = Button(frame1, text='Ajouter', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=start_face_detection_and_add_data)
 add_button.grid(row=7, column=0, pady=10)
 delete_button = Button(frame1, text='Supprimer', width=10, font=('arial', 14, 'bold'), bd=4, relief='raised', bg='white', fg='black', command=delete_data)
 delete_button.grid(row=7, column=2, pady=10)


 

 db.close()


image_icon=PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
root.iconphoto(False,image_icon)
img = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
Label(root,image=img,bg='white').place(x=50,y=50)

frame=Frame(root,width=350,height=350,bg="white")
frame.place(x=480, y=70)

heading=Label(frame,text='CamPoint',fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)
###-----------------------------------

def on_entry_click(event):
    if user.get() == 'Nom Utilisateur':
        user.delete(0, END)
        user.configure(fg='black')

def on_exit(event):
    if user.get() == '':
        user.insert(0, 'Nom Utilisateur')
        user.configure(fg='gray')

user = Entry(frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Nom Utilisateur')
user.bind('<FocusIn>', on_entry_click)
user.bind('<FocusOut>', on_exit)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_password_entry_click(event):
    if code.get() == 'mot de passe':
        code.delete(0, END)
        code.configure(show='*', fg='black')

def on_password_exit(event):
    if code.get() == '':
        code.insert(0, 'mot de passe')
        code.configure(show='', fg='gray')

code = Entry(frame, width=25, fg='gray', border=0, bg='white', show='', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'mot de passe')
code.bind('<FocusIn>', on_password_entry_click)
code.bind('<FocusOut>', on_password_exit)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

##-------------------------------------

Button(frame,width=39,pady=7,text='Confirmer',bg='#57a1f8',fg='white',border=0, command=signin).place(x=35,y=204)


root.mainloop()


