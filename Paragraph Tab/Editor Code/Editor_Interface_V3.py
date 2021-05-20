# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import story_button_func
import initial_paragraph_buttons_func
import paragraph_buttons_func
import choice_buttons_func
import character_buttons_func
import npc_buttons_func
import id


database = "EditorDataV3.db"


# Function to create ALL necessary tables in the database
def tables():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS stories 
    (s_id text, 
    s_text text,
    ch_id text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS initial_paragraphs
        (s_id text, 
        ip_id text,
        ip_text text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs_list
            (s_id text,
            pl_id text,
            p_text text,
            npc_id text,
            mst_id text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS choices
        (s_id text,
        ip_id text,
        c_id text,
        c_text text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS characters
                 (ch_id text,
                 ch_name text, 
                 ch_breed text,
                 ch_life integer,
                 ch_speed integer,
                 ch_defense integer,
                 ch_attack integer,
                 ch_background text)""")
    c.execute("""CREATE TABLE IF NOT EXISTS npcs
                 (npc_id text,
                 npc_name text)""")
    conn.commit()
    conn.close()


tables()


# Class to set tab number in new_tab function
class NewTab(Frame):
    def __init__(self, root, name):
        Frame.__init__(self, root)

        self.root = root
        self.name = name


# Function to print all created stories as tabs
def new_tab():
    # Delete previous paragraphs in the frame
    for widgets in pg_main_story_frame.winfo_children():
        widgets.destroy()

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(f"SELECT s_id FROM stories")
    story_id_list_raw = c.fetchall()
    story_id_list = []
    for tp in story_id_list_raw:
        for item in tp:
            story_id_list.append(item)

    notebook = ttk.Notebook(pg_main_story_frame, width=pg_left_frame_width, height=window_y - pg_main_frame_height)

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
        notebook.add(tab_id, text=f"Story {id.id_int(s_id)}")

        # Position
        notebook.pack(side=TOP)

    conn.commit()
    conn.close()


# Main App
editor = Tk()
editor.title("Game Editor")

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
npc_tab = ttk.Frame(tabControl)
mst_tab = ttk.Frame(tabControl)
objects_tab = ttk.Frame(tabControl)
game_settings_tab = ttk.Frame(tabControl)
test_tab = ttk.Frame(tabControl)

# Adding Tabs
tabControl.add(paragraphs_tab, text="Paragraphs")
tabControl.add(characters_tab, text="Characters")
tabControl.add(npc_tab, text="Npc's")
tabControl.add(mst_tab, text="Monsters / Enemies")
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
pg_left_frame_width = int(0.75 * window_x)
pg_left_frame = LabelFrame(paragraphs_tab, width=pg_left_frame_width, height=window_y)
pg_left_frame.pack(fill="both", expand=True, side=LEFT)

# List Frame
pg_right_frame = LabelFrame(paragraphs_tab, width=window_x - pg_left_frame_width, height=window_y)
pg_right_frame.pack(fill="both", side=RIGHT)

# Main Buttons Frame
pg_main_frame_height = int(window_y / 4.8)
pg_main_buttons_frame = LabelFrame(pg_left_frame, height=pg_main_frame_height, width=pg_left_frame_width)
pg_main_buttons_frame.pack(fill="both")

# Story Buttons Frame
pg_sub_frame_width = int(pg_left_frame_width / 4)
pg_story_buttons_frame = LabelFrame(pg_main_buttons_frame, height=pg_main_frame_height, width=pg_sub_frame_width)
pg_story_buttons_frame.pack(fill="both", side=LEFT)

# Initial Paragraphs Buttons Frame
pg_int_paragraph_buttons_frame = LabelFrame(pg_main_buttons_frame, height=pg_main_frame_height, width=pg_sub_frame_width)
pg_int_paragraph_buttons_frame.pack(fill="both", side=LEFT)

# Paragraphs Buttons Frame
pg_paragraphs_buttons_frame = LabelFrame(pg_main_buttons_frame, height=pg_main_frame_height, width=pg_sub_frame_width)
pg_paragraphs_buttons_frame.pack(fill="both", side=LEFT)

# Choices Buttons Frame
pg_choices_buttons_frame = LabelFrame(pg_main_buttons_frame, height=pg_main_frame_height, width=pg_sub_frame_width)
pg_choices_buttons_frame.pack(fill="both", side=LEFT)

# Story Frame
pg_main_story_frame = LabelFrame(pg_left_frame, height=window_x - pg_main_frame_height)
pg_main_story_frame.pack(fill="both", expand=True)

# Update Tabs Automatically
new_tab()

pg_button_width = 22
pg_buttons_width = 30
pg_buttons_height = 1
pg_button_x_space = 2
pg_button_y_space = 4
pg_font_size = 18
# NEW STORY Button
pg_new_story_button = Button(pg_story_buttons_frame, text="New Story", bg="#5fafde", fg="White", padx=pg_buttons_width,
                             pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT, width=pg_button_width,
                             command=story_button_func.s_new_window)
pg_new_story_button.grid(row=0, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# EDIT STORY  Button
pg_edit_story_button = Button(pg_story_buttons_frame, text="Edit Story", bg="#5fafde", fg="White", padx=pg_buttons_width,
                              pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT, width=pg_button_width,
                              command=story_button_func.s_edt_window)
pg_edit_story_button.grid(row=1, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# ADD INITIAL PARAGRAPH Button
pg_new_int_par_button = Button(pg_int_paragraph_buttons_frame, text="New Initial Paragraph", bg="#5fafde", fg="White",
                               padx=pg_buttons_width, pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT,
                               width=pg_button_width, command=initial_paragraph_buttons_func.ip_new_window)
pg_new_int_par_button.grid(row=0, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# EDIT INITIAL PARAGRAPH  Button
pg_edit_int_par_button = Button(pg_int_paragraph_buttons_frame, text="Edit Initial Paragraph", bg="#5fafde", fg="White",
                                padx=pg_buttons_width, pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT,
                                width=pg_button_width, command=initial_paragraph_buttons_func.ip_edt_window)
pg_edit_int_par_button.grid(row=1, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# NEW PARAGRAPH Button
pg_new_paragraph_button = Button(pg_paragraphs_buttons_frame, text="New Paragraph", bg="#5fafde", fg="White",
                                 padx=pg_buttons_width, pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT,
                                 width=pg_button_width, command=paragraph_buttons_func.p_new_window)
pg_new_paragraph_button.grid(row=0, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# EDIT PARAGRAPH  Button
edit_paragraph_button = Button(pg_paragraphs_buttons_frame, text="Edit Paragraph", bg="#5fafde", fg="White", padx=pg_buttons_width,
                               pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT, width=pg_button_width,
                               command=paragraph_buttons_func.p_edt_window)
edit_paragraph_button.grid(row=1, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# ADD CHOICE Button
new_choice_button = Button(pg_choices_buttons_frame, text="New Choice", bg="#5fafde", fg="White", padx=pg_buttons_width,
                           pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT, width=pg_button_width,
                           command=choice_buttons_func.c_new_window)
new_choice_button.grid(row=0, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# EDIT CHOICE  Button
edit_choice_button = Button(pg_choices_buttons_frame, text="Edit Choice", bg="#5fafde", fg="White", padx=pg_buttons_width,
                            pady=pg_buttons_height, font=("Times New Roman", pg_font_size), relief=FLAT, width=pg_button_width,
                            command=choice_buttons_func.c_edt_window)
edit_choice_button.grid(row=1, column=0, stick="w", padx=pg_button_x_space, pady=pg_button_y_space)

# -------------------------------------------
# THIS IS THE END OF THE "PARAGRAPH" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "CHARACTERS" TAB
# -------------------------------------------
# ALL MAIN FRAMES
# MAIN Frame
ch_left_frame_width = int(0.75 * window_x)
ch_main_frame = LabelFrame(characters_tab, width=ch_left_frame_width, height=window_y)
ch_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
ch_main_frame_height = int(window_y / 4.8)
ch_main_buttons_frame = LabelFrame(ch_main_frame, height=ch_main_frame_height, width=ch_left_frame_width)
ch_main_buttons_frame.pack(fill="both")

# Characters Frame
ch_main_characters_frame = LabelFrame(ch_main_frame, height=window_x - ch_main_frame_height)
ch_main_characters_frame.pack(fill="both", expand=True)

ch_button_width = 22
ch_buttons_width = 30
ch_buttons_height = 1
ch_button_x_space = 2
ch_button_y_space = 4
ch_font_size = 18
# NEW CHARACTER Button
ch_new_character_button = Button(ch_main_buttons_frame, text="New Character", bg="#5fafde", fg="White", padx=ch_buttons_width,
                                 pady=ch_buttons_height, font=("Times New Roman", ch_font_size), relief=FLAT, width=ch_button_width,
                                 command=character_buttons_func.ch_new_window)
ch_new_character_button.pack(padx=ch_button_x_space, pady=ch_button_y_space)

# EDIT CHARACTER Button
ch_edit_character_button = Button(ch_main_buttons_frame, text="Edit Character", bg="#5fafde", fg="White", padx=ch_buttons_width,
                                  pady=ch_buttons_height, font=("Times New Roman", ch_font_size), relief=FLAT, width=ch_button_width,
                                  command=character_buttons_func.ch_edt_window)
ch_edit_character_button.pack(padx=ch_button_x_space, pady=ch_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "CHARACTER" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "NPC" TAB
# -------------------------------------------
# ALL MAIN FRAMES
# MAIN Frame
npc_left_frame_width = int(0.75 * window_x)
npc_main_frame = LabelFrame(npc_tab, width=npc_left_frame_width, height=window_y)
npc_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
npc_main_frame_height = int(window_y / 4.8)
npc_main_buttons_frame = LabelFrame(npc_main_frame, height=npc_main_frame_height, width=npc_left_frame_width)
npc_main_buttons_frame.pack(fill="both")

# NPC Frame
npc_main_npc_frame = LabelFrame(npc_main_frame, height=window_x - npc_main_frame_height)
npc_main_npc_frame.pack(fill="both", expand=True)

npc_button_width = 22
npc_buttons_width = 30
npc_buttons_height = 1
npc_button_x_space = 2
npc_button_y_space = 4
npc_font_size = 18
# NEW NPC Button
npc_new_npc_button = Button(npc_main_buttons_frame, text="New NPC", bg="#5fafde", fg="White", padx=npc_buttons_width,
                            pady=npc_buttons_height, font=("Times New Roman", npc_font_size), relief=FLAT, width=npc_button_width,
                            command=npc_buttons_func.npc_new_window)
npc_new_npc_button.pack(padx=npc_button_x_space, pady=npc_button_y_space)

# EDIT NPC Button
npc_edit_npc_button = Button(npc_main_buttons_frame, text="Edit NPC", bg="#5fafde", fg="White", padx=npc_buttons_width,
                             pady=npc_buttons_height, font=("Times New Roman", npc_font_size), relief=FLAT, width=npc_button_width,
                             command=npc_buttons_func.npc_edt_window)
npc_edit_npc_button.pack(padx=npc_button_x_space, pady=npc_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "NPC" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "MONSTERS / ENEMIES" TAB
# -------------------------------------------
# ALL MAIN FRAMES
# MAIN Frame
mst_main_frame_width = int(0.75 * window_x)
mst_main_frame = LabelFrame(mst_tab, width=mst_main_frame_width, height=window_y)
mst_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
mst_main_frame_height = int(window_y / 4.8)
mst_main_buttons_frame = LabelFrame(mst_main_frame, height=mst_main_frame_height, width=mst_main_frame_width)
mst_main_buttons_frame.pack(fill="both")

# MONSTER / ENEMY Frame
mst_main_mst_frame = LabelFrame(mst_main_frame, height=window_x - mst_main_frame_height)
mst_main_mst_frame.pack(fill="both", expand=True)

mst_button_width = 22
mst_buttons_width = 30
mst_buttons_height = 1
mst_button_x_space = 2
mst_button_y_space = 4
mst_font_size = 18
# NEW MONSTER / ENEMY Button
mst_new_mst_button = Button(mst_main_buttons_frame, text="New Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                            pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                            command=None)
mst_new_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)

# EDIT MONSTER / ENEMY Button
mst_edit_mst_button = Button(mst_main_buttons_frame, text="Edit Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                             pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                             command=None)
mst_edit_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "MONSTERS / ENEMIES" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "OBJECTS / CONDITIONS" TAB
# -------------------------------------------
# ALL MAIN FRAMES
# MAIN Frame
obj_main_frame_width = int(0.75 * window_x)
obj_main_frame = LabelFrame(objects_tab, width=obj_main_frame_width, height=window_y)
obj_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
obj_main_frame_height = int(window_y / 4.8)
obj_main_buttons_frame = LabelFrame(obj_main_frame, height=obj_main_frame_height, width=obj_main_frame_width)
obj_main_buttons_frame.pack(fill="both")

# OBJECT Frame
obj_main_mst_frame = LabelFrame(obj_main_frame, height=window_x - obj_main_frame_height)
obj_main_mst_frame.pack(fill="both", expand=True)

obj_button_width = 22
obj_buttons_width = 30
obj_buttons_height = 1
obj_button_x_space = 2
obj_button_y_space = 4
obj_font_size = 18
# NEW OBJECT Button
obj_new_obj_button = Button(obj_main_buttons_frame, text="New Object", bg="#5fafde", fg="White", padx=obj_buttons_width,
                            pady=obj_buttons_height, font=("Times New Roman", obj_font_size), relief=FLAT, width=obj_button_width,
                            command=None)
obj_new_obj_button.pack(padx=obj_button_x_space, pady=obj_button_y_space)

# EDIT OBJECT Button
obj_edit_obj_button = Button(obj_main_buttons_frame, text="Edit Object / Set Conditions", bg="#5fafde", fg="White", padx=obj_buttons_width,
                             pady=obj_buttons_height, font=("Times New Roman", obj_font_size), relief=FLAT, width=obj_button_width,
                             command=None)
obj_edit_obj_button.pack(padx=obj_button_x_space, pady=obj_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "OBJECTS / CONDITIONS" TAB CODE
# -------------------------------------------
# -------------------------------------------
# LOOP END
# -------------------------------------------

editor.config(menu=main_menu)
editor.mainloop()
