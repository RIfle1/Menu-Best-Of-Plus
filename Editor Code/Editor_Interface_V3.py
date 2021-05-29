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


def delete():
    for widget in test_main_error_frame.winfo_children():
        widget.destroy()


# Function to print Errors
def errors_print():

    # Create A Canvas
    canvas = Canvas(test_main_error_frame)
    canvas.pack(side=LEFT, fill='both', expand=1)

    # Add A Scroll Bar To Canvas
    scroll_bar = Scrollbar(test_main_error_frame, orient=VERTICAL, command=canvas.yview)
    scroll_bar.pack(side=RIGHT, fill='y')

    # Configure Canvas
    canvas.configure(yscrollcommand=scroll_bar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create Another Frame in Canvas
    test_main_error_frame_0 = LabelFrame(canvas)

    # Add A new Frame to a window in the canvas
    canvas.create_window((0, 0), window=test_main_error_frame_0, anchor="nw")

    # Update Canvas
    canvas.update_idletasks()
    canvas.config(scrollregion=test_main_error_frame_0.bbox())

    padding = 10
    errors_file = open("errors.txt", "r")
    text = errors_file.read()
    errors_list = text.split('###')

    for errors in errors_list[0:-1]:
        error_frame = LabelFrame(test_main_error_frame_0, height=100)
        error_frame.pack()
        error_message = Message(error_frame, text=errors, width=400)
        error_message.grid(column=0, row=0, padx=padding, pady=(padding, 0))


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

create_button, edit_button = PhotoImage(file='Illustrations/New Character.png'), PhotoImage(file='Illustrations/Edit Character.png')

# MAIN Frame
ch_left_frame_width = int(0.75 * window_x)
ch_main_frame = LabelFrame(characters_tab, width=ch_left_frame_width, height=window_y)
ch_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
ch_main_frame_height = int(window_y / 4.8)
ch_main_buttons_frame = LabelFrame(ch_main_frame, height=ch_main_frame_height, width=ch_left_frame_width)
ch_main_buttons_frame.pack(fill="both")

# Frame 2
ch_main_buttons_frame_2 =Frame(ch_main_buttons_frame, height=ch_main_frame_height, width=ch_left_frame_width)
ch_main_buttons_frame_2.pack()

# Characters Frame
ch_main_characters_frame = LabelFrame(ch_main_frame, height=window_x - ch_main_frame_height)
ch_main_characters_frame.pack(fill="both", expand=True)

ch_button_width = 22
ch_buttons_width = 30
ch_buttons_height = 1
ch_button_x_space = 2
ch_button_y_space = 4
ch_font_size = 18

# NEW CHARACTER & EDIT CHARACTER Button
createButton = Button(ch_main_buttons_frame_2, image=create_button, border=0, command=character_buttons_func.ch_new_window)
createButton.grid(column=1, row=0, padx=30, pady=30)
editButton = Button(ch_main_buttons_frame_2, image=edit_button, border=0, command=character_buttons_func.ch_edt_window)
editButton.grid(column=2, row=0, padx=15, pady=30)


# -------------------------------------------
# THIS IS THE END OF THE "CHARACTER" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "NPC" TAB
# -------------------------------------------
# ALL MAIN FRAMES

New_NPC, Edit_NPC = PhotoImage(file='Illustrations/New  NPC.png'), PhotoImage(file='Illustrations/Edit NPC.png')

# MAIN Frame
npc_left_frame_width = int(0.75 * window_x)
npc_main_frame = LabelFrame(npc_tab, width=npc_left_frame_width, height=window_y)
npc_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
npc_main_frame_height = int(window_y / 4.8)
npc_main_buttons_frame = LabelFrame(npc_main_frame, height=npc_main_frame_height, width=npc_left_frame_width)
npc_main_buttons_frame.pack(fill="both")

# Frame 2
npc_main_npc_frame2 =Frame(npc_main_buttons_frame, height=ch_main_frame_height, width=ch_left_frame_width)
npc_main_npc_frame2.pack()

npc_button_width = 22
npc_buttons_width = 30
npc_buttons_height = 1
npc_button_x_space = 2
npc_button_y_space = 4
npc_font_size = 18

# NEW NPC & EDIT NPC Button
npc_new_npc_button = Button(npc_main_npc_frame2, image=New_NPC, border=0, command=npc_buttons_func.npc_new_window)
npc_new_npc_button.grid(column=1, row=0, padx=30, pady=30)
npc_edit_npc_button = Button(npc_main_npc_frame2, image=Edit_NPC, border=0, command=npc_buttons_func.npc_edt_window)
npc_edit_npc_button.grid(column=2, row=0, padx=15, pady=30)

# -------------------------------------------
# THIS IS THE END OF THE "NPC" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "MONSTERS / ENEMIES" TAB
# -------------------------------------------

New_monster, edit_monster = PhotoImage(file='Illustrations/New  Monster.png'), PhotoImage(file='Illustrations/Edit Monster.png')

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

# Frame 2
ch_main_buttons_frame_2 =Frame(mst_main_buttons_frame, height=ch_main_frame_height, width=ch_left_frame_width)
ch_main_buttons_frame_2.pack()

mst_button_width = 22
mst_buttons_width = 30
mst_buttons_height = 1
mst_button_x_space = 2
mst_button_y_space = 4
mst_font_size = 18

# NEW MONSTER & EDIT MONSTER Button
mst_new_mst_button = Button(ch_main_buttons_frame_2, image=New_monster, border=0, command=monster_enemy_buttons_func.mst_new_window)
mst_new_mst_button.grid(column=1, row=0, padx=30, pady=30)
mst_new_mst_button = Button(ch_main_buttons_frame_2, image=edit_monster, border=0, command=monster_enemy_buttons_func.mst_edt_window)
mst_new_mst_button.grid(column=2, row=0, padx=15, pady=30)

# -------------------------------------------
# THIS IS THE END OF THE "MONSTERS / ENEMIES" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "OBJECTS" TAB
# -------------------------------------------
# ALL MAIN FRAMES

New_object, edit_object = PhotoImage(file='Illustrations/New  Object.png'), PhotoImage(file='Illustrations/Edit Object.png')

# MAIN Frame
obj_main_frame_width = int(0.75 * window_x)
obj_main_frame = LabelFrame(objects_tab, width=obj_main_frame_width, height=window_y)
obj_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
obj_main_frame_height = int(window_y / 4.8)
obj_main_buttons_frame = LabelFrame(obj_main_frame, height=obj_main_frame_height, width=obj_main_frame_width)
obj_main_buttons_frame.pack(fill="both")

# OBJECT Frame
obj_frame = LabelFrame(obj_main_frame, height=window_x - obj_main_frame_height)
obj_frame.pack(fill="both", expand=True)

# Frame 2
ch_main_buttons_frame_2 =Frame(obj_main_buttons_frame, height=ch_main_frame_height, width=ch_left_frame_width)
ch_main_buttons_frame_2.pack()

obj_button_width = 22
obj_buttons_width = 30
obj_buttons_height = 1
obj_button_x_space = 2
obj_button_y_space = 4
obj_font_size = 18

# NEW OBJECT & EDIT OBJECT Button
obj_new_obj_button = Button(ch_main_buttons_frame_2, image=New_object, border=0, command=object_buttons_func.obj_new_window)
obj_new_obj_button.grid(column=1, row=0, padx=30, pady=30)
obj_new_obj_button = Button(ch_main_buttons_frame_2, image=edit_object, border=0, command=object_buttons_func.obj_edt_window)
obj_new_obj_button.grid(column=2, row=0, padx=15, pady=30)


# -------------------------------------------
# THIS IS THE END OF THE "OBJECTS" TAB CODE
# -------------------------------------------
# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "TEST" TAB
# -------------------------------------------

Check = PhotoImage(file='Illustrations/Safety Check.png')
Compile = PhotoImage(file='Illustrations/Compile.png')

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
test_main_error_frame = LabelFrame(test_main_frame, height=window_x - test_main_frame_height)
test_main_error_frame.pack(fill="both", expand=True)


test_button_width = 22
test_buttons_width = 30
test_buttons_height = 1
text_button_x_space = 500
test_button_y_space = 4
test_font_size = 18

# CHECK ERRORS BUTTON
test_test_script_button = Button(test_main_buttons_frame, image=Check, border=0, command=error_buttons_func.function_runner)
test_test_script_button.grid(column=1, row=0, padx=630, pady=30)

# COMPILE BUTTON
test_compile_script_button = Button(test_main_buttons_frame, image=Compile, border=0, command=None)
test_compile_script_button.grid(column=1, row=1, padx=700, pady=20)

# -------------------------------------------
# THIS IS THE END OF THE "TEST" TAB CODE
# -------------------------------------------
# -------------------------------------------
# LOOP END
# -------------------------------------------

editor.config(menu=main_menu)
editor.protocol("WM_DELETE_WINDOW", close_window)
editor.mainloop()
