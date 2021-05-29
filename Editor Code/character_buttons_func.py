# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id
import editor_settings


def ch_new_save():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect(database, uri=True)
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
        messagebox.showinfo("Success", f'Character Number {ch_new_ch_id} Has Been Successfully Created.')
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


def ch_new_window():
    global ch_new_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    ch_new_wd = Toplevel()
    ch_new_wd.title("Create A New Character")
    screen_x_2 = ch_new_wd.winfo_screenwidth()
    screen_y_2 = ch_new_wd.winfo_screenheight()
    window_x_2 = 700
    window_y_2 = 500
    ch_new_wd.minsize(window_x_2, window_y_2)
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


def ch_edt_delete():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ch_edt_ch_name = ch_edt_ch_name_id_var.get()

    # Get ch_id with ch_name
    c.execute(f"""SELECT ch_id FROM characters WHERE ch_name = '{ch_edt_ch_name}'""")
    ch_edt_ch_id_raw = c.fetchall()
    ch_edt_ch_id = str(id.raw_conv(ch_edt_ch_id_raw)[0])

    # Get s_id with ch_id
    c.execute(f"""SELECT s_id FROM stories WHERE ch_id = '{ch_edt_ch_id}'""")
    ch_edt_s_id_raw = c.fetchall()
    ch_edt_s_id = id.raw_conv(ch_edt_s_id_raw)

    # Make a string of it only if an actual s_id connected to this character exists
    if ch_edt_s_id:
        ch_edt_s_id = str(id.raw_conv(ch_edt_s_id_raw)[0])
    else:
        ch_edt_s_id = '/'

    s_del_warning = messagebox.askquestion('Confirm Deletion',
                                           f"Are you sure you want to delete Character called '{ch_edt_ch_name}'?\nEVERYTHING CONNECTED TO THIS CHARACTER WILL BE DELETED!",
                                           icon='warning')

    if s_del_warning == 'yes':
        if ch_edt_s_id == '/':
            c.execute(f"""DELETE FROM characters WHERE ch_id = '{ch_edt_ch_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Character Number {id.id_int(ch_edt_ch_id)} has been successfully deleted.")
        else:
            c.execute(f"""DELETE FROM characters WHERE ch_id = '{ch_edt_ch_id}'""")
            c.execute(f"""DELETE FROM stories WHERE s_id = '{ch_edt_s_id}'""")
            c.execute(f"""DELETE FROM initial_paragraphs WHERE s_id = '{ch_edt_s_id}'""")
            c.execute(f"""DELETE FROM paragraphs_list WHERE s_id = '{ch_edt_s_id}'""")
            c.execute(f"""DELETE FROM choices WHERE s_id = '{ch_edt_s_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Character Number {id.id_int(ch_edt_ch_id)} has been successfully deleted.\nAll Stories, Paragraphs And Choices From Story Number {id.id_int(ch_edt_s_id)} Have Also Been Deleted.")

        conn.commit()

        # Delete Previous Input
        ch_edt_name_entry.delete(0, END)
        ch_edt_breed_entry.delete(0, END)
        ch_edt_life_entry.delete(0, END)
        ch_edt_speed_entry.delete(0, END)
        ch_edt_defense_entry.delete(0, END)
        ch_edt_attack_entry.delete(0, END)
        ch_edt_background_text_entry.delete("1.0", "end")

        ch_edt_ch_name_opt_menu()




def ch_edt_insert():
    # Delete Previous Input
    ch_edt_name_entry.delete(0, END)
    ch_edt_breed_entry.delete(0, END)
    ch_edt_life_entry.delete(0, END)
    ch_edt_speed_entry.delete(0, END)
    ch_edt_defense_entry.delete(0, END)
    ch_edt_attack_entry.delete(0, END)
    ch_edt_background_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ch_edt_ch_name = ch_edt_ch_name_id_var.get()

    c.execute(f"""SELECT * FROM characters WHERE ch_name = '{ch_edt_ch_name}'""")
    ch_edt_info_list_raw = c.fetchall()
    ch_edt_info_list = id.raw_conv(ch_edt_info_list_raw)

    # Input data into text box
    ch_edt_name_entry.insert(END, f'{ch_edt_info_list[1]}')
    ch_edt_breed_entry.insert(END, f'{ch_edt_info_list[2]}')
    ch_edt_life_entry.insert(END, f'{ch_edt_info_list[3]}')
    ch_edt_speed_entry.insert(END, f'{ch_edt_info_list[4]}')
    ch_edt_defense_entry.insert(END, f'{ch_edt_info_list[5]}')
    ch_edt_attack_entry.insert(END, f'{ch_edt_info_list[6]}')
    ch_edt_background_text_entry.insert(END, f"{ch_edt_info_list[7]}")

    conn.commit()


def ch_edt_edit():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ch_edt_ch_name = ch_edt_ch_name_id_var.get()

    edt_ch_name = ch_edt_name_entry.get()
    edt_ch_breed = ch_edt_breed_entry.get()
    edt_ch_life = ch_edt_life_entry.get()
    edt_ch_speed = ch_edt_speed_entry.get()
    edt_ch_attack = ch_edt_attack_entry.get()
    edt_ch_defense = ch_edt_defense_entry.get()
    edt_ch_background = ch_edt_background_text_entry.get('1.0', 'end')
    try:
        edt_ch_life = int(edt_ch_life)
        edt_ch_speed = int(edt_ch_speed)
        edt_ch_attack = int(edt_ch_attack)
        edt_ch_defense = int(edt_ch_defense)

        if edt_ch_name and edt_ch_breed and edt_ch_life and edt_ch_speed and edt_ch_attack and edt_ch_defense \
                and edt_ch_background != '' \
                and len(ch_edt_background_text_entry.get("1.0", "end")) != 1:
            c.execute(f"""UPDATE characters SET
                ch_name = :ch_name,
                ch_breed = :ch_breed,
                ch_life = :ch_life,
                ch_speed = :ch_speed,
                ch_attack = :ch_attack,
                ch_defense = :ch_defense,
                ch_background = :ch_background 
    
                WHERE ch_name ='{ch_edt_ch_name}'""",
                      {"ch_name": f'{edt_ch_name}',
                          "ch_breed": f'{edt_ch_breed}',
                          "ch_life": f'{edt_ch_life}',
                          "ch_speed": f'{edt_ch_speed}',
                          "ch_attack": f'{edt_ch_attack}',
                          "ch_defense": f'{edt_ch_defense}',
                          "ch_background": f'{edt_ch_background}'})
            messagebox.showinfo("Success",
                                f"Character '{ch_edt_ch_name}' has been successfully modified.")
            # Clear the Text Boxes
            ch_edt_name_entry.delete(0, END)
            ch_edt_breed_entry.delete(0, END)
            ch_edt_life_entry.delete(0, END)
            ch_edt_speed_entry.delete(0, END)
            ch_edt_defense_entry.delete(0, END)
            ch_edt_attack_entry.delete(0, END)
            ch_edt_background_text_entry.delete("1.0", "end")

        else:
            messagebox.showerror("Input Error", f'One Of The Inputs Are Empty', icon='warning')
    except ValueError:
        messagebox.showerror("Input Error", f'One Of The Stats Are Not a Number', icon='warning')

    conn.commit()

    ch_edt_ch_name_opt_menu()


def ch_edt_window():
    global ch_edt_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    ch_edt_wd = Toplevel()
    ch_edt_wd.title("Edit A Character")
    screen_x_2 = ch_edt_wd.winfo_screenwidth()
    screen_y_2 = ch_edt_wd.winfo_screenheight()
    window_x_2 = 600
    window_y_2 = 600
    ch_edt_wd.minsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    ch_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    ch_edt_frame_height = 200
    ch_edt_rest = window_y_2 - ch_edt_frame_height * 2
    # Info Frame 0
    ch_edt_info_frame_0 = LabelFrame(ch_edt_wd, width=window_x_2, height=ch_edt_frame_height)
    ch_edt_info_frame_0.pack(fill="both", side=TOP)

    # Info Frame 1
    ch_edt_info_frame_1 = LabelFrame(ch_edt_wd, width=window_x_2, height=ch_edt_frame_height)
    ch_edt_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    ch_edt_info_frame_2 = LabelFrame(ch_edt_wd, width=window_x_2, height=ch_edt_frame_height)
    ch_edt_info_frame_2.pack(fill="both", side=TOP)

    # Button Frame
    ch_edt_button_frame = LabelFrame(ch_edt_wd, height=ch_edt_rest / 2, width=window_x_2)
    ch_edt_button_frame.pack(fill="both")

    ch_edt_width = 42
    ch_edt_pad = 10
    ch_edt_entry_width = 49
    ch_edt_text_width = 37

    # Labels
    ch_edt_select_ch_label = Label(ch_edt_info_frame_0, text="Select Character:", width=int(ch_edt_width / 2), anchor=W)
    ch_edt_select_ch_label.grid(row=0, column=0, padx=(ch_edt_pad, ch_edt_pad-3), pady=ch_edt_pad, stick="w")

    ch_edt_name_label = Label(ch_edt_info_frame_1, text="Name:", width=int(ch_edt_width / 2), anchor=W)
    ch_edt_name_label.grid(row=0, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="w")

    ch_edt_breed_label = Label(ch_edt_info_frame_1, text="Breed:", width=int(ch_edt_width / 2),
                                      anchor=W)
    ch_edt_breed_label.grid(row=1, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="w")

    ch_edt_life_label = Label(ch_edt_info_frame_1, text="Life:", width=int(ch_edt_width / 2), anchor=NW)
    ch_edt_life_label.grid(row=2, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_speed_label = Label(ch_edt_info_frame_1, text="Speed:", width=int(ch_edt_width / 2), anchor=NW)
    ch_edt_speed_label.grid(row=3, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_attack_label = Label(ch_edt_info_frame_1, text="Attack:", width=int(ch_edt_width / 2),
                                       anchor=NW)
    ch_edt_attack_label.grid(row=4, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_defense_label = Label(ch_edt_info_frame_1, text="Defense:", width=int(ch_edt_width / 2),
                                anchor=NW)
    ch_edt_defense_label.grid(row=5, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_background_label = Label(ch_edt_info_frame_2, text="Background:", width=int(ch_edt_width / 2),
                                anchor=NW)
    ch_edt_background_label.grid(row=0, column=0, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    # Short Entries
    global ch_edt_name_entry_var, ch_edt_breed_entry_var, ch_edt_life_entry_var, ch_edt_speed_entry_var, ch_edt_attack_entry_var, ch_edt_defense_entry_var, ch_edt_background_text_entry
    global ch_edt_name_entry, ch_edt_breed_entry, ch_edt_life_entry, ch_edt_speed_entry, ch_edt_attack_entry, ch_edt_defense_entry
    ch_edt_name_entry_var = StringVar()
    ch_edt_name_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_name_entry_var, width=ch_edt_entry_width)
    ch_edt_name_entry.grid(row=0, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_breed_entry_var = StringVar()
    ch_edt_breed_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_breed_entry_var, width=ch_edt_entry_width)
    ch_edt_breed_entry.grid(row=1, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_life_entry_var = StringVar()
    ch_edt_life_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_life_entry_var, width=ch_edt_entry_width)
    ch_edt_life_entry.grid(row=2, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_speed_entry_var = StringVar()
    ch_edt_speed_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_speed_entry_var, width=ch_edt_entry_width)
    ch_edt_speed_entry.grid(row=3, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_attack_entry_var = StringVar()
    ch_edt_attack_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_attack_entry_var, width=ch_edt_entry_width)
    ch_edt_attack_entry.grid(row=4, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    ch_edt_defense_entry_var = StringVar()
    ch_edt_defense_entry = Entry(ch_edt_info_frame_1, textvariable=ch_edt_defense_entry_var, width=ch_edt_entry_width)
    ch_edt_defense_entry.grid(row=5, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="nw")

    # Text Entry
    ch_edt_background_text_entry = Text(ch_edt_info_frame_2, width=ch_edt_text_width, height=7)
    ch_edt_background_text_entry.grid(row=0, column=1, padx=ch_edt_pad, pady=ch_edt_pad)

    # Buttons
    ch_edt_width_buttons = 13
    ch_edt_save_changes_button = Button(ch_edt_button_frame, text="Save Changes", width=ch_edt_width_buttons,
                                      command=ch_edt_edit)
    ch_edt_save_changes_button.grid(row=0, column=0, padx=(ch_edt_pad + 9, ch_edt_pad), pady=ch_edt_pad, stick="w")

    ch_edt_load_character_button = Button(ch_edt_button_frame, text="Load Character", width=ch_edt_width_buttons,
                                          command=ch_edt_insert)
    ch_edt_load_character_button.grid(row=0, column=1, padx=ch_edt_pad, pady=ch_edt_pad, stick="w")

    ch_edt_delete_character_button = Button(ch_edt_button_frame, text="Delete Character", width=ch_edt_width_buttons,
                                       command=ch_edt_delete)
    ch_edt_delete_character_button.grid(row=0, column=2, padx=ch_edt_pad, pady=ch_edt_pad, stick="w")

    ch_edt_cancel_button = Button(ch_edt_button_frame, text="Cancel", width=ch_edt_width_buttons,
                                  command=ch_edt_wd.destroy)
    ch_edt_cancel_button.grid(row=0, column=3, padx=ch_edt_pad, pady=ch_edt_pad, stick="w")

    global ch_edt_ch_name_opt_menu

    def ch_edt_ch_name_opt_menu():
        # Options Menu For all existing Character Names
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT ch_name FROM characters""")
        ch_new_ch_name_id_ist_raw = c.fetchall()
        ch_new_ch_name_id_list = id.raw_conv(ch_new_ch_name_id_ist_raw)

        if ch_new_ch_name_id_list:
            global ch_edt_ch_name_id_var
            ch_edt_ch_name_id_var = StringVar()
            ch_edt_ch_name_id_var.set(ch_new_ch_name_id_list[0])
            ch_edt_ch_name_id_opt_menu_var = OptionMenu(ch_edt_info_frame_0, ch_edt_ch_name_id_var, *ch_new_ch_name_id_list)
            ch_edt_ch_name_id_opt_menu_var.config(width=ch_edt_width+1)
            ch_edt_ch_name_id_opt_menu_var.grid(row=0, column=1, pady=ch_edt_pad, padx=ch_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Characters were Found")
            ch_edt_wd.destroy()

        conn.commit()

    ch_edt_ch_name_opt_menu()

    ch_edt_wd.mainloop()


