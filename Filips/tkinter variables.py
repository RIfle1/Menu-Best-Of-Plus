import tkinter
from tkinter import *
# Necessary components for an interface
app = Tk()
app.title("Tkinter Variables")
screen_x = app.winfo_screenwidth()
screen_y = app.winfo_screenheight()
window_x = 1200
window_y = 800
pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)
app.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# StringVar() : str
# IntVar() : int
# DoubleVar() : float
# BooleanVar() : bool

# Assign a variable -> str, int, float, bool
var_label = tkinter.StringVar()

# Create the label, button or whatever with whatever
label = tkinter.Label(app, text="", textvariable=var_label)

# Set the variable to something to change the preferred setting
var_label.set("Hello")
label.pack()

# Use either textvariable= <> or variable = <>

# Connect another module using an observer

"""var_entry = tkinter.StringVar()
entry = tkinter.Entry(app, textvariable=var_entry)
entry.pack()"""

# Observer


def update_label(*arg):
    var_label2.set(var_entry.get())


var_entry = tkinter.StringVar()
# Use .trace("w or u or r", ,function) to trace and change in real time

var_entry.trace("w", update_label)
entry = tkinter.Entry(app, textvariable=var_entry)
entry.pack()

var_label2 = tkinter.StringVar()
label2 = tkinter.Label(app, textvariable=var_label2)
label2.pack()

app.mainloop()
