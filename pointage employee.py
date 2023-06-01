from tkinter import*
from tkinter import messagebox
from PIL import ImageTk, Image
import cv2
from datetime import datetime
import tkinter as tk
import mysql.connector
from datetime import datetime

db = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "anis1234",
  database='firstp'
)

cur = db.cursor()
def resize_image(event):
    # Get the current size of the label
    width = event.width
    height = event.height

    # Resize the image to fit the label size
    resized_image = bg.resize((width, height))

    # Update the image displayed in the label
    my_label.config(image=resized_image)
    my_label.image = resized_image  # Keep a reference to prevent image from being garbage collected
 
def function():
    now = datetime.now()
    date=now.strftime('%Y-%m-%d')
    heure=now.strftime('%H:%M:%S')
    if now.hour <=12 and now.hour >=8:
      exec(open("./Face_recognition_entrerh.py").read())
    else:
       if now.hour <=16 and now.hour >=12:
          exec(open("./Face_recognition_sortieh.py").read())
          
window = Tk()
window.title('accueil')
window.geometry("925x500+200+100")
window.configure(background='gray')
window.resizable(False, False)

image_icon = PhotoImage(file="C:\\Users\\Anis_\\OneDrive\\Bureau\\login.png")
window.iconphoto(False,image_icon)

pic = Image.open("C:\\Users\\Anis_\\Downloads\\Desktop - 4.png")
resized = pic.resize((925,500),Image.ANTIALIAS)

bg = ImageTk.PhotoImage(resized)
my_label = Label(window, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

b1 = Button(window, text="ouvrir camera",
          font=("TKHeadingFont",20),
          bg="#57a1f8",
          fg='white',
          cursor="hand2",
          activebackground="#badee2",
          activeforeground="black",
          anchor="center",
          command=function
          
          

         
            )

b1.grid(row=2, column=5, pady=240, padx=275)

def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
         window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
button_quit = Button(window,text="X",
          font=("TKHeadingFont",30),
          bg="#FA270F",
          fg='white',
          cursor="hand2",
          activebackground="#C6BEBD",
          activeforeground="black",
          anchor="center",
          command=lambda: [cv2.destroyAllWindows(), window.destroy()]
            )
button_quit.grid(row=0, column=0,padx=30,pady=20)
window.mainloop()

            





