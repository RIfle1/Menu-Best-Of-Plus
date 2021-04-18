import tkinter
from tkinter import messagebox
from tkinter import *
import tkinter.font as font

UI = tkinter.Tk()
# set window size
UI.geometry("1200x800")
# define font size
myFont = font.Font(size=20)

#When "delete this character" is pressed
def action():
    result = messagebox.askquestion(title="Not so fast", message="You're about to delete this character. Are you sure do you want to continue ?", icon="warning")
    if result == 'yes':
        Character_name.place_forget()
        Character_name_box.place_forget()
        Breed.place_forget()
        Breed_box.place_forget()
        Health.place_forget()
        Health_box.place_forget()
        Speed.place_forget()
        Speed_box.place_forget()
        Attack.place_forget()
        Attack_box.place_forget()
        Defense.place_forget()
        Defense_box.place_forget()
        Background.place_forget()
        Background_box.place_forget()
        btn["state"] = "normal"
        btn["bg"] = "#4285F4"
        btn2["state"] = "disabled"
        btn2["bg"] = "#C4C4C4"
    else:
        print(" ")


#When "new character" is pressed
def btn():
    btn["state"] = "disabled"
    btn["bg"] = "#C4C4C4"
    btn2["state"] = "normal"
    btn2["bg"] = "#E86351"
    Character_name.place(x=25, y=150)
    Character_name_box.place(x=325, y=150)
    Breed.place(x=25, y=200)
    Breed_box.place(x=325, y=200)
    Health.place(x=25, y=250)
    Health_box.place(x=325, y=250)
    Speed.place(x=25, y=300)
    Speed_box.place(x=325, y=300)
    Attack.place(x=25, y=350)
    Attack_box.place(x=325, y=350)
    Defense.place(x=25, y=350)
    Defense_box.place(x=325, y=350)
    Background.place(x=25, y=400)
    Background_box.place(x=325, y=400)

#apparence du bouton new character
btn = tkinter.Button(UI, text="New Character", bd=0, bg="#3285F4", fg="White", padx=30, pady=10, font="Montserrat", relief=FLAT, command=btn)
btn['font'] = myFont
btn.place(x=25, y=25)

#apparence du bouton delete
btn2 = tkinter.Button(UI, text="Delete this character", bd=0, bg="#C4C4C4", fg="White", padx=30, pady=10, font="Montserrat", relief=FLAT, state=DISABLED, command=action)
btn2['font'] = myFont
btn2.place(x=325, y=25)


# First text with text box
Character_name = Label(UI, text="Character name", font=("Montserat", 14), fg="#323232")
Character_name.place_forget()

Character_name_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Character_name_box.place_forget()

# Second text with text box
Breed = Label(UI, text="Breed", font=("Montserat", 14), fg="#323232")
Breed.place_forget()

Breed_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Breed_box.place_forget()

# Third text with text box
Health = Label(UI, text="Health", font=("Montserat", 14), fg="#323232")
Health.place_forget()

Health_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Health_box.place_forget()

# 4th text with text box
Speed = Label(UI, text="Speed", font=("Montserat", 14), fg="#323232")
Speed.place_forget()

Speed_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Speed_box.place_forget()

# 5th text with text box
Attack = Label(UI, text="Attack", font=("Montserat", 14), fg="#323232")
Attack.place_forget()

Attack_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Attack_box.place_forget()

# 6th text with text box
Defense = Label(UI, text="Defense", font=("Montserat", 14), fg="#323232")
Defense.place_forget()

Defense_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Defense_box.place_forget()

# 7th text with text box
Background = Label(UI, text="Background", font=("Montserat", 14), fg="#323232")
Background.place_forget()

Background_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Background_box.place_forget()


UI.mainloop()
