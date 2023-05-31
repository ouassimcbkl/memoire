import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import ttk

# Creating a Tkinter window
noot = tk.Tk()
noot.title('absence')
noot.geometry('925x500+200+100')
noot.configure(bg="#fff")
noot.resizable(False, False)

# Creating a frame to hold the treeview and scrollbar
frame = tk.Frame(noot, width=900, height=400)  # Adjust the dimensions as desired
frame.pack(padx=10, pady=10)

# Creating a scrollbar
scrollbar = ttk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Creating a Treeview widget
treeview = ttk.Treeview(frame, yscrollcommand=scrollbar.set)
treeview.pack(fill=tk.BOTH, expand=True)  # Fill the entire frame with the treeview

# Configuring the scrollbar to scroll the treeview
scrollbar.config(command=treeview.yview)

# Connecting to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="anis1234",
    database='firstp'
)
cur = db.cursor()

# Getting the current date and formatting it
now = datetime.now()
S = now.strftime('%Y-%m-%d')
SS = S.split()

# Executing a SELECT query to retrieve employees' names who have no entry for the specific date
req2 = "SELECT Nomemployer FROM employer WHERE NOT EXISTS (SELECT * FROM entrer WHERE entrer.idemp = employer.id AND date = %s)"
cur.execute(req2, SS)
absent_employees = cur.fetchall()

# Inserting names into the treeview
for employee in absent_employees:
    treeview.insert('', 'end', text=employee[0])

# Running the Tkinter event loop
noot.mainloop()
