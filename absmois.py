import mysql.connector
from datetime import datetime, timedelta
from calendar import monthrange
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Create the Tkinter window
noot = tk.Tk()
noot.title('abssence')
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
year = today_date.year
month = today_date.month
days_in_month = monthrange(year, month)[1]
next_month = today_date - timedelta(days=days_in_month)
SSSS = next_month.strftime('%Y-%m-%d')
value = (S, SSSS)
req = "SELECT entrer.idemp, employer.Nomemployer FROM entrer INNER JOIN employer ON entrer.idemp = employer.id WHERE date = %s AND retard = 'true'"
req4 = "SELECT COUNT(*) AS absence_count FROM entrer WHERE date >= CURDATE() - INTERVAL 30 DAY AND date <= CURDATE()"
req2 = "SELECT employer.Nomemployer, COUNT(entrer.id) FROM employer LEFT JOIN entrer ON employer.id = entrer.idemp WHERE NOT EXISTS (SELECT * FROM entrer WHERE entrer.idemp = employer.id AND date <= %s AND date >= %s) GROUP BY employer.Nomemployer"
reeq = "SELECT employer.Nomemployer, COUNT(entrer.idemp) FROM employer LEFT JOIN entrer ON employer.id = entrer.idemp WHERE employer.id NOT IN (SELECT idemp FROM entrer WHERE date >= CURDATE() - INTERVAL 30 DAY AND date <= CURDATE()) GROUP BY employer.Nomemployer"
qqqq = "SELECT employer.Nomemployer, (30 - COUNT(entrer.id)) AS nombre_absences FROM employer LEFT JOIN entrer ON employer.id = entrer.idemp AND entrer.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) GROUP BY employer.id, employer.Nomemployer;"
cur.execute(qqqq)
result = cur.fetchall()

# Create a Treeview widget
tree = ttk.Treeview(noot, columns=("Name", "Absences", "Delete"), show="headings")

tree.column("Name", width=300)
tree.column("Absences", width=150)
tree.column("Delete", width=100)

tree.heading("Name", text="Name")
tree.heading("Absences", text="Absences")
tree.heading("Delete", text="Delete")

# Insert data into the Treeview
for row in result:
    tree.insert("", tk.END, values=row + ("Delete",), tags=("Delete",))

# Add horizontal scrollbar
hsb = ttk.Scrollbar(noot, orient="horizontal", command=tree.xview)
hsb.pack(fill=tk.X, side=tk.BOTTOM)
tree.configure(xscrollcommand=hsb.set)

# Add vertical scrollbar
vsb = ttk.Scrollbar(noot, orient="vertical", command=tree.yview)
vsb.pack(fill=tk.Y, side=tk.RIGHT)
tree.configure(yscrollcommand=vsb.set)

# Add delete button to each row
tree.tag_configure("Delete", foreground="blue")

# Bind double-click event to the delete_employee function
tree.tag_bind("Delete", "<Double-1>", delete_employee)

# Display the number of absences
label_count = tk.Label(noot, text="Number of absences within the last 30 days: {}".format(len(result)), font=('calibre', 14, 'bold'), bg="#fff")
label_count.pack()

# Display the Treeview widget
tree.pack(fill=tk.BOTH, expand=True)

noot.mainloop()
