import tkinter
from tkinter import messagebox
from tkinter import *
import tkinter.font as font

UI = tkinter.Tk()
# set window size
UI.geometry("1200x800")
# define font size
myFont = font.Font(size=20)

#def of save variable
player_ID = 2
done_ID = 0
player_name = ""
player1_name = "Character 1"
player2_name = "Character 2"
player3_name = "Character 3"
player4_name = "Character 4"

player_race = ""
player1_race = ""
player2_race = ""
player3_race = ""
player4_race = ""

player_life = ""
player1_life = ""
player2_life = ""
player3_life = ""
player4_life = ""

player_speed = ""
player1_speed = ""
player2_speed = ""
player3_speed = ""
player4_speed = ""

player_strength = ""
player1_strength = ""
player2_strength = ""
player3_strength = ""
player4_strength = ""

player_defense = ""
player1_defense = ""
player2_defense = ""
player3_defense = ""
player4_defense = ""

player_attack = ""
player1_attack = ""
player2_attack = ""
player3_attack = ""
player4_attack = ""

player_Background = ""
player1_Background = ""
player2_Background = ""
player3_Background = ""
player4_Background = ""


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
        btn3.place_forget()
        if player_ID >= 1:
            Ch1.place(x=25, y=175)
        else:
            Ch1.place_forget()
        if player_ID >= 2:
            Ch2.place(x=25, y=300)
        else:
            Ch2.place_forget()
        if player_ID >= 3:
            Ch3.place(x=25, y=425)
        else:
            Ch3.place_forget()
        if player_ID >= 4:
            Ch4.place(x=25, y=550)
        else:
            Ch4.place_forget()
    else:
        print(" ")


#When "create new character" is pressed
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
    btn3.place(x=1025, y=705)
    Ch4.place_forget()
    Ch3.place_forget()
    Ch2.place_forget()
    Ch1.place_forget()
    if player_ID == 0:
       done_ID = 1
    elif player_ID == 1:
        done_ID = 2
    elif player_ID == 2:
        done_ID = 3
    elif player_ID == 3:
        done_ID = 4
    elif player_ID == 4:
        btn["state"] = "disabled"



#When "done" button is pressed
def done():
    e

#apparence du bouton new character
btn = tkinter.Button(UI, text="New Character", bd=0, bg="#3285F4", fg="White", padx=30, pady=10, font="Montserrat", relief=FLAT, command=btn)
btn['font'] = myFont
btn.place(x=25, y=25)

#apparence du bouton delete
btn2 = tkinter.Button(UI, text="Delete this character", bd=0, bg="#C4C4C4", fg="White", padx=30, pady=10, font="Montserrat", relief=FLAT, state=DISABLED, command=action)
btn2['font'] = myFont
btn2.place(x=325, y=25)

#apparence du bouton done
btn3 = tkinter.Button(UI, text="Done", bd=0, bg="#4285F4", fg="White", padx=30, pady=10, font="Montserrat", relief=FLAT, command=done)
btn3['font'] = myFont
btn3.place_forget()

#UI of "Character 1"
Ch1 = tkinter.Button(UI, text= player1_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2, font="Montserrat", relief=FLAT, command=btn)
Ch1['font'] = myFont
if player_ID >= 1:
    Ch1.place(x=25, y=175)
else:
    Ch1.place_forget()

#UI of "Character 2"
Ch2 = tkinter.Button(UI, text=player2_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2, font="Montserrat", relief=FLAT, command=btn)
Ch2['font'] = myFont
if player_ID >= 2:
    Ch2.place(x=25, y=300)

else:
    Ch2.place_forget()

#UI of "Character 3"
Ch3 = tkinter.Button(UI, text=player3_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2, font="Montserrat", relief=FLAT, command=btn)
Ch3['font'] = myFont
if player_ID >=3:
    Ch3.place(x=25, y=425)
else:
    Ch3.place_forget()

#UI of "Character 4"
Ch4 = tkinter.Button(UI, text=player4_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2, font="Montserrat", relief=FLAT, command=btn)
Ch4['font'] = myFont
if player_ID >= 4:
    Ch4.place(x=25, y=550)
else:
    Ch4.place_forget()


# First text with text box
Character_name = Label(UI, text="Character name", font=("Montserat", 14), fg="#323232")
Character_name.place_forget()

Character_name_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Character_name_box.place_forget()
Character_name_box.insert(tkinter.END, player_name)

# Second text with text box
Breed = Label(UI, text="Breed", font=("Montserat", 14), fg="#323232")
Breed.place_forget()

Breed_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Breed_box.place_forget()
Breed_box.insert(tkinter.END, player_race)

# Third text with text box
Health = Label(UI, text="Health", font=("Montserat", 14), fg="#323232")
Health.place_forget()

Health_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Health_box.place_forget()
Health_box.insert(tkinter.END, player_life)

# 4th text with text box
Speed = Label(UI, text="Speed", font=("Montserat", 14), fg="#323232")
Speed.place_forget()

Speed_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Speed_box.place_forget()
Speed_box.insert(tkinter.END, player_speed)

# 5th text with text box
Attack = Label(UI, text="Attack", font=("Montserat", 14), fg="#323232")
Attack.place_forget()

Attack_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Attack_box.place_forget()
Attack_box.insert(tkinter.END, player_attack)

# 6th text with text box
Defense = Label(UI, text="Defense", font=("Montserat", 14), fg="#323232")
Defense.place_forget()

Defense_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Defense_box.place_forget()
Defense_box.insert(tkinter.END, player_defense)

# 7th text with text box
Background = Label(UI, text="Background", font=("Montserat", 14), fg="#323232")
Background.place_forget()

Background_box = tkinter.Text(UI, height=1, width=30, font=("Montserat", 14),fg="#4285F4")
Background_box.place_forget()
Background_box.insert(tkinter.END, player_Background)


UI.mainloop()
