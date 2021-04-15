import tkinter
from tkinter import *
from tkinter import messagebox
game = Tk()
game.title("Game Creator")
# game.minsize(640, 480)
# game.maxsize(1280, 720)
# game.geometry("1980x1080")
# game.resizable(width=False, height=True)
# game.positionfrom("user")
# game.positionfrom("user")
# game.geometry("480x480+120+120")


# How to center the screen
screen_x = game.winfo_screenwidth()
screen_y = game.winfo_screenheight()
window_x = 1200
window_y = 800

pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)

game.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# How to create a widget

label_welcome = tkinter.Label(game, text="Welcome")


# How to access the parameter of a widget

print(label_welcome["text"])
print(label_welcome.cget("text"))

# How to change label parameters

label_welcome.config(text="Goodbye")
label_welcome.pack()

# How to cut a message on multiple lines in a label

message_label = tkinter.Message(game, text="Hello everyone and welcome to die")
message_label.pack()

# Widget to enter stuff

entry_name = tkinter.Entry(game)
entry_name.pack()
password = tkinter.Entry(game, show="*")
password.pack()
# add exportselection=0 in second parameter to avoid stuff being copied to clipboard

# Widget to create a button


def stars():
    for x in range(10, 1, -1):
        print(x * " ", "*")


button_1 = tkinter.Button(game, text="Button 1", width=10, height=10, command=stars)
button_1.pack()

# Widget to check button

check_widget = tkinter.Checkbutton(game, text="Publish game?", offvalue=2, onvalue=5)
check_widget.pack()

# Widget : if one is turned on, the other is turned off

radio_widget_man = tkinter.Radiobutton(game, text="Man", value=1)
radio_widget_man.pack()
radio_widget_woman = tkinter.Radiobutton(game, text="Female", value=0)
radio_widget_woman.pack()

# Widget for cursors

scale_w = tkinter.Scale(game, from_=10, to_=100)
scale_w.pack()
# add tickinterval=<int> in parameters for a tick interval


# Widget for an incrementing box

spin_w = tkinter.Spinbox(game, from_=1, to_=10)
spin_w.pack()

# Widget for a box with a list with different clickable elements

lb = tkinter.Listbox(game)
lb.insert(1, "First")
lb.insert(2, "Second")
lb.insert(3, "Third")
lb.pack()

# Widget for alert messages
# IMPORTANT -> from tkinter import messagebox


def show_error_window():
    messagebox.showerror("Error", "There's a problem")


button_2 = tkinter.Button(game, text="Shows error", command=show_error_window)
button_2.pack()

# Widget to show info message


def show_info_window():
    messagebox.showinfo("Info", "Insert information here")


button_3 = tkinter.Button(game, text="Info Button", command=show_info_window)
button_3.pack()

# Widget to show info message


def show_warning():
    messagebox.showwarning("Warning", "Insert warning here")


button_4 = tkinter.Button(game, text="Warning Button", command=show_warning)
button_4.pack()

# Widget to ask a yes or no question


def ask_question():
    messagebox.askquestion("Question", "Yes or no my nigga")


button_5 = tkinter.Button(game, text="Question button", command=ask_question)
button_5.pack()

# More widgets for windows
# askokcancel
# askyesno
# askretrycancel


game.mainloop()

