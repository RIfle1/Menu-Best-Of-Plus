import tkinter
from tkinter import *

app = Tk()
app.title("Tkinter Variables")
screen_x = app.winfo_screenwidth()
screen_y = app.winfo_screenheight()
window_x = 1200
window_y = 800
pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)
app.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")


def gender_observer(*args):
    if var_gender.get():
        var_gender_label.set("It's a Male")
    else:
        var_gender_label.set("It's a Female")


var_gender = tkinter.IntVar()
var_gender.trace("w", gender_observer)

radio1 = tkinter.Radiobutton(app, text="Male", value=1, variable=var_gender)
radio1.pack()
radio2 = tkinter.Radiobutton(app, text="Female", value=0, variable=var_gender)
radio2.pack()


var_gender_label = tkinter.StringVar()
gender_label = tkinter.Label(app, textvariable=var_gender_label)
var_gender_label.trace("w", gender_observer)
gender_label.pack()

app.mainloop()
