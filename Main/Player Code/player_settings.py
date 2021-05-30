# All necessary imports
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import sys
import os

database_module = sys.modules[__name__]

# Database For The Player To Load
database_module.database = None


def new_save():
    global database
    database = database_module.database
    # get path of editor_settings location
    path = os.path.dirname(__file__)

    # Pop-up window to choose where to save
    db_name_dir = filedialog.asksaveasfilename(initialdir=f"{path}/databases", title="Select File Name",
                                               defaultextension=".db", filetypes=[("database files", "*.db")])

    # Create backup with selected name from memory
    conn = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    backup = sqlite3.connect(f'file:{db_name_dir}', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    with backup:
        conn.backup(backup)
    backup.close()
    conn.close()

    # Get file name
    db_name = os.path.basename(db_name_dir)

    if db_name_dir != '':
        messagebox.showinfo("Save Editor", f"Success, New Editor Save '{db_name}' Has Been Created.")

    # Change The WHOLE data base
    database_module.database = f'{db_name_dir}'


def load_story():
    path = os.path.dirname(__file__)

    db_name_dir = filedialog.askopenfilename(initialdir=f"{path}/Saved Games", title="Select File Name",
                                             defaultextension=".db", filetypes=[("database files", "*.db")])

    db_name = os.path.basename(db_name_dir)

    if db_name_dir != '':
        messagebox.showinfo("Load Editor", f"Success, Editor Save '{db_name}' Has Been Loaded.")

    # Set Database To Loaded database
    database_module.database = f'{db_name_dir}'
