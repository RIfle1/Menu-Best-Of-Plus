# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import sys

database_module = sys.modules[__name__]

database_module.database = 'file:my_db?mode=memory&cache=shared'


def create_save():
    global database
    file_name = main_input_name_entry_var.get()

    conn = sqlite3.connect('file:my_db?mode=memory&cache=shared', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    backup = sqlite3.connect(f'file:{file_name}.db', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    with backup:
        conn.backup(backup)
    backup.close()
    conn.close()

    messagebox.showinfo("New Editor Save", f"Success, New Editor Save '{file_name}' Has Been Created")
    main_new_save_wd.destroy()

    database_module.database = f'{file_name}.db'
    print(database_module.database)


def new_save():
    # Create New Window
    global main_new_save_wd
    main_new_save_wd = Toplevel()
    main_new_save_wd.title("Create a New Editor Save")
    screen_x_2 = main_new_save_wd.winfo_screenwidth()
    screen_y_2 = main_new_save_wd.winfo_screenheight()
    window_x_2 = 400
    window_y_2 = 90
    main_new_save_wd.minsize(window_x_2, window_y_2)
    main_new_save_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    main_new_save_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    main_new_pad = 10
    main_new_width = 21
    main_new_entry_width = 33

    main_input_save_name_label = Label(main_new_save_wd, text="Editor Save Name:", width=main_new_width, anchor=W)
    main_input_save_name_label.grid(row=0, column=0, padx=main_new_pad, pady=main_new_pad, stick="w")

    global main_input_name_entry_var
    main_input_name_entry_var = StringVar()
    main_input_name_entry = Entry(main_new_save_wd, textvariable=main_input_name_entry_var, width=main_new_entry_width)
    main_input_name_entry.grid(row=0, column=1, padx=main_new_pad, pady=main_new_pad, stick="nw")

    npc_edt_load_npc_button = Button(main_new_save_wd, text="Create New Save", width=main_new_width,
                                     command=create_save)
    npc_edt_load_npc_button.grid(row=1, column=0, padx=main_new_pad, pady=main_new_pad, stick="w")





