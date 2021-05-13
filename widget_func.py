# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3

# .py files import
import story_buttons_func


# Function to create new tabs
def new_tab(root, id):
    # Tab Control
    tabcontrol = ttk.Notebook(root)

    # Creating Tabs
    story_tab = ttk.Frame(tabcontrol)

    # Adding Tab
    tabcontrol.add(main_story_frame, text=f"Story {id}")

    # Position
    tabcontrol.grid(row=0, column=id)