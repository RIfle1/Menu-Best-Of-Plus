# All necessary imports
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import sys
import os

database_module = sys.modules[__name__]

# Memory Database (Temporary -> Deleted if not saved)
database_module.database0 = 'file:my_db?mode=memory&cache=shared'

# Database Used For Code Modifications
database_module.database = 'Editor.db'


def new_save():
    # get path of editor_settings location
    path = os.path.dirname(__file__)

    # Pop-up window to choose where to save
    db_name_dir = filedialog.asksaveasfilename(initialdir=f"{path}/databases", title="Select File Name",
                                               defaultextension=".db", filetypes=[("database files", "*.db")])

    # Create backup with selected name from memory
    conn = sqlite3.connect('file:my_db?mode=memory&cache=shared', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    backup = sqlite3.connect(f'file:{db_name_dir}', detect_types=sqlite3.PARSE_DECLTYPES, uri=True)
    with backup:
        conn.backup(backup)
    backup.close()
    conn.close()

    # Get file name
    db_name = os.path.basename(db_name_dir)

    if db_name_dir != '':
        messagebox.showinfo("Save Editor", f"Success, New Editor Save '{db_name}' Has Been Created.\n(Be sure to Refresh In Options)")

    # Change The WHOLE data base
    database_module.database = f'{db_name_dir}'


def load_save():
    path = os.path.dirname(__file__)

    db_name_dir = filedialog.askopenfilename(initialdir=f"{path}/databases", title="Select File Name",
                                             defaultextension=".db", filetypes=[("database files", "*.db")])

    db_name = os.path.basename(db_name_dir)

    if db_name_dir != '':
        messagebox.showinfo("Load Editor", f"Success, Editor Save '{db_name}' Has Been Loaded.\n(Be sure to Refresh In Options)")

    database_module.database = f'{db_name_dir}'


