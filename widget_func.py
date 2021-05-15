# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3


# Function create an option menu
def option_menu_story(frame, window, height):
    # Options Menu For all existing stories
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c.execute("""SELECT s_id FROM stories""")
    s_id_list_raw = c.fetchall()
    s_id_list = []
    for tp in s_id_list_raw:
        for item in tp:
            s_id_list.append(item)

    if s_id_list:
        global s_id_variable
        s_id_variable = StringVar()
        s_id_variable.set(s_id_list[0])
        story_id_del_opmenu = OptionMenu(frame, s_id_variable, *s_id_list)
        story_id_del_opmenu.grid(row=0, column=1, ipadx=120, pady=height, stick="w")

    else:
        messagebox.showerror("Index Error", "No Existing Stories Found")
        window.destroy()

    conn.commit()
    conn.close()