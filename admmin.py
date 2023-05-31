from tkinter import *
from tkinter import messagebox
from datetime import date
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk
import mysql.connector
import tkinter
from PIL import Image, ImageTk
import os
import cv2
from tkinter.ttk import Combobox

import pathlib
import sqlite3 

root = Tk()
root.title('login')
root.geometry('925x500+200+100')
root.configure(bg="#fff")
# root.state('zoomed')
root.resizable(False, False)

# Function to display the next page content
def show_next_page():
    login_frame.pack_forget()  # Hide the login frame

    next_page_frame = Frame(root, bg="white")  # Create a new frame for the next page content
    next_page_frame.pack(pady=50)

    label = Label(next_page_frame, text="Welcome to the Next Page!", font=('Arial', 24, 'bold'), bg='white', fg='black')
    label.pack()

    # Add the content for the next page here


def signin():
    username = user.get()
    password = code.get()

    if username == 'admin' and password == 'aaaa':
        show_next_page()
    else:
        messagebox.showerror("Invalid", "Invalid username or password")


image_icon=PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
root.iconphoto(False,image_icon)

img = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
Label(root,image=img,bg='white').place(x=50,y=50)

login_frame = Frame(root, width=350, height=350, bg="white")
login_frame.place(x=480, y=70)

heading = Label(login_frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

def on_entry_click(event):
    if user.get() == 'Username':
        user.delete(0, END)
        user.configure(fg='black')

def on_exit(event):
    if user.get() == '':
        user.insert(0, 'Username')
        user.configure(fg='gray')

user = Entry(login_frame, width=25, fg='gray', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_entry_click)
user.bind('<FocusOut>', on_exit)
Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_password_entry_click(event):
    if code.get() == 'Password':
        code.delete(0, END)
        code.configure(show='*', fg='black')

def on_password_exit(event):
    if code.get() == '':
        code.insert(0, 'Password')
        code.configure(show='', fg='gray')

code = Entry(login_frame, width=25, fg='gray', border=0, bg='white', show='', font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_password_entry_click)
code.bind('<FocusOut>', on_password_exit)
Frame(login_frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(login_frame, text='Sign In', font=('Arial', 13, 'bold'), fg='white', bg='#57a1f8', activeforeground='white', activebackground='#57a1f8', relief=GROOVE, command=signin).place(x=115, y=220)

root.mainloop()
