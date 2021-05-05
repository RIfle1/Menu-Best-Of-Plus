# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font

# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
screen_x = editor.winfo_screenwidth()
screen_y = editor.winfo_screenheight()
window_x = 1200
window_y = 800

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


def new_text():
    text = tkinter.Text(paragraphs_tab, height=1, width=30, font=("Montserrat", 14), fg="#4285F4")
    text.pack()


create_paragraph_button = tkinter.Button(paragraphs_tab,
                                  text="New Paragraph",
                                  bd=0, bg="#3285F4",
                                  fg="White", padx=30, pady=10,
                                  font="Montserrat", relief=FLAT, command=None)
create_paragraph_button.pack()

del_paragraph_button = tkinter.Button(paragraphs_tab,
                                      text="Delete this paragraph",
                                      bd=0, bg="#C4C4C4", fg="White", padx=30,
                                      pady=10, font="Montserrat", relief=FLAT,
                                      state=DISABLED, command=None)
del_paragraph_button.pack()
   
    
# End
editor.config(menu=main_menu)
editor.mainloop()
