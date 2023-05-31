from tkinter import *
import mysql.connector
from datetime import datetime, timedelta
from calendar import monthrange
def retard():
 reet = Tk()
 reet.title('Retard Moi')
 reet.geometry('925x500+200+100')
 reet.configure(bg="#e0eaf5")
 reet.resizable(False, False)


 def mois():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
    )

    frame = Frame(reet, bg="#e0eaf5")
    frame.pack(pady=20)

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


 def now():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="anis1234",
        database='firstp'
    )

    frame = Frame(reet, bg="#e0eaf5")
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
    req = "SELECT ALL entrer.id, entrer.idemp, employer.Nomemployer FROM entrer, employer WHERE date = %s and retard ='true' and entrer.idemp = employer.id"
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

    reet.mainloop()
# Execute both functions on the same page
 mois()
 now()
retard()
 
