# All necessary imports

import tkinter
from tkinter import *
from tkinter import ttk
import sqlite3
import re

# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
screen_x = editor.winfo_screenwidth()
screen_y = editor.winfo_screenheight()
window_x = 1200
window_y = 800

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
create_button, edit_button, delete_button = PhotoImage(file='New Character.png'), PhotoImage(file='Edit Character.png'), PhotoImage(file='Delete Character.png')
database = "databaseV1.db"

def CreateButton_action():  # When "create new character" is pressed
    global C2_ID, C2_name, C2_breed, C2_life, C2_speed, C2_attack, C2_defense, C2_background

    create = Toplevel()
    create.title("Create a character")
    screen_x_2 = create.winfo_screenwidth()
    screen_y_2 = create.winfo_screenheight()
    window_x_2 = 410
    window_y_2 = 250
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    create.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Create Text Boxes
    C2_ID = Entry(create, width=30)
    C2_ID.grid(row=0, column=1, padx=(10, 0), pady=(25, 0))

    C2_name = Entry(create, width=30)
    C2_name.grid(row=1, column=1, padx=(10, 0))

    C2_breed = Entry(create, width=30)
    C2_breed.grid(row=2, column=1, padx=(10, 0))

    C2_life = Entry(create, width=30)
    C2_life.grid(row=3, column=1, padx=(10, 0))

    C2_speed = Entry(create, width=30)
    C2_speed.grid(row=4, column=1, padx=(10, 0))

    C2_attack = Entry(create, width=30)
    C2_attack.grid(row=5, column=1, padx=(10, 0))

    C2_defense = Entry(create, width=30)
    C2_defense.grid(row=6, column=1, padx=(10, 0))

    C2_background = Entry(create, width=30)
    C2_background.grid(row=7, column=1, padx=(10, 0))

    # Create Text Box Labels
    C2_ID_label = Label(create, text="Character ID")
    C2_ID_label.grid(row=0, column=0, padx=(25, 0), pady=(25, 0))

    C2_name_label = Label(create, text="Name")
    C2_name_label.grid(row=1, column=0, padx=(25, 0))

    C2_breed_label = Label(create, text="Breed")
    C2_breed_label.grid(row=2, column=0, padx=(25, 0))

    C2_life_label = Label(create, text="Life")
    C2_life_label.grid(row=3, column=0, padx=(25, 0))

    C2_speed_label = Label(create, text="Speed")
    C2_speed_label.grid(row=4, column=0, padx=(25, 0))

    C2_attack_label = Label(create, text="Attack")
    C2_attack_label.grid(row=5, column=0, padx=(25, 0))

    C2_defense_label = Label(create, text="Defense")
    C2_defense_label.grid(row=6, column=0, padx=(25, 0))

    C2_background_label = Label(create, text="Background")
    C2_background_label.grid(row=7, column=0, padx=(25, 0))

    # Set up the create button
    submit_button = Button(create, text="Create this character", command=submit)
    submit_button.grid(row=8, column=0, columnspan=2, pady=15, padx=25, ipadx=120)


# Create Function to delete a record
def delete():
    global select_box

    delete = Toplevel()
    delete.title("Delete a character")
    screen_x_2 = delete.winfo_screenwidth()
    screen_y_2 = delete.winfo_screenheight()
    window_x_2 = 390
    window_y_2 = 100
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    delete.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Creating character ID box and  character ID label
    global delete_box
    delete_box = Entry(delete, width=35)
    delete_box.grid(row=0, column=1, padx=20, pady=(20, 0))
    C_ID_delete = Label(delete, text="Character ID")
    C_ID_delete.grid(row=0, column=0, pady=(10, 0))



    # Set up the delete button
    delete_button = Button(delete, text="Delete this character", command=delete_action)
    delete_button.grid(row=8, column=0, columnspan=2, pady=15, padx=25, ipadx=110)

def delete_action():
    # Set up database or connect to one
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Delete a record
    delete_id = delete_box.get()
    c.execute(f"DELETE FROM characters WHERE character_ID={delete_id}")

    # Upload changes & close connection
    conn.commit()
    conn.close()



# Create Submit Function for database
def submit():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS characters
             (ch_id text,
             character_name text, 
             character_breed text,
             character_life integer,
             character_speed integer,
             character_defense integer,
             character_attack integer,
             character_background text)""")

    # Insert into table
    c.execute("""INSERT INTO characters VALUES (:ch_id, :character_name, :character_breed, :character_life, :character_speed, :character_defense, :character_attack, :character_background)""",
        {
            'ch_id': str(C2_ID.get()),
            'character_name': str(C2_name.get()),
            'character_breed': str(C2_breed.get()),
            'character_life': int(C2_life.get()),
            'character_speed': int(C2_speed.get()),
            'character_defense': int(C2_defense.get()),
            'character_attack': int(C2_attack.get()),
            'character_background': str(C2_background.get())
        })

    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()

    # Clear the Text Boxes
    C2_ID.delete(0, END)
    C2_name.delete(0, END)
    C2_breed.delete(0, END)
    C2_life.delete(0, END)
    C2_speed.delete(0, END)
    C2_defense.delete(0, END)
    C2_attack.delete(0, END)
    C2_background.delete(0, END)


# Create Query Function. For display characters
def show_characters():
    global root
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect(database)
    c = conn.cursor()

    for i in c.execute("SELECT character_ID FROM characters "):
        i = i[0]







    # Query The database
    c.execute("SELECT * FROM characters")
    records = c.fetchall()

    print_records = ""
    for record in records:
        for item in record:
            print_records += str(item) + "\n"

    character_print = Message(query_label, text=print_records)
    character_print.grid()


    # Commit changes & close connexion
    conn.commit()
    conn.close()




# Create an Update function to update the new stuff that was input inside the Entry boxes
def update():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    record_id = C_ID_editor.get()
    c.execute(f"""UPDATE characters SET
    character_name = :C_name,
    character_breed = :C_breed,
    character_life = :C_life,
    character_speed = :C_speed,
    character_attack = :C_attack,
    character_defense = :C_defense,
    character_background = :C_background 

    WHERE ch_id = :ch_id""",
              {
                  "C_name": C_name_editor.get(),
                  "C_breed": C_breed_editor.get(),
                  "C_life": C_life_editor.get(),
                  "C_speed": C_speed_editor.get(),
                  "C_attack": C_attack_editor.get(),
                  "C_defense": C_speed_editor.get(),
                  "C_background": C_attack_editor.get(),
                  "ch_id": record_id})
    conn.commit()
    conn.close()
    editor.destroy()


# Create Edit function to update a record
def edit():
    global editor

    editor = Toplevel()
    editor.title("Edit your character")
    screen_x_2 = editor.winfo_screenwidth()
    screen_y_2 = editor.winfo_screenheight()
    window_x_2 = 325
    window_y_2 = 225
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    editor.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    global C_ID_editor, C_name_editor, C_breed_editor, C_life_editor, C_speed_editor, C_attack_editor, C_defense_editor, C_background_editor

    # Create Text Boxes
    C_ID_editor = Entry(editor, width=30)
    C_ID_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    C_name_editor = Entry(editor, width=30)
    C_name_editor.grid(row=1, column=1, padx=20)

    C_breed_editor = Entry(editor, width=30)
    C_breed_editor.grid(row=2, column=1, padx=20)

    C_life_editor = Entry(editor, width=30)
    C_life_editor.grid(row=3, column=1, padx=20)

    C_speed_editor = Entry(editor, width=30)
    C_speed_editor.grid(row=4, column=1, padx=20)

    C_attack_editor = Entry(editor, width=30)
    C_attack_editor.grid(row=5, column=1, padx=20)

    C_defense_editor = Entry(editor, width=30)
    C_defense_editor.grid(row=6, column=1, padx=20)

    C_background_editor = Entry(editor, width=30)
    C_background_editor.grid(row=7, column=1, padx=20)

    # Create Text Box Labels
    C_ID_label_editor = Label(editor, text="Character ID")
    C_ID_label_editor.grid(row=0, column=0, pady=(10, 0))

    C_name_label_editor = Label(editor, text="Name")
    C_name_label_editor.grid(row=1, column=0)

    C_breed_label_editor = Label(editor, text="Breed")
    C_breed_label_editor.grid(row=2, column=0)

    C_life_label_editor = Label(editor, text="Life")
    C_life_label_editor.grid(row=3, column=0)

    C_speed_label_editor = Label(editor, text="Speed")
    C_speed_label_editor.grid(row=4, column=0)

    C_attack_label_editor = Label(editor, text="Attack")
    C_attack_label_editor.grid(row=5, column=0)

    C_defense_label_editor = Label(editor, text="Defense")
    C_defense_label_editor.grid(row=6, column=0)

    C_background_label_editor = Label(editor, text="Background")
    C_background_label_editor.grid(row=7, column=0)

    delete_box_label_editor = Label(editor, text="Select ID")
    delete_box_label_editor.grid(row=10, column=0)

    # Create a save Button to save an edited record
    save_btn = Button(editor, text="Update Character", command=update)
    save_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

    editor.mainloop()


# Set up the frame for the buttons
main_frame = LabelFrame(characters_tab, height=250)
main_frame.pack(side=TOP, fill='both')

global query_label
query_label = LabelFrame(characters_tab, height=300)
query_label.pack(side=BOTTOM, anchor=W, fill='both', expand=True)


# Create the 3 main buttons
createButton = Button(main_frame, image=create_button, border=0, command=CreateButton_action)
createButton.grid(column=1, row=0, padx=30, pady=30)
editButton = Button(main_frame, image=edit_button, border=0, command=edit)
editButton.grid(column=2, row=0, padx=15, pady=30)
deleteButton = Button(main_frame, image=delete_button, border=0, command=delete)
deleteButton.grid(column=3, row=0, padx=30, pady=30)

show_characters()
# ----------------------------------------------------
# THIS IS THE END OF THE CODE FOR THE "CHARACTER" TAB
# ----------------------------------------------------

editor.config(menu=main_menu)
editor.mainloop()
