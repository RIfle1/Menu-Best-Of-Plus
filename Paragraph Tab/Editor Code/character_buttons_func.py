# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id

database = 'EditorDataV3.db'


def ch_new_save():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create a new ch_id
    c.execute(f"""SELECT ch_id from characters""")
    ch_new_ch_id_list_raw = c.fetchall()
    ch_new_ch_id_list = id.raw_conv(ch_new_ch_id_list_raw)

    if not ch_new_ch_id_list:
        ch_new_ch_id = 1
    else:
        ch_new_ch_id = int(id.max_num(id.int_list(ch_new_ch_id_list))) + 1

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS characters
             (ch_id text,
             ch_name text, 
             ch_breed text,
             ch_life integer,
             ch_speed integer,
             ch_defense integer,
             ch_attack integer,
             ch_background text)""")

    # Error check:
    try:
        int(ch_new_life_entry_var.get())
        int(ch_new_speed_entry_var.get())
        int(ch_new_defense_entry_var.get())
        int(ch_new_attack_entry_var.get())
        # Insert into table
        c.execute("""INSERT INTO characters VALUES (
        :ch_id, 
        :ch_name, 
        :ch_breed, 
        :ch_life, 
        :ch_speed, 
        :ch_defense, 
        :ch_attack, 
        :ch_background)""",
            {
                'ch_id': str(id.ch_id(ch_new_ch_id)),
                'ch_name': str(ch_new_name_entry_var.get()),
                'ch_breed': str(ch_new_breed_entry_var.get()),
                'ch_life': int(ch_new_life_entry_var.get()),
                'ch_speed': int(ch_new_speed_entry_var.get()),
                'ch_defense': int(ch_new_defense_entry_var.get()),
                'ch_attack': int(ch_new_attack_entry_var.get()),
                'ch_background': str(ch_new_background_text_entry.get("1.0", "end"))
            })
        # Success Message
        messagebox.showinfo("Sucess", f'Character Number {ch_new_ch_id} Has Been Successfully Created.')
        # Clear the Text Boxes
        ch_new_name_entry.delete(0, END)
        ch_new_breed_entry.delete(0, END)
        ch_new_life_entry.delete(0, END)
        ch_new_speed_entry.delete(0, END)
        ch_new_defense_entry.delete(0, END)
        ch_new_attack_entry.delete(0, END)
        ch_new_background_text_entry.delete("1.0", "end")
    except ValueError:
        messagebox.showerror('Value Error', 'Life, Speed, Defense and Attack Must Be Numbers.', icon="warning")
    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


def ch_new_window():
    global ch_new_wd
    # Create New Window
    ch_new_wd = Toplevel()
    ch_new_wd.title("Create A New Character")
    screen_x_2 = ch_new_wd.winfo_screenwidth()
    screen_y_2 = ch_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 440
    ch_new_wd.minsize(window_x_2, window_y_2)
    ch_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    ch_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    ch_new_frame_height = 200
    ch_new_rest = window_y_2 - ch_new_frame_height * 2
    # Info Frame 1
    ch_new_info_frame_1 = LabelFrame(ch_new_wd, width=window_x_2, height=ch_new_frame_height)
    ch_new_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    ch_new_info_frame_2 = LabelFrame(ch_new_wd, width=window_x_2, height=ch_new_frame_height)
    ch_new_info_frame_2.pack(fill="both", side=TOP)

    # Top Button Frame
    ch_new_button_frame = LabelFrame(ch_new_wd, height=ch_new_rest / 2, width=window_x_2)
    ch_new_button_frame.pack(fill="both")

    ch_new_width = 42
    ch_new_pad = 10
    ch_new_entry_width = 49
    ch_new_text_width = 37

    # Labels
    ch_new_name_label = Label(ch_new_info_frame_1, text="Name:", width=int(ch_new_width / 2), anchor=W)
    ch_new_name_label.grid(row=0, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="w")

    ch_new_breed_label = Label(ch_new_info_frame_1, text="Breed:", width=int(ch_new_width / 2),
                                      anchor=W)
    ch_new_breed_label.grid(row=1, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="w")

    ch_new_life_label = Label(ch_new_info_frame_1, text="Life:", width=int(ch_new_width / 2), anchor=NW)
    ch_new_life_label.grid(row=2, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_speed_label = Label(ch_new_info_frame_1, text="Speed:", width=int(ch_new_width / 2), anchor=NW)
    ch_new_speed_label.grid(row=3, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_attack_label = Label(ch_new_info_frame_1, text="Attack:", width=int(ch_new_width / 2),
                                       anchor=NW)
    ch_new_attack_label.grid(row=4, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_defense_label = Label(ch_new_info_frame_1, text="Defense:", width=int(ch_new_width / 2),
                                anchor=NW)
    ch_new_defense_label.grid(row=5, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_background_label = Label(ch_new_info_frame_2, text="Background:", width=int(ch_new_width / 2),
                                anchor=NW)
    ch_new_background_label.grid(row=0, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    # Short Entries
    global ch_new_name_entry_var, ch_new_breed_entry_var, ch_new_life_entry_var, ch_new_speed_entry_var, ch_new_attack_entry_var, ch_new_defense_entry_var, ch_new_background_text_entry
    global ch_new_name_entry, ch_new_breed_entry, ch_new_life_entry, ch_new_speed_entry, ch_new_attack_entry, ch_new_defense_entry
    ch_new_name_entry_var = StringVar()
    ch_new_name_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_name_entry_var, width=ch_new_entry_width)
    ch_new_name_entry.grid(row=0, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_breed_entry_var = StringVar()
    ch_new_breed_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_breed_entry_var, width=ch_new_entry_width)
    ch_new_breed_entry.grid(row=1, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_life_entry_var = StringVar()
    ch_new_life_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_life_entry_var, width=ch_new_entry_width)
    ch_new_life_entry.grid(row=2, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_speed_entry_var = StringVar()
    ch_new_speed_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_speed_entry_var, width=ch_new_entry_width)
    ch_new_speed_entry.grid(row=3, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_attack_entry_var = StringVar()
    ch_new_attack_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_attack_entry_var, width=ch_new_entry_width)
    ch_new_attack_entry.grid(row=4, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    ch_new_defense_entry_var = StringVar()
    ch_new_defense_entry = Entry(ch_new_info_frame_1, textvariable=ch_new_defense_entry_var, width=ch_new_entry_width)
    ch_new_defense_entry.grid(row=5, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="nw")

    # Text Entry
    ch_new_background_text_entry = Text(ch_new_info_frame_2, width=ch_new_text_width, height=7)
    ch_new_background_text_entry.grid(row=0, column=1, padx=ch_new_pad, pady=ch_new_pad)

    # Buttons
    ch_new_save_character_button = Button(ch_new_button_frame, text="Save Character", width=int(ch_new_width / 2),
                                      command=ch_new_save)
    ch_new_save_character_button.grid(row=0, column=0, padx=ch_new_pad, pady=ch_new_pad, stick="w")

    ch_new_cancel_button = Button(ch_new_button_frame, text="Cancel", width=ch_new_width, command=ch_new_wd.destroy)
    ch_new_cancel_button.grid(row=0, column=1, padx=ch_new_pad, pady=ch_new_pad, stick="w")

    ch_new_wd.mainloop()


