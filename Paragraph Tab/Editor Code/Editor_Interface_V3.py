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
import monster_enemy_buttons_func
import object_buttons_func
import error_buttons_func
import editor_settings
import id

database = editor_settings.database_module.database


# Functions That Refresh Button calls
def refresh():
    new_tab()
    errors_print()


# Function to print Errors
def errors_print():
    for widget in test_main_frame_2.winfo_children():
        widget.destroy()

    padding = 10
    errors_file = open("errors.txt", "r")
    text = errors_file.read()
    errors_list = text.split('###')

    row = 1
    column_frame = Frame(test_main_frame_2, height=100)
    column_frame.pack(fill="both", side=LEFT)

    for errors in errors_list[0:-1]:
        if row == 0 or row == 15:
            column_frame = Frame(test_main_frame_2, height=100)
            column_frame.pack(fill="both", side=LEFT)
            row = 0

        error_frame = LabelFrame(column_frame, height=100)
        error_frame.pack(fill="both")

        error_message = Message(error_frame, text=errors, width=400)
        error_message.grid(column=0, row=0, padx=padding, pady=(padding, 0), stick="w")
        row += 1


# Class to set tab number in new_tab function
class NewTab(Frame):
    def __init__(self, root, name):
        Frame.__init__(self, root)

        self.root = root
        self.name = name


# Function to print all created stories as tabs
def new_tab():
    global database
    database = editor_settings.database_module.database
    # Delete previous paragraphs in the frame
    for widgets in pg_main_story_frame.winfo_children():
        widgets.destroy()

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    c.execute(f"SELECT s_id FROM stories ORDER BY s_id")
    story_id_list_raw = c.fetchall()
    story_id_list = []
    for tp in story_id_list_raw:
        for item in tp:
            story_id_list.append(item)

    notebook = ttk.Notebook(pg_main_story_frame)

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

        # Scroll Bar stuff
        pg_main_frame_1 = Frame(tab_id)
        pg_main_frame_1.pack(fill="both", expand=True)

        # Create Canvas
        pg_canvas = Canvas(pg_main_frame_1)

        # Create ScrollBar
        pg_y_scrollbar = Scrollbar(pg_main_frame_1, orient="vertical", command=pg_canvas.yview)
        pg_y_scrollbar.pack(side="right", fill="y")
        pg_x_scrollbar = Scrollbar(pg_main_frame_1, orient="horizontal", command=pg_canvas.xview)
        pg_x_scrollbar.pack(side="bottom", fill="x")

        # Frame To Put Objects in
        pg_main_frame_2 = Frame(pg_canvas)
        pg_main_frame_2.bind("<Configure>", lambda e: pg_canvas.configure(scrollregion=pg_canvas.bbox("all")))

        # Canvas Config
        pg_canvas.create_window((0, 0), window=pg_main_frame_2, anchor="nw")
        pg_canvas.configure(yscrollcommand=pg_y_scrollbar.set)
        pg_canvas.configure(xscrollcommand=pg_x_scrollbar.set)
        pg_canvas.pack(side="left", fill="both", expand=True)

        # Add stuff here

        # Position
        notebook.pack(side=TOP, expand=True, fill="both")

    conn.commit()


# Function to create ALL necessary tables in the database
conn = sqlite3.connect(database, uri=True)
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
                                               mst_id text,
                                               npc_bool integer,
                                               mst_bool integer,
                                               obj_id text,
                                               end_bool integer)""")
c.execute("""CREATE TABLE IF NOT EXISTS choices
                                           (s_id text,
                                           ip_id text,
                                           c_id text,
                                           obj_id text,
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
c.execute("""CREATE TABLE IF NOT EXISTS monsters
                                                    (mst_id text,
                                                    mst_name text,
                                                    mst_type text)""")
c.execute("""CREATE TABLE IF NOT EXISTS objects
                                                        (obj_id text,
                                                        obj_name text)""")

conn.commit()


# Main App
editor = Tk()


def close_window():
    global database
    database = editor_settings.database_module.database
    if database == 'file:my_db?mode=memory&cache=shared':
        s_del_warning = messagebox.askquestion('Exit Without Saving?',
                                               f'Are you sure you want Exit Without Saving? All Unsaved Data Will Be Lost',
                                               icon='warning')
        if s_del_warning == 'no':
            editor_settings.new_save()
            editor.destroy()
        else:
            editor.destroy()
    else:
        editor.destroy()

    errors_file = open("errors.txt", "w")
    errors_file.truncate(0)
    errors_file.close()

editor.title("Game Editor")

window_x = editor.winfo_screenwidth()
window_y = editor.winfo_screenheight()
editor.geometry(f"{window_x}x{window_y}")

# Adding the Menus
main_menu = tkinter.Menu(editor)

file_menu = tkinter.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Load Game Editor", command=editor_settings.load_save)
file_menu.add_command(label="Save Game Editor", command=editor_settings.new_save)

options_menu = tkinter.Menu(main_menu, tearoff=0)
options_menu.add_command(label="Dark Mode")
options_menu.add_command(label="Refresh", command=refresh)
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
tabControl.add(test_tab, text="Test / Compile")

# Positioning the Tabs
tabControl.pack(expand=1, fill="both")

# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "PARAGRAPH" TAB
# -------------------------------------------
# ALL MAIN FRAMES

# Left Frame
pg_left_frame_width = int(0.65 * window_x)
pg_left_frame = Frame(paragraphs_tab)
pg_left_frame.pack(fill="both", side=LEFT)

# List Frame
pg_right_frame = LabelFrame(paragraphs_tab, height=window_y)
pg_right_frame.pack(fill="both", expand=True, side=RIGHT)

# Scroll Bar stuff
pg_2_main_frame_1 = Frame(pg_right_frame)
pg_2_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
pg_2_canvas = Canvas(pg_2_main_frame_1)

# Create ScrollBar
pg_2_y_scrollbar = Scrollbar(pg_2_main_frame_1, orient="vertical", command=pg_2_canvas.yview)
pg_2_y_scrollbar.pack(side="right", fill="y")
pg_2_x_scrollbar = Scrollbar(pg_2_main_frame_1, orient="horizontal", command=pg_2_canvas.xview)
pg_2_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
pg_2_main_frame_2 = Frame(pg_2_canvas)
pg_2_main_frame_2.bind("<Configure>", lambda e: pg_2_canvas.configure(scrollregion=pg_2_canvas.bbox("all")))

# Canvas Config
pg_2_canvas.create_window((0, 0), window=pg_2_main_frame_2, anchor="nw")
pg_2_canvas.configure(yscrollcommand=pg_2_y_scrollbar.set)
pg_2_canvas.configure(xscrollcommand=pg_2_x_scrollbar.set)
pg_2_canvas.pack(side="left", fill="both", expand=True)

# Main Buttons Frame
pg_main_buttons_frame = Frame(pg_left_frame)
pg_main_buttons_frame.pack(fill="both")

# Story Buttons Frame
pg_story_buttons_frame = Frame(pg_main_buttons_frame)
pg_story_buttons_frame.pack(fill="both", side=LEFT)

# Initial Paragraphs Buttons Frame
pg_int_paragraph_buttons_frame = Frame(pg_main_buttons_frame)
pg_int_paragraph_buttons_frame.pack(fill="both", side=LEFT)

# Paragraphs Buttons Frame
pg_paragraphs_buttons_frame = Frame(pg_main_buttons_frame)
pg_paragraphs_buttons_frame.pack(fill="both", side=LEFT)

# Choices Buttons Frame
pg_choices_buttons_frame = Frame(pg_main_buttons_frame)
pg_choices_buttons_frame.pack(fill="both", side=LEFT)

# Story Frame
pg_main_story_frame = LabelFrame(pg_left_frame)
pg_main_story_frame.pack(fill="both", expand=True)

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
ch_main_characters_frame = LabelFrame(ch_main_frame)
ch_main_characters_frame.pack(fill="both", expand=True)

# Scroll Bar stuff
ch_main_frame_1 = Frame(ch_main_characters_frame)
ch_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
ch_canvas = Canvas(ch_main_frame_1)

# Create ScrollBar
ch_y_scrollbar = Scrollbar(ch_main_frame_1, orient="vertical", command=ch_canvas.yview)
ch_y_scrollbar.pack(side="right", fill="y")
ch_x_scrollbar = Scrollbar(ch_main_frame_1, orient="horizontal", command=ch_canvas.xview)
ch_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
ch_main_frame_2 = Frame(ch_canvas)
ch_main_frame_2.bind("<Configure>", lambda e: ch_canvas.configure(scrollregion=ch_canvas.bbox("all")))

# Canvas Config
ch_canvas.create_window((0, 0), window=ch_main_frame_2, anchor="nw")
ch_canvas.configure(yscrollcommand=ch_y_scrollbar.set)
ch_canvas.configure(xscrollcommand=ch_x_scrollbar.set)
ch_canvas.pack(side="left", fill="both", expand=True)

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
npc_main_npc_frame = LabelFrame(npc_main_frame)
npc_main_npc_frame.pack(fill="both", expand=True)

# Scroll Bar stuff
npc_main_frame_1 = Frame(npc_main_npc_frame)
npc_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
npc_canvas = Canvas(npc_main_frame_1)

# Create ScrollBar
npc_y_scrollbar = Scrollbar(npc_main_frame_1, orient="vertical", command=npc_canvas.yview)
npc_y_scrollbar.pack(side="right", fill="y")
npc_x_scrollbar = Scrollbar(npc_main_frame_1, orient="horizontal", command=npc_canvas.xview)
npc_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
npc_main_frame_2 = Frame(npc_canvas)
npc_main_frame_2.bind("<Configure>", lambda e: npc_canvas.configure(scrollregion=npc_canvas.bbox("all")))

# Canvas Config
npc_canvas.create_window((0, 0), window=npc_main_frame_2, anchor="nw")
npc_canvas.configure(yscrollcommand=npc_y_scrollbar.set)
npc_canvas.configure(xscrollcommand=npc_x_scrollbar.set)
npc_canvas.pack(side="left", fill="both", expand=True)

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
mst_main_mst_frame = LabelFrame(mst_main_frame)
mst_main_mst_frame.pack(fill="both", expand=True)

# Scroll Bar stuff
mst_main_frame_1 = Frame(mst_main_mst_frame)
mst_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
mst_canvas = Canvas(mst_main_frame_1)

# Create ScrollBar
mst_y_scrollbar = Scrollbar(mst_main_frame_1, orient="vertical", command=mst_canvas.yview)
mst_y_scrollbar.pack(side="right", fill="y")
mst_x_scrollbar = Scrollbar(mst_main_frame_1, orient="horizontal", command=mst_canvas.xview)
mst_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
mst_main_frame_2 = Frame(mst_canvas)
mst_main_frame_2.bind("<Configure>", lambda e: mst_canvas.configure(scrollregion=mst_canvas.bbox("all")))

# Canvas Config
mst_canvas.create_window((0, 0), window=mst_main_frame_2, anchor="nw")
mst_canvas.configure(yscrollcommand=mst_y_scrollbar.set)
mst_canvas.configure(xscrollcommand=mst_x_scrollbar.set)
mst_canvas.pack(side="left", fill="both", expand=True)


mst_button_width = 22
mst_buttons_width = 30
mst_buttons_height = 1
mst_button_x_space = 2
mst_button_y_space = 4
mst_font_size = 18
# NEW MONSTER / ENEMY Button
mst_new_mst_button = Button(mst_main_buttons_frame, text="New Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                            pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                            command=monster_enemy_buttons_func.mst_new_window)
mst_new_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)

# EDIT MONSTER / ENEMY Button
mst_edit_mst_button = Button(mst_main_buttons_frame, text="Edit Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                             pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                             command=monster_enemy_buttons_func.mst_edt_window)
mst_edit_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "MONSTERS / ENEMIES" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "OBJECTS" TAB
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
obj_frame_0 = LabelFrame(obj_main_frame)
obj_frame_0.pack(fill="both", expand=True)

# Scroll Bar stuff
obj_main_frame_1 = Frame(obj_frame_0)
obj_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
obj_canvas = Canvas(obj_main_frame_1)

# Create ScrollBar
obj_y_scrollbar = Scrollbar(obj_main_frame_1, orient="vertical", command=obj_canvas.yview)
obj_y_scrollbar.pack(side="right", fill="y")
obj_x_scrollbar = Scrollbar(obj_main_frame_1, orient="horizontal", command=obj_canvas.xview)
obj_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
obj_main_frame_2 = Frame(obj_canvas)
obj_main_frame_2.bind("<Configure>", lambda e: obj_canvas.configure(scrollregion=obj_canvas.bbox("all")))

# Canvas Config
obj_canvas.create_window((0, 0), window=obj_main_frame_2, anchor="nw")
obj_canvas.configure(yscrollcommand=obj_y_scrollbar.set)
obj_canvas.configure(xscrollcommand=obj_x_scrollbar.set)
obj_canvas.pack(side="left", fill="both", expand=True)

obj_button_width = 22
obj_buttons_width = 30
obj_buttons_height = 1
obj_button_x_space = 2
obj_button_y_space = 4
obj_font_size = 18
# NEW OBJECT Button
obj_new_obj_button = Button(obj_main_buttons_frame, text="New Object", bg="#5fafde", fg="White", padx=obj_buttons_width,
                            pady=obj_buttons_height, font=("Times New Roman", obj_font_size), relief=FLAT, width=obj_button_width,
                            command=object_buttons_func.obj_new_window)
obj_new_obj_button.pack(padx=obj_button_x_space, pady=obj_button_y_space)

# EDIT OBJECT Button
obj_edit_obj_button = Button(obj_main_buttons_frame, text="Edit Object", bg="#5fafde", fg="White", padx=obj_buttons_width,
                             pady=obj_buttons_height, font=("Times New Roman", obj_font_size), relief=FLAT, width=obj_button_width,
                             command=object_buttons_func.obj_edt_window)
obj_edit_obj_button.pack(padx=obj_button_x_space, pady=obj_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "OBJECTS" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "TEST" TAB
# -------------------------------------------
# ALL MAIN FRAMES
# MAIN Frame
test_main_frame_width = int(0.75 * window_x)
test_main_frame = LabelFrame(test_tab, width=test_main_frame_width, height=window_y)
test_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
test_main_frame_height = int(window_y / 4.8)
test_main_buttons_frame = LabelFrame(test_main_frame, height=test_main_frame_height, width=test_main_frame_width)
test_main_buttons_frame.pack(fill="both")

# Errors Frame
test_main_frame_0 = LabelFrame(test_main_frame)
test_main_frame_0.pack(fill="both", expand=True)

# Scroll Bar stuff
test_main_frame_1 = Frame(test_main_frame_0)
test_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
test_canvas = Canvas(test_main_frame_1)

# Create ScrollBar
test_y_scrollbar = Scrollbar(test_main_frame_1, orient="vertical", command=test_canvas.yview)
test_y_scrollbar.pack(side="right", fill="y")
test_x_scrollbar = Scrollbar(test_main_frame_1, orient="horizontal", command=test_canvas.xview)
test_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
test_main_frame_2 = Frame(test_canvas)
test_main_frame_2.bind("<Configure>", lambda e: test_canvas.configure(scrollregion=test_canvas.bbox("all")))

# Canvas Config
test_canvas.create_window((0, 0), window=test_main_frame_2, anchor="nw")
test_canvas.configure(yscrollcommand=test_y_scrollbar.set)
test_canvas.configure(xscrollcommand=test_x_scrollbar.set)
test_canvas.pack(side="left", fill="both", expand=True)

test_button_width = 22
test_buttons_width = 30
test_buttons_height = 1
text_button_x_space = 2
test_button_y_space = 4
test_font_size = 18

# CHECK ERRORS Button
test_test_script_button = Button(test_main_buttons_frame, text="Check For Errors", bg="#5fafde", fg="White", padx=test_buttons_width,
                                 pady=test_buttons_height, font=("Times New Roman", test_font_size), relief=FLAT, width=test_button_width,
                                 command=error_buttons_func.function_runner)
test_test_script_button.pack(padx=text_button_x_space, pady=test_button_y_space)

# COMPILE DATA Button
test_compile_script_button = Button(test_main_buttons_frame, text="Compile Data Into Game", bg="#5fafde", fg="White", padx=test_buttons_width,
                                    pady=test_buttons_height, font=("Times New Roman", test_font_size), relief=FLAT, width=test_button_width, state=DISABLED,
                                    command=None)
test_compile_script_button.pack(padx=text_button_x_space, pady=test_button_y_space)
# -------------------------------------------
# THIS IS THE END OF THE "TEST" TAB CODE
# -------------------------------------------
# -------------------------------------------
# LOOP END
# -------------------------------------------

editor.config(menu=main_menu)
editor.protocol("WM_DELETE_WINDOW", close_window)
editor.mainloop()
