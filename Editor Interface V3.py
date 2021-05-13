# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import widget_func
import buttons_func

# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
screen_x = editor.winfo_screenwidth()
screen_y = editor.winfo_screenheight()
window_x = 1920
window_y = 1080

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
# THIS FOLLOWING CODE IS FOR "PARAGRAPH" TAB
# -------------------------------------------

# Left Frame
left_frame_width = 1280
left_frame = LabelFrame(paragraphs_tab, width=left_frame_width, height=1080)
left_frame.pack(fill="both", expand=True, side=LEFT)

# List Frame
right_frame = LabelFrame(paragraphs_tab, width=1920 - left_frame_width, height=1080)
right_frame.pack(fill="both", side=RIGHT)

# Button Frame
button_frame_height = 140
main_buttons_frame = LabelFrame(left_frame, height=button_frame_height)
main_buttons_frame.pack(fill="both", expand=True)

# Story Frame
main_story_frame = LabelFrame(left_frame, height=1080 - button_frame_height)
main_story_frame.pack(fill="both", expand=True)

button_width = 25
# NEW STORY Button
new_story_button = Button(main_buttons_frame, text="New Story", bg="#5a951f", fg="White", padx=30, pady=10, font=("Montserrat", 18), relief=FLAT, width=button_width, command=buttons_func.new_story_window)
new_story_button.grid(row=0, column=0, stick="w", padx=(5, 0))

# EDIT STORY  Button
edit_story_button = Button(main_buttons_frame, text="Edit Story", bg="#e8c124", fg="White", padx=30, pady=10, font=("Montserrat", 18), relief=FLAT, width=button_width, command=buttons_func.edit_story_window)
edit_story_button.grid(row=0, column=1, stick="w", padx=(5, 0))

# DELETE STORY Button
delete_story_button = Button(main_buttons_frame, text="Delete Story", bg="#9E1A1A", fg="White", padx=30, pady=10, font=("Montserrat", 18), relief=FLAT, width=button_width, command=buttons_func.delete_story_window)
delete_story_button.grid(row=0, column=2, stick="w", padx=5)

# -------------------------------------------
# LOOP END
# -------------------------------------------

editor.config(menu=main_menu)
editor.mainloop()
