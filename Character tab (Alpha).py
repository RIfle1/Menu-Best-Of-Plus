import tkinter
from tkinter import messagebox
from tkinter import *
import tkinter.font as font

UI = tkinter.Tk()
# set window size
UI.geometry("1000x500")
# define font
myFont = font.Font(size=20)

def action():
    messagebox.askquestion(title="Windows", message="coucou")


btn = tkinter.Button(UI, text="Button 1", bd=0, bg="#3285F4", fg="White", padx=30, pady=10, font="BritannicBold", relief=FLAT, command=action)
btn['font'] = myFont

btn2 = tkinter.Button(UI, text="Button 2", bd=0, bg="#1666DE", fg="White", padx=30, pady=10, font="ProductSans", relief=FLAT,)
btn2['font'] = myFont

btn.place(x=0, y=0)
btn2.place(x=200, y=0)
UI.mainloop()
