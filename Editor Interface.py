# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font

# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
screen_x = editor.winfo_screenwidth()
screen_y = editor.winfo_screenheight()
window_x = 1200
window_y = 825

pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)

editor.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# Adding the Menus
main_menu = tkinter.Menu(editor)

file_menu = tkinter.Menu(main_menu, tearoff=0)
file_menu.add_command(label="New Game Editor")
file_menu.add_command(label="Load Game Editor")
file_menu.add_command(label="Save Game Editor")

options_menu = tkinter.Menu(main_menu, tearoff=0)
options_menu.add_command(label="Change Paragraph Order")
options_menu.add_command(label="Dark Mode")
options_menu.add_command(label="Quit", command=editor.quit)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Options", menu=options_menu)

# Tab Control
tabControl = ttk.Notebook(editor)

# Creating Tabs
paragraphs_tab = ttk.Frame(tabControl)
characters_tab = ttk.Frame(tabControl)
objects_tab = ttk.Frame(tabControl)
game_settings_tab = ttk.Frame(tabControl)
test_tab = ttk.Frame(tabControl)

# Adding Tabs
tabControl.add(paragraphs_tab, text="Paragraphs")
tabControl.add(characters_tab, text="Characters")
tabControl.add(objects_tab, text="Objects")
tabControl.add(game_settings_tab, text="Game Settings")
tabControl.add(test_tab, text="Test")

# Positioning the Tabs
tabControl.pack(expand=1, fill="both")

# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "CHARACTER" TAB
# -------------------------------------------

# define font size
myFont = font.Font(size=20)

# def of all necessary variables
Character1_set = Character2_set = Character3_set = Character4_set = 0  # To know which character is used and which is not
active_character = 0  # It's the Character which is editing in the editor page

# All important variables
player_name = player1_name = player2_name = player3_name = player4_name = str("")
player_breed = player1_breed = player2_breed = player3_breed = player4_breed = str("")
player_life = player1_life = player2_life = player3_life = player4_life = int("0")
player_speed = player1_speed = player2_speed = player3_speed = player4_speed = int("0")
player_defense = player1_defense = player2_defense = player3_defense = player4_defense = int("0")
player_attack = player1_attack = player2_attack = player3_attack = player4_attack = int("0")
player_Background = player1_Background = player2_Background = player3_Background = player4_Background = str("")
Compile_blue, Compile_grey, Test_blue, Test_fail, Test_pass, Back, Coding_Success = PhotoImage(file='Compile_blue.png'), PhotoImage(file='Compile_grey.png'), PhotoImage(file='Test_blue.png'), PhotoImage(file='Test_fail.png'), PhotoImage(file='Test_pass.png'), PhotoImage(file='Back_button.png'), PhotoImage(file='Coding_success.png')
Character_name = Character_name_box = Breed = Breed_box = Health = Health_box = Speed = Speed_box = Attack = Attack_box = Defense = Defense_box = Background = Background_box = None
CH1 = CH2 = CH3 = CH4 = ""


# Def some functions for better optimisation
def Character_name_line():  # Display text "Character_name" text with the text box UI
    global Character_name, Character_name_box
    Character_name = Label(characters_tab, text="Character name", font=("Montserrat", 14), fg="#323232")
    Character_name.place_forget()
    Character_name_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Character_name_box.place_forget()
    Character_name_box.insert(tkinter.END, player_name)
    Character_name.place(x=25, y=150)
    Character_name_box.place(x=325, y=150)


def Breed_line():  # Display text "Breed" text with the text box UI
    global Breed, Breed_box
    Breed = Label(characters_tab, text="Breed", font=("Montserrat", 14), fg="#323232")
    Breed.place_forget()
    Breed_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Breed_box.place_forget()
    Breed_box.insert(tkinter.END, player_breed)
    Breed.place(x=25, y=200)
    Breed_box.place(x=325, y=200)


def Health_line():  # Display text "Health" text with the text box UI
    global Health, Health_box
    Health = Label(characters_tab, text="Health", font=("Montserrat", 14), fg="#323232")
    Health.place_forget()
    Health_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Health_box.place_forget()
    Health_box.insert(tkinter.END, player_life)
    Health.place(x=25, y=250)
    Health_box.place(x=325, y=250)


def Speed_line():  # Display text "Speed" text with the text box UI
    global Speed, Speed_box
    Speed = Label(characters_tab, text="Speed", font=("Montserrat", 14), fg="#323232")
    Speed.place_forget()
    Speed_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Speed_box.place_forget()
    Speed_box.insert(tkinter.END, player_speed)
    Speed.place(x=25, y=300)
    Speed_box.place(x=325, y=300)


def Attack_line():  # Display text "Attack" text with the text box UI
    global Attack, Attack_box
    Attack = Label(characters_tab, text="Attack", font=("Montserrat", 14), fg="#323232")
    Attack.place_forget()
    Attack_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Attack_box.place_forget()
    Attack_box.insert(tkinter.END, player_attack)
    Attack.place(x=25, y=350)
    Attack_box.place(x=325, y=350)


def Defense_line():  # Display text "Defense" text with the text box UI
    global Defense, Defense_box
    Defense = Label(characters_tab, text="Defense", font=("Montserrat", 14), fg="#323232")
    Defense.place_forget()
    Defense_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Defense_box.place_forget()
    Defense_box.insert(tkinter.END, player_defense)
    Defense.place(x=25, y=400)
    Defense_box.place(x=325, y=400)


def Background_line():  # Display text "Background" text with the text box UI
    global Background, Background_box
    Background = Label(characters_tab, text="Background", font=("Montserrat", 14), fg="#323232")
    Background.place_forget()
    Background_box = tkinter.Text(characters_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    Background_box.place_forget()
    Background_box.insert(tkinter.END, player_Background)
    Background.place(x=25, y=450)
    Background_box.place(x=325, y=450)


def Show_all_lines():  # This show and update all text line & text box seamless together
    Character_name_line()
    Breed_line()
    Health_line()
    Speed_line()
    Attack_line()
    Defense_line()
    Background_line()


def Hide_all_lines():  # Just hide all lines together
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


def CH1_component():  # Define the "Character 1" component and if it has to be displayed or not
    global Character1_set, CH1
    CH1 = tkinter.Button(characters_tab, text=player1_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2,
                         font="Montserrat", relief=FLAT, command=CH1_action)
    CH1['font'] = myFont
    if Character1_set == 1:
        CH1.place(x=25, y=175)
    else:
        CH1.place_forget()


def CH1_action():  # When CH1_component is clicked
    global active_character, player_name, player_breed, player_speed, player_defense, player_attack, player_Background, player_life
    global player1_name, player1_breed, player1_speed, player1_defense, player1_attack, player1_Background, player1_life
    active_character = 1
    player_name, player_breed, player_speed, player_life, player_defense, player_attack, player_Background = player1_name, player1_breed, player1_speed, player1_life, player1_defense, player1_attack, player1_Background
    CreateButton["state"] = "disabled"
    CreateButton["bg"] = "#C4C4C4"
    DeleteButton["state"] = "normal"
    DeleteButton["bg"] = "#E86351"
    DoneButton.place(x=1025, y=675)
    Hide_CH_components()
    Show_all_lines()


def CH2_component():  # Define the "Character 2" component and if it has to be displayed or not
    global Character2_set, CH2
    CH2 = tkinter.Button(characters_tab, text=player2_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2,
                         font="Montserrat", relief=FLAT, command=CH2_action)
    CH2['font'] = myFont
    if Character2_set == 1:
        CH2.place(x=25, y=300)
    else:
        CH2.place_forget()


def CH2_action():  # When CH2_component is clicked
    global active_character, player_name, player_breed, player_speed, player_defense, player_attack, player_Background, player_life
    global player2_name, player2_breed, player2_speed, player2_defense, player2_attack, player2_Background, player2_life
    active_character = 2
    player_name, player_breed, player_speed, player_life, player_defense, player_attack, player_Background = player2_name, player2_breed, player2_speed, player2_life, player2_defense, player2_attack, player2_Background
    CreateButton["state"] = "disabled"
    CreateButton["bg"] = "#C4C4C4"
    DeleteButton["state"] = "normal"
    DeleteButton["bg"] = "#E86351"
    DoneButton.place(x=1025, y=675)
    Hide_CH_components()
    Show_all_lines()


def CH3_component():  # Define the "Character 3" component and if it has to be displayed or not
    global Character3_set, CH3
    CH3 = tkinter.Button(characters_tab, text=player3_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2,
                         font="Montserrat", relief=FLAT, command=CH3_action)
    CH3['font'] = myFont
    if Character3_set == 1:
        CH3.place(x=25, y=425)
    else:
        CH3.place_forget()


def CH3_action():  # When CH3_component is clicked
    global active_character, player_name, player_breed, player_speed, player_defense, player_attack, player_Background, player_life
    global player3_name, player3_breed, player3_speed, player3_defense, player3_attack, player3_Background, player3_life
    active_character = 3
    player_name, player_breed, player_speed, player_life, player_defense, player_attack, player_Background = player3_name, player3_breed, player3_speed, player3_life, player3_defense, player3_attack, player3_Background
    CreateButton["state"] = "disabled"
    CreateButton["bg"] = "#C4C4C4"
    DeleteButton["state"] = "normal"
    DeleteButton["bg"] = "#E86351"
    DoneButton.place(x=1025, y=675)
    Hide_CH_components()
    Show_all_lines()


def CH4_component():  # Define the "Character 4" component and if it has to be displayed or not
    global Character4_set, CH4
    CH4 = tkinter.Button(characters_tab, text=player4_name, bd=0, bg="#FFFFFF", fg="#4285F4", width=63, height=2,
                         font="Montserrat", relief=FLAT, command=CH4_action)
    CH4['font'] = myFont
    if Character4_set == 1:
        CH4.place(x=25, y=550)
    else:
        CH4.place_forget()


def CH4_action():  # When CH4_component is clicked
    global active_character, player_name, player_breed, player_speed, player_defense, player_attack, player_Background, player_life
    global player4_name, player4_breed, player4_speed, player4_defense, player4_attack, player4_Background, player4_life
    active_character = 4
    player_name, player_breed, player_speed, player_life, player_defense, player_attack, player_Background = player4_name, player4_breed, player4_speed, player4_life, player4_defense, player4_attack, player4_Background
    CreateButton["state"] = "disabled"
    CreateButton["bg"] = "#C4C4C4"
    DeleteButton["state"] = "normal"
    DeleteButton["bg"] = "#E86351"
    DoneButton.place(x=1025, y=675)
    Hide_CH_components()
    Show_all_lines()


def Show_CH_components():  # Show and update the four CH components at once AND "Test" button
    CH1_component()
    CH2_component()
    CH3_component()
    CH4_component()


def Hide_CH_components():  # Just hide all CH components
    global CH4, CH3, CH2, CH1
    CH4.place_forget()
    CH3.place_forget()
    CH2.place_forget()
    CH1.place_forget()


def Delete_action():  # When "delete this character" is pressed
    global CreateButton, player1_name, player1_breed, player1_life, player1_speed, player1_defense, player1_attack, player1_Background, Character1_set, player_name, player_breed, player_speed, player_defense, player_attack, player_Background, player_life
    global player2_name, player2_breed, player2_life, player2_speed, player2_defense, player2_attack, player2_Background, Character2_set
    global player3_name, player3_breed, player3_life, player3_speed, player3_defense, player3_attack, player3_Background, Character3_set
    global player4_name, player4_breed, player4_life, player4_speed, player4_defense, player4_attack, player4_Background, Character4_set
    result = messagebox.askquestion(title="Not so fast",
                                    message="You're about to delete this character. Are you sure do you want to continue ?",
                                    icon="warning")
    if result == 'yes':

        # First, Clear the default values
        player_name = player_Background = player_breed = ""
        player_life = player_speed = player_defense = player_attack = 0

        # Second, determine which is the character to delete
        if active_character == 1:
            player1_name = player1_Background = player1_breed = ""
            player1_life = player1_speed = player1_defense = player1_attack = Character1_set = 0
        elif active_character == 2:
            player2_name = player2_Background = player2_breed = ""
            player2_life = Character2_set = player2_attack = player2_defense = player2_speed = 0
        elif active_character == 3:
            player3_name = player3_Background = player3_breed = ""
            player3_life = player3_attack = Character3_set = player3_defense = player3_speed = 0
        elif active_character == 4:
            player4_name = player4_breed = player4_Background = ""
            player4_life = player4_attack = Character4_set = player4_defense = player4_speed = 0

        # Third, update the UI
        CreateButton["state"] = "normal"
        CreateButton["bg"] = "#4285F4"
        DeleteButton["state"] = "disabled"
        DeleteButton["bg"] = "#C4C4C4"
        DoneButton.place_forget()
        Hide_all_lines()
        Show_CH_components()


def CreateButton_action():  # When "create new character" is pressed
    global CreateButton, DeleteButton, DoneButton, active_character, Character1_set, Character2_set, Character3_set, Character4_set

    # Define which character will get the values
    if Character1_set == 0:
        active_character = 1
    elif Character2_set == 0:
        active_character = 2
    elif Character3_set == 0:
        active_character = 3
    elif Character4_set == 0:
        active_character = 4

    # To update the UI
    CreateButton["state"] = "disabled"
    CreateButton["bg"] = "#C4C4C4"
    DeleteButton["state"] = "normal"
    DeleteButton["bg"] = "#E86351"
    DoneButton.place(x=1025, y=675)
    Show_all_lines()
    Hide_CH_components()


def DoneButton_action():  # When "done" button is pressed
    global CreateButton, active_character, player1_name, player1_breed, player1_life, player1_speed, player1_defense, player1_attack, player1_Background, Character1_set
    global player2_name, player2_breed, player2_life, player2_speed, player2_defense, player2_attack, player2_Background, Character2_set
    global player3_name, player3_breed, player3_life, player3_speed, player3_defense, player3_attack, player3_Background, Character3_set
    global player4_name, player4_breed, player4_life, player4_speed, player4_defense, player4_attack, player4_Background, Character4_set
    global Character_name_box, Breed_box, Health_box, Speed_box, Defense_box, Attack_box, Background_box

    # This following lines is for get which is write in the text box
    if active_character == 1:
        player1_name = ""
        player1_name = Character_name_box.get("1.0", END + "-1c")
        player1_breed = Breed_box.get("1.0", END + "-1c")
        player1_life = Health_box.get("1.0", END + "-1c")
        player1_speed = Speed_box.get("1.0", END + "-1c")
        player1_defense = Defense_box.get("1.0", END + "-1c")
        player1_attack = Attack_box.get("1.0", END + "-1c")
        player1_Background = Background_box.get("1.0", END + "-1c")
        Character1_set = 1
    elif active_character == 2:
        player2_name = Character_name_box.get("1.0", END + "-1c")
        player2_breed = Breed_box.get("1.0", END + "-1c")
        player2_life = Health_box.get("1.0", END + "-1c")
        player2_speed = Speed_box.get("1.0", END + "-1c")
        player2_defense = Defense_box.get("1.0", END + "-1c")
        player2_attack = Attack_box.get("1.0", END + "-1c")
        player2_Background = Background_box.get("1.0", END + "-1c")
        Character2_set = 1
    elif active_character == 3:
        player3_name = Character_name_box.get("1.0", END + "-1c")
        player3_breed = Breed_box.get("1.0", END + "-1c")
        player3_life = Health_box.get("1.0", END + "-1c")
        player3_speed = Speed_box.get("1.0", END + "-1c")
        player3_defense = Defense_box.get("1.0", END + "-1c")
        player3_attack = Attack_box.get("1.0", END + "-1c")
        player3_Background = Background_box.get("1.0", END + "-1c")
        Character3_set = 1
    elif active_character == 4:
        player4_name = Character_name_box.get("1.0", END + "-1c")
        player4_breed = Breed_box.get("1.0", END + "-1c")
        player4_life = Health_box.get("1.0", END + "-1c")
        player4_speed = Speed_box.get("1.0", END + "-1c")
        player4_defense = Defense_box.get("1.0", END + "-1c")
        player4_attack = Attack_box.get("1.0", END + "-1c")
        player4_Background = Background_box.get("1.0", END + "-1c")
        Character4_set = 1

    # If there are 4 Characters configured, disable the "Create new character" button
    if Character1_set == Character2_set == Character3_set == Character4_set == 1:
        CreateButton["state"] = "disabled"
        CreateButton["bg"] = "#C4C4C4"
    else:
        CreateButton["state"] = "normal"
        CreateButton["bg"] = "#4285F4"

    # Updating the UI ...
    active_character = 0
    DeleteButton["state"] = "disabled"
    DeleteButton["bg"] = "#C4C4C4"
    DoneButton.place_forget()
    Hide_all_lines()
    Show_CH_components()


# MAIN CODE
# "Create New character" button UI
CreateButton = tkinter.Button(characters_tab, text="New Character", bd=0, bg="#3285F4", fg="White", padx=30, pady=10,
                              font="Montserrat", relief=FLAT, command=CreateButton_action)
CreateButton['font'] = myFont
CreateButton.place(x=25, y=25)

# "Delete" button UI
DeleteButton = tkinter.Button(characters_tab, text="Delete this character", bd=0, bg="#C4C4C4", fg="White", padx=30,
                              pady=10, font="Montserrat", relief=FLAT, state=DISABLED, command=Delete_action)
DeleteButton['font'] = myFont
DeleteButton.place(x=335, y=25)

# "Done" button UI
DoneButton = tkinter.Button(characters_tab, text="Done", bd=0, bg="#4285F4", fg="White", padx=30, pady=10,
                            font="Montserrat", relief=FLAT, command=DoneButton_action)
DoneButton['font'] = myFont
DoneButton.place_forget()

Show_CH_components()
# ----------------------------------------------------
# THIS IS THE END OF THE CODE FOR THE "CHARACTER" TAB
# ----------------------------------------------------

# ------------------------------------------
# THIS FOLLOWING CODE IS FOR THE "TEST" TAB
# ------------------------------------------
Fail_reason = None

def Test_action_fail():  # If the test fail
    Fail_canvas.create_image(10, 25, anchor=NW, image=Test_fail)
    Fail_canvas.pack()
    Test_button.place_forget()
    Fail_explain['text'] = Fail_reason
    Fail_explain.place(x=25, y=200)

def Test_action_pass():  # If the test pass / is succeed
    Test_button.place_forget()
    Pass_canvas.pack()
    Pass_canvas.create_image(10, 25, anchor=NW, image=Test_pass)
    Pass_illustration.pack()
    Pass_illustration.create_image(0, -5, anchor=NW, image=Coding_Success)
    Back_button.place(x=25, y=25)
    Compile_button["state"] = "normal"

def Back_action():  # When you click on "Back" button
    Fail_explain.place_forget()
    Pass_canvas.pack_forget()
    Pass_illustration.pack_forget()
    Fail_canvas.pack_forget()
    Back_button.place_forget()
    Test_button.place(x=470, y=25)
    Compile_button.place(x=433, y=150)

def TestButton_action():  # When "test" in pressed. fin t'as compris t pas con si ?
    Back_button.place(x=25, y=25)
    Test_button.place_forget()
    Compile_button.place_forget()
    Safety_Check_Up()

def Safety_Check_Up():  # It's all the process behind the "test" button
    global Fail_reason, player1_name, player1_breed, player1_life, player1_speed, player1_defense, player1_attack, player1_Background, Character1_set
    global player2_name, player2_breed, player2_life, player2_speed, player2_defense, player2_attack, player2_Background, Character2_set
    global player3_name, player3_breed, player3_life, player3_speed, player3_defense, player3_attack, player3_Background, Character3_set
    global player4_name, player4_breed, player4_life, player4_speed, player4_defense, player4_attack, player4_Background, Character4_set

    # Write bellow all conditions that the editor have to respect
    while True:
        if Character1_set == Character2_set == Character3_set == Character4_set == 0:
            Fail_reason = "You must set up at least one Character"
            Test_action_fail()
            break
        if Character1_set == 1 and player1_name == "":
            Fail_reason = "Your Character 1 has no name"
            Test_action_fail()
            break
        if Character2_set == 1 and player2_name == "":
            Fail_reason = "Your Character 2 has no name"
            Test_action_fail()
            break
        if Character3_set == 3 and player3_name == "":
            Fail_reason = "Your Character 3 has no name"
            Test_action_fail()
            break
        if Character4_set == 4 and player4_name == "":
            Fail_reason = "Your Character 4 has no name"
            Test_action_fail()
            break
        else:
            Test_action_pass() # If the editor have done everything well
            break


# "Compile" button UI
Compile_button = Button(test_tab, image=Compile_blue, border=0)
Compile_button.place(x=433, y=150)
Compile_button["state"] = "disabled"

# "Test" button UI
Test_button = Button(test_tab, image=Test_blue, border=0, command=TestButton_action, state=NORMAL)
Test_button.place(x=470, y=25)

# "Back" button UI
Back_button = Button(test_tab, image=Back, border=0, command=Back_action)
Back_button.place_forget()

# "Fail explanation" UI
Fail_explain = tkinter.Button(test_tab, text=Fail_reason, bd=0, bg="#FFFFFF", fg="#323232", width=63, height=2,font="Montserrat", relief=FLAT)
Fail_explain['font'] = myFont
Fail_explain.place_forget()

# "Pass" canvas
Pass_canvas = Canvas(test_tab, width=270, height=160)
Pass_canvas.pack_forget()

# "Pass" illustration (by freepik)
Pass_illustration = Canvas(test_tab, width=917, height=650)
Pass_illustration.pack_forget()

# "Fail" canvas
Fail_canvas = Canvas(test_tab, width=270, height=160)
Fail_canvas.pack_forget()

# -----------------------------------------------
# THIS IS THE END OF THE CODE FOR THE "TEST" TAB
# -----------------------------------------------


editor.config(menu=main_menu)
editor.mainloop()
