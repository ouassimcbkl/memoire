from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta
from calendar import monthrange
def retard_moi():
 db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="anis1234",
  database='firstp'
 )

 doot = Tk()
 doot.title('Login')
 doot.geometry('925x500+200+100')
 doot.configure(bg="#fff")
 doot.resizable(False, False)

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

 result_label = Label(doot, text="Results:")
 result_label.pack()

 for row in nom:
    employer_name = row[0]
    entry_count = row[1]
    result_text = f"Employer: {employer_name}, Entry Count: {entry_count}"
    result_entry = Label(doot, text=result_text)
    result_entry.pack()

 doot.mainloop()
