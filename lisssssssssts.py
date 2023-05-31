import mysql.connector
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as mb

r = tk.Tk()
r.geometry("925x500+200+100")
r.title("user details")

connect = mysql.connector.connect(host="localhost",
    user="root",
    password="anis1234",
    database="firstp")

conn = connect.cursor()

conn.execute("SELECT * FROM employer ORDER BY id")

tree=ttk.Treeview(r)
tree['show'] = 'headings'

s = ttk.Style(r)
s.theme_use("clam")
s.configure(".", font=('Helvetica', 11))
s.configure("Treeview.Heading", foreground='red',font=('Helvetica', 11,"bold"))

# Define number of columns
tree["columns"]=("id","nom","prenom","age","titre")

#Assign the width,minwidth and anchor to the respective columns
tree.column("id", width=50, minwidth=50,anchor=tk.CENTER)
tree.column("nom", width=100, minwidth=100,anchor=tk.CENTER)
tree.column("prenom", width=50, minwidth=50,anchor=tk.CENTER)

tree.column("age", width=150, minwidth=150,anchor=tk.CENTER)
tree.column("titre", width=150, minwidth=150,anchor=tk.CENTER)

#Assign the heading names to the respective columns
tree.heading("id", text="Id",anchor=tk.CENTER)
tree.heading("nom", text=" nom",anchor=tk.CENTER)
tree.heading("prenom", text="prenom",anchor=tk.CENTER)

tree.heading("age", text="age",anchor=tk.CENTER)
tree.heading("titre", text="specialitee",anchor=tk.CENTER)

i = 0
for ro in conn:
    if ro[0]%2==0:
        tree.insert('', i, text="",values=(ro[0],ro[1],ro[2],ro[3],ro[4]),tags=("even",))
    else:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4]), tags=("odd",))
    i = i + 1

tree.tag_configure("even",foreground="black",background="white")
tree.tag_configure("odd",foreground="white",background="black")

hsb = ttk.Scrollbar(r,orient="horizontal")
hsb.configure(command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(fill=X,side = BOTTOM)

vsb = ttk.Scrollbar(r,orient="vertical")
vsb.configure(command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(fill=Y,side = RIGHT)

tree.pack()
nom=tk.StringVar()
prenom=tk.StringVar()

age=tk.StringVar()
titre=tk.IntVar()

def add_data(tree):
    f = Frame(r,width=400,height=320,background="grey")
    f.place(x=100,y=250)
    l1=Label(f,text="nom",width=8,font=('Times',11,'bold'))
    e1=Entry(f,textvariable=nom,width=25)
    l1.place(x=50,y=30)
    e1.place(x=170,y=30)

    l2 = Label(f, text="prenom", width=8, font=('Times', 11, 'bold'))
    e2 = Entry(f, textvariable=prenom, width=25)
    l2.place(x=50, y=70)
    e2.place(x=170, y=70)

    l3 = Label(f, text="age", width=8, font=('Times', 11, 'bold'))
    l3.place(x=50, y=110)
    e3 = Entry(f, textvariable=age, width=25)
    e3.place(x=170, y=110)

    l4 = Label(f, text="titre", width=8, font=('Times', 11, 'bold'))
    l4.place(x=50, y=150)
    e4 = Entry(f, textvariable=titre, width=25)
    e4.place(x=170, y=150)

    
    def insert_data():
        nonlocal e1,e2,e3,e4
        s_name=nom.get()
        g = prenom.get()
        
        e = age.get()
        p = titre.get()
        
        conn.execute('INSERT INTO employer(nom,prenom,age,titre) VALUES(%s,%s,%s,%s)',
                     (s_name,g,e,p,))
        print(conn.lastrowid)
        connect.commit()
        tree.insert('','end',text="",values=(conn.lastrowid,s_name,g,e,p))
        mb.showinfo("Success","employee registered")
        e1.delete(0,END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        
        f.destroy()

    submitbutton = tk.Button(f, text="submit", command=insert_data)
    submitbutton.configure(font=('Times', 11, 'bold'), bg='green', fg='white')
    submitbutton.place(x=100, y=280)
    cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
    cancelbutton.configure(font=('Times', 11, 'bold'), bg='red', fg='white')
    cancelbutton.place(x=240, y=280)

def delete_data(tree):
    selected_item=tree.selection()[0]
    print(tree.item(selected_item)['values'])
    uid=tree.item(selected_item)['values'][0]
    del_query="DELETE FROM employer WHERE id=%s"
    sel_data=(uid,)
    conn.execute(del_query,sel_data)
    connect.commit()
    tree.delete(selected_item)
    mb.showinfo("success","employee data deleted ")

def select_data(tree):
    curItem=tree.focus()
    values= tree.item(curItem,"values")
    print(values)
    f = Frame(r, width=400, height=320, background="grey")
    f.place(x=100, y=250)
    l1 = Label(f, text="nom", width=8, font=('Times', 11, 'bold'))
    e1 = Entry(f, textvariable=nom, width=25)
    l1.place(x=50, y=30)
    e1.place(x=170, y=30)

    l2 = Label(f, text="prenom", width=8, font=('Times', 11, 'bold'))
    e2 = Entry(f, textvariable=prenom, width=25)
    l2.place(x=50, y=70)
    e2.place(x=170, y=70)

    

    l4 = Label(f, text="age", width=8, font=('Times', 11, 'bold'))
    l4.place(x=50, y=150)
    e4 = Entry(f, textvariable=age, width=25)
    e4.place(x=170, y=150)

    l5 = Label(f, text="titre", width=8, font=('Times', 11, 'bold'))
    l5.place(x=50, y=190)
    e5 = Entry(f, textvariable=titre, width=25)
    e5.place(x=170, y=190)
    e5.delete(0, END)

    e1.insert(0,values[1])
    e2.insert(0, values[2])
    
    e4.insert(0,values[4])
    e5.insert(0, values[5])
    
    def update_data():
        nonlocal e1,e2,e4,e5,curItem,values
        s_name = nom.get()
        g = prenom.get()
        
        e = age.get()
        p = titre.get()
        
        tree.item(curItem,values=(values[0],s_name,g,e,p))
        conn.execute(
            "UPDATE employer SET nom=%s, prenom=%s, age=%s, titre=%s WHERE id=%s"
            , (s_name, g, e, int(p), values[0]))
        connect.commit()
        mb.showinfo("success","employee data updated")
        e1.delete(0,END)
        e2.delete(0, END)
    
        e4.delete(0, END)
        e5.delete(0, END)
        
        f.destroy()

    savebutton = tk.Button(f, text="Update", command=update_data)
    savebutton.place(x=100, y=270)
    cancelbutton = tk.Button(f, text="cancel", command=f.destroy)
    cancelbutton.place(x=200, y=270)

insertbutton = tk.Button(r,text="Insert",command=lambda:add_data(tree))
insertbutton.configure(font =('calibri', 14, 'bold'), bg = 'green',fg='white')
insertbutton.place(x=200,y=260)

deletebutton = tk.Button(r,text="delete",command=lambda:delete_data(tree))
deletebutton.configure(font =('calibri', 14, 'bold'), bg = 'red',fg='white')
deletebutton.place(x=300,y=260)

updatebutton = tk.Button(r,text="update",command=lambda:select_data(tree))
updatebutton.configure(font =('calibri', 14, 'bold'), bg = 'blue',fg='white')
updatebutton.place(x=400,y=260)

r.mainloop()



