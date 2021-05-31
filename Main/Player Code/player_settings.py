# All necessary imports
from tkinter import messagebox
from tkinter import filedialog
import sqlite3
import sys
import os
import shutil

database_module = sys.modules[__name__]

progress_module = sys.modules[__name__]

inventory_module = sys.modules[__name__]

# Database For The Player To Load
database_module.database = None

# Initial Progress List
progress_module.progress_list = []

# Initial Inventory List
inventory_module.inventory_list = ['check']


def load_position():
    global database, inventory_list, progress_list
    database = database_module.database
    inventory_list = inventory_module.inventory_list
    progress_list = progress_module.progress_list

    path = os.path.dirname(__file__)

    folder_name_raw = database.split('/')[-1]
    folder_name = folder_name_raw.split('.')

    directory = f"{path}/Saved Games/{folder_name[0]}_saves"

    file_name_dir = filedialog.askopenfilename(initialdir=f"{directory}", title="Select Save Name", defaultextension=".txt", filetypes=[("text files", "*.txt")])

    if file_name_dir:
        file_name = file_name_dir.split('/')[-1]

        save_game_file = open(file_name_dir, 'r')
        save_game_info_raw = save_game_file.read()
        save_game_info = save_game_info_raw.split('###')

        database = save_game_info[0]
        progress_list = save_game_info[1].split('#')
        inventory_list = save_game_info[2].split('#')
        inventory_list.remove('')

        messagebox.showinfo("Load Editor", f"Success, Editor Save '{file_name}' In Player Story {folder_name[0]} Has Been Loaded.")


def save_position():
    global database
    database = database_module.database

    try:
        folder_name_raw = database.split('/')[-1]
        folder_name = folder_name_raw.split('.')

        directory = f"{folder_name[0]}_saves"
        path = os.path.dirname(__file__)

        file_name_dir = filedialog.asksaveasfilename(initialdir=f"{path}/Saved Games/{directory}",
                                                     title="Select File Name", defaultextension=".txt",
                                                     initialfile="save1", filetypes=[("text files", "*.txt")])

        temporary_save_location = f'{path}/Saved Games/temporary_save.txt'
        save_location = f'{file_name_dir}'

        if save_location:
            shutil.copyfile(temporary_save_location, save_location)

            messagebox.showinfo("New Save", f"Success, New Save For Story {folder_name[0]} Has Been Created.")
        else:
            pass

    except AttributeError:
        pass


def load_story():
    path = os.path.dirname(__file__)

    db_name_dir = filedialog.askopenfilename(initialdir=f"{path}/Saved Games", title="Select File Name",
                                             defaultextension=".db", filetypes=[("database files", "*.db")])

    db_name = os.path.basename(db_name_dir)

    if db_name_dir != '':
        messagebox.showinfo("Load Editor", f"Success, Editor Save '{db_name}' Has Been Loaded.")

    # Set Database To Loaded database
    database_module.database = f'{db_name_dir}'

    try:
        if not db_name == '':
            # Create A Dedicated game saves folder for the database
            folder_name = db_name.split('.')

            # Directory
            directory = f"{folder_name[0]}_saves"

            # Parent Directory path
            parent_dir = f"{path}/Saved Games"

            # Path
            path = os.path.join(parent_dir, directory)

            # Create the directory
            os.mkdir(path)
        else:
            messagebox.showerror("Error", "Operation Was Canceled")
    except FileExistsError:
        pass
