# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import widget_func
import story_buttons_func
import paragraph_buttons_func


# Class to set tab number in new_tab function
class NewTab(Frame):
    def __init__(self, root, name):
        Frame.__init__(self, root)

        self.root = root
        self.name = name


# Function to print all created stories as tabs
def new_tab():
    # Delete previous paragraphs in the frame
    for widgets in main_story_frame.winfo_children():
        widgets.destroy()

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS stories 
                                    (s_id text,
                                    s_text text)""")

    c.execute(f"SELECT s_id FROM stories")
    story_id_list_raw = c.fetchall()
    story_id_list = []
    for tp in story_id_list_raw:
        for item in tp:
            story_id_list.append(item)

    notebook = ttk.Notebook(main_story_frame, width=left_frame_width, height=window_y - main_frame_height)

    tab_id_dict = {}
    tab_id_list = []

    for s_id in story_id_list:
        # Tab Control
        tab_name = f"Story {s_id}"

        tab_id = NewTab(notebook, tab_name)

        # Save the TAB variables in a list
        tab_id_list.append(tab_id)

        # Save the TAB variables in a dict
        tab_id_dict["tab_id_" + str(s_id)] = tab_id

        # Adding Tab
        notebook.add(tab_id, text=f"Story {s_id}")

        # Position
        notebook.pack(side=TOP)

    conn.commit()
    conn.close()


# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
window_x = editor.winfo_screenwidth()
window_y = editor.winfo_screenheight()

editor.geometry(f"{window_x}x{window_y}")

# Adding the Menus
main_menu = tkinter.Menu(editor)

file_menu = tkinter.Menu(main_menu, tearoff=0)
file_menu.add_command(label="New Game Editor")
file_menu.add_command(label="Load Game Editor")
file_menu.add_command(label="Save Game Editor")

options_menu = tkinter.Menu(main_menu, tearoff=0)
options_menu.add_command(label="Change Paragraph Order")
options_menu.add_command(label="Dark Mode")
options_menu.add_command(label="Refresh", command=new_tab)
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
# ALL MAIN FRAMES

# Left Frame
left_frame_width = int(0.75*window_x)
left_frame = LabelFrame(paragraphs_tab, width=left_frame_width, height=window_y)
left_frame.pack(fill="both", expand=True, side=LEFT)

# List Frame
right_frame = LabelFrame(paragraphs_tab, width=window_x - left_frame_width, height=window_y)
right_frame.pack(fill="both", side=RIGHT)

# Main Buttons Frame
main_frame_height = int(window_y/4.8)
main_buttons_frame = LabelFrame(left_frame, height=main_frame_height, width=left_frame_width)
main_buttons_frame.pack(fill="both")

# Story Buttons Frame
sub_frame_width = int(left_frame_width/4)
story_buttons_frame = LabelFrame(main_buttons_frame, height=main_frame_height, width=sub_frame_width)
story_buttons_frame.pack(fill="both", side=LEFT)

# Initial Paragraphs Buttons Frame
int_paragraph_buttons_frame = LabelFrame(main_buttons_frame, height=main_frame_height, width=sub_frame_width)
int_paragraph_buttons_frame.pack(fill="both", side=LEFT)

# Paragraphs Buttons Frame
paragraphs_buttons_frame = LabelFrame(main_buttons_frame, height=main_frame_height, width=sub_frame_width)
paragraphs_buttons_frame.pack(fill="both", side=LEFT)

# Choices Buttons Frame
choices_buttons_frame = LabelFrame(main_buttons_frame, height=main_frame_height, width=sub_frame_width)
choices_buttons_frame.pack(fill="both", side=LEFT)

# Story Frame
main_story_frame = LabelFrame(left_frame, height=window_x - main_frame_height)
main_story_frame.pack(fill="both", expand=True)

# Update Tabs Automatically
new_tab()

button_width = 22
buttons_width = 30
buttons_height = 1
button_x_space = 2
button_y_space = 4
font_size = 18
# NEW STORY Button
new_story_button = Button(story_buttons_frame, text="New Story", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=story_buttons_func.new_story_window)
new_story_button.grid(row=0, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# EDIT STORY  Button
edit_story_button = Button(story_buttons_frame, text="Edit Story", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=story_buttons_func.edit_story_window)
edit_story_button.grid(row=1, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# DELETE STORY Button
delete_story_button = Button(story_buttons_frame, text="Delete Story", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=story_buttons_func.delete_story_window)
delete_story_button.grid(row=2, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# ADD INITIAL PARAGRAPH Button
new_int_par_button = Button(int_paragraph_buttons_frame, text="New Initial Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=paragraph_buttons_func.int_paragraph_window)
new_int_par_button.grid(row=0, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# EDIT INITIAL PARAGRAPH  Button
edit_int_par_button = Button(int_paragraph_buttons_frame, text="Edit Initial Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
edit_int_par_button.grid(row=1, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# DELETE INITIAL PARAGRAPH Button
delete_int_par_button = Button(int_paragraph_buttons_frame, text="Delete Initial Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
delete_int_par_button.grid(row=2, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# NEW PARAGRAPH Button
new_paragraph_button = Button(paragraphs_buttons_frame, text="New Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
new_paragraph_button.grid(row=0, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# EDIT PARAGRAPH  Button
edit_paragraph_button = Button(paragraphs_buttons_frame, text="Edit Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
edit_paragraph_button.grid(row=1, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# DELETE PARAGRAPH Button
delete_paragraph_button = Button(paragraphs_buttons_frame, text="Delete Paragraph", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
delete_paragraph_button.grid(row=2, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# ADD CHOICE Button
new_choice_button = Button(choices_buttons_frame, text="New Choice", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
new_choice_button.grid(row=0, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# EDIT CHOICE  Button
edit_choice_button = Button(choices_buttons_frame, text="Edit Choice", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
edit_choice_button.grid(row=1, column=0, stick="w", padx=button_x_space, pady=button_y_space)

# DELETE CHOICE Button
delete_choice_button = Button(choices_buttons_frame, text="Delete Choice", bg="#5fafde", fg="White", padx=buttons_width, pady=buttons_height, font=("Times New Roman", font_size), relief=FLAT, width=button_width, command=None)
delete_choice_button.grid(row=2, column=0, stick="w", padx=button_x_space, pady=button_y_space)


# -------------------------------------------
# LOOP END
# -------------------------------------------

editor.config(menu=main_menu)
editor.mainloop()
