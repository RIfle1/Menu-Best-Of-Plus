from tkinter import *
import sqlite3

root = Tk()
root.title("GUI Database")
screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()
window_x = 356
window_y = 600
pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)
root.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")


# Create Function to delete a record
def delete():
    # Set upa database or connect to one
    conn = sqlite3.connect("databaseV1.db")
    c = conn.cursor()

    # Delete a record
    c.execute(f"DELETE from characters WHERE oid={select_box.get()}")

    # Upload changes & close connection
    conn.commit()
    conn.close()

# Create Submit Function for database

def submit():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect("databaseV1.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS characters
             (character_ID integer,
             character_name text, 
             character_breed text,
             character_life integer,
             character_speed integer,
             character_defense integer,
             character_attack integer,
             character_background text)""")

    # Insert into table
    c.execute("""INSERT INTO characters VALUES (:character_ID, :character_name, :character_breed, :character_life, :character_speed, :character_defense, :character_attack, :character_background)""",
        {
            'character_ID': int(C2_ID.get()),
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


# Create Query Function
def query():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect("databaseV1.db")
    c = conn.cursor()

    # Query The database
    c.execute("SELECT * FROM characters")
    records = c.fetchall()

    print_records = ""
    for record in records:
        for item in record:
            print_records += str(item) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=11, column=0, columnspan=2)

    # Commit changes & close connexion
    conn.commit()
    conn.close()


# Create an Update function to update the new stuff that was input inside the Entry boxes
def update():
    conn = sqlite3.connect("databaseV1.db")
    c = conn.cursor()

    record_id = select_box.get()
    c.execute(f"""UPDATE characters SET
    character_ID = :C_ID,
    character_name = :C_name,
    character_breed = :C_breed,
    character_life = :C_life,
    character_speed = :C_speed,
    character_attack = :C_attack,
    character_defense = :C_defense,
    character_background = :C_background 
    
    WHERE oid = :oid""",
              {
                  "C_ID": C_ID_editor.get(),
                  "C_name": C_name_editor.get(),
                  "C_breed": C_breed_editor.get(),
                  "C_life": C_life_editor.get(),
                  "C_speed": C_speed_editor.get(),
                  "C_attack": C_attack_editor.get(),
                  "C_defense": C_speed_editor.get(),
                  "C_background": C_attack_editor.get(),

                  "oid": record_id})
    conn.commit()
    conn.close()
    editor.destroy()


# Create Edit function to update a record

def edit():
    global editor

    editor = Toplevel()
    editor.title("Update a Record")
    screen_x_2 = editor.winfo_screenwidth()
    screen_y_2 = editor.winfo_screenheight()
    window_x_2 = 356
    window_y_2 = 250
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    editor.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Create Global Variables for text box names

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

    delete_box_editor = Entry(editor, width=30)
    delete_box_editor.grid(row=10, column=1, padx=20)

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
    save_btn = Button(editor, text="Save Character", command=update)
    save_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=131)

    # Connection start
    conn = sqlite3.connect("databaseV1.db")
    c = conn.cursor()

    record_id = select_box.get()

    c.execute(f"SELECT * FROM characters WHERE oid={record_id}")
    records = c.fetchall()

    # Loop through the results
    for record in records:
        C_ID_editor.insert(0, record[0])
        C_name_editor.insert(0, record[1])
        C_breed_editor.insert(0, record[2])
        C_life_editor.insert(0, record[3])
        C_speed_editor.insert(0, record[4])
        C_attack_editor.insert(0, record[5])
        C_defense_editor.insert(0, record[6])
        C_background_editor.insert(0, record[7])

    conn.commit()
    conn.close()

    editor.mainloop()




# Create Text Box Labels

C2_ID_label = Label(root, text="Character ID")
C2_ID_label.grid(row=0, column=0, pady=(10, 0))

C2_name_label = Label(root, text="Name")
C2_name_label.grid(row=1, column=0)

C2_breed_label = Label(root, text="Breed")
C2_breed_label.grid(row=2, column=0)

C2_life_label = Label(root, text="Life")
C2_life_label.grid(row=3, column=0)

C2_speed_label = Label(root, text="Speed")
C2_speed_label.grid(row=4, column=0)

C2_attack_label = Label(root, text="Attack")
C2_attack_label.grid(row=5, column=0)

C2_defense_label = Label(root, text="Defense")
C2_defense_label.grid(row=6, column=0)

C2_background_label = Label(root, text="Background")
C2_background_label.grid(row=7, column=0)

delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=10, column=0)

# Create Submit Button
submit_button = Button(root, text="Add this character to database", command=submit)
submit_button.grid(row=8, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a Query Button
query_btn = Button(root, text="Show characters", command=query)
query_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=124)

# Create a delete button
query_btn = Button(root, text="Delete character", command=delete)
query_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Create an update button
edit_btn = Button(root, text="Edit character", command=edit)
edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=131)

root.mainloop()

# A REPLACER

# Pour mettre l'ID du perso à modifier ou à supprimer
global select_box
select_box = Entry(create, width=30)
select_box.grid(row=10, column=1, padx=(0, 0))

# le label de la boite au dessus
delete_box_label = Label(create, text="Select ID")
delete_box_label.grid(row=10, column=0, padx=(25, 0))

# Create a Query Button
query_btn = Button(create, text="Show characters", command=query)
query_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=124)

# Create a delete button
query_btn = Button(create, text="Delete character", command=delete)
query_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Create an update button
edit_btn = Button(create, text="Edit character", command=edit)
edit_btn.grid(row=12, column=0, columnspan=2, pady=10, padx=10, ipadx=131)


