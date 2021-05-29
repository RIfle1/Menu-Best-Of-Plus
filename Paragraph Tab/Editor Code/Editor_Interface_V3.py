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

main_font = ("Times New Roman", 12)


# Functions That Refresh Button calls
def refresh():
    global database
    database = editor_settings.database_module.database

    # Delete Previous Info
    for widget in pg_2_main_frame_2.winfo_children():
        widget.destroy()

    # Delete previous paragraphs in the frame
    for widgets in pg_main_story_frame.winfo_children():
        widgets.destroy()

    # Call All Info
    new_story_print()
    errors_print()
    character_list()
    npc_list()
    mst_list()
    obj_list()


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

        error_message = Message(error_frame, text=errors, width=400, font=main_font)
        error_message.grid(column=0, row=0, padx=padding, pady=(padding, 0), stick="w")
        row += 1


# Function To Print Info in Info List
def character_list():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get All Info From Characters
    c.execute(f"""SELECT ch_name, ch_breed, ch_life, ch_speed, ch_defense, ch_attack, ch_background FROM characters""")
    characters_list_info = c.fetchall()

    labels_width = 10
    messages_width = 200
    padding = 10

    if characters_list_info:
        # Frame For All characters
        ch_main_list_frame = LabelFrame(pg_2_main_frame_2, text=f'CHARACTERS LIST', font=main_font)
        ch_main_list_frame.pack(fill="both", side=LEFT)
    else:
        ch_main_list_frame = None

    for ch in characters_list_info:
        # Frame For each character
        ch_info_frame = LabelFrame(ch_main_list_frame, text=f'{ch[0]}', font=main_font)
        ch_info_frame.pack(fill="both")

        # Label Frame
        ch_info_label_frame = Frame(ch_info_frame)
        ch_info_label_frame.pack(fill="both", side=LEFT)

        # Labels
        breed_label = Label(ch_info_label_frame, text="Breed:", width=labels_width, font=main_font, anchor=W)
        breed_label.grid(row=1, column=0, padx=padding, pady=padding, stick="w")

        life_label = Label(ch_info_label_frame, text="Life:", width=labels_width, font=main_font, anchor=NW)
        life_label.grid(row=2, column=0, padx=padding, pady=padding, stick="nw")

        speed_label = Label(ch_info_label_frame, text="Speed:", width=labels_width, font=main_font, anchor=NW)
        speed_label.grid(row=3, column=0, padx=padding, pady=padding, stick="nw")

        attack_label = Label(ch_info_label_frame, text="Attack:", width=labels_width, font=main_font, anchor=NW)
        attack_label.grid(row=4, column=0, padx=padding, pady=padding, stick="nw")

        defense_label = Label(ch_info_label_frame, text="Defense:", width=labels_width, font=main_font, anchor=NW)
        defense_label.grid(row=5, column=0, padx=padding, pady=padding, stick="nw")

        background_label = Label(ch_info_label_frame, text="Background:", width=labels_width, font=main_font, anchor=NW)
        background_label.grid(row=6, column=0, padx=padding, pady=padding, stick="nw")

        # Character Info Frame
        ch_info_frame = Frame(ch_info_frame)
        ch_info_frame.pack(fill="both", side=RIGHT)

        # Labels
        breed_info = Label(ch_info_frame, text=str(ch[1]), width=labels_width, font=main_font, anchor=W)
        breed_info.grid(row=1, column=0, padx=padding, pady=padding, stick="w")

        life_info = Label(ch_info_frame, text=str(ch[2]), width=labels_width, font=main_font, anchor=NW)
        life_info.grid(row=2, column=0, padx=padding, pady=padding, stick="nw")

        speed_info = Label(ch_info_frame, text=str(ch[3]), width=labels_width, font=main_font, anchor=NW)
        speed_info.grid(row=3, column=0, padx=padding, pady=padding, stick="nw")

        attack_info = Label(ch_info_frame, text=str(ch[4]), width=labels_width, font=main_font, anchor=NW)
        attack_info.grid(row=4, column=0, padx=padding, pady=padding, stick="nw")

        defense_info = Label(ch_info_frame, text=str(ch[5]), width=labels_width, font=main_font, anchor=NW)
        defense_info.grid(row=5, column=0, padx=padding, pady=padding, stick="nw")

        background_message = Message(ch_info_frame, text=str(ch[6]), width=messages_width, font=main_font, anchor=NW)
        background_message.grid(row=6, column=0, padx=padding, pady=padding, stick="nw")

    conn.commit()


def npc_list():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get All NPC Names
    c.execute(f"""SELECT npc_name FROM npcs""")
    npc_name_list_raw = c.fetchall()
    npc_name_list = id.raw_conv(npc_name_list_raw)

    messages_width = 200
    padding = 10

    if npc_name_list:
        # Frame For All characters
        npc_main_list_frame = LabelFrame(pg_2_main_frame_2, text=f'NPC LIST', font=main_font)
        npc_main_list_frame.pack(fill="both", side=LEFT)
    else:
        npc_main_list_frame = None

    for npc_name in npc_name_list:
        npc_name_message = Message(npc_main_list_frame, text=str(npc_name), width=messages_width, font=main_font, anchor=NW)
        npc_name_message.pack(padx=padding, pady=padding)

    conn.commit()


def mst_list():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get All NPC Names
    c.execute(f"""SELECT mst_name FROM monsters""")
    mst_name_list_raw = c.fetchall()
    mst_name_list = id.raw_conv(mst_name_list_raw)

    messages_width = 200
    padding = 10

    if mst_name_list:
        # Frame For All characters
        mst_main_list_frame = LabelFrame(pg_2_main_frame_2, text=f'ENEMIES LIST', font=main_font)
        mst_main_list_frame.pack(fill="both", side=LEFT)
    else:
        mst_main_list_frame = None

    for mst_name in mst_name_list:
        mst_name_message = Message(mst_main_list_frame, text=str(mst_name), width=messages_width, font=main_font, anchor=NW)
        mst_name_message.pack(padx=padding, pady=padding)

    conn.commit()


def obj_list():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get All NPC Names
    c.execute(f"""SELECT obj_name FROM objects""")
    obj_name_list_raw = c.fetchall()
    obj_name_list = id.raw_conv(obj_name_list_raw)

    messages_width = 200
    padding = 10

    if obj_name_list:
        # Frame For All characters
        obj_main_list_frame = LabelFrame(pg_2_main_frame_2, text=f'OBJECTS LIST', font=main_font)
        obj_main_list_frame.pack(fill="both", side=LEFT)
    else:
        obj_main_list_frame = None

    for obj_name in obj_name_list:
        obj_name_message = Message(obj_main_list_frame, text=str(obj_name), width=messages_width, font=main_font, anchor=NW)
        obj_name_message.pack(padx=padding, pady=padding)

    conn.commit()


# Class to set tab number in new_tab function
class NewTab(Frame):
    def __init__(self, root, name):
        Frame.__init__(self, root)

        self.root = root
        self.name = name


# Function to print all created stories as tabs
def new_story_print():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    messages_width = 300
    labels_width = 20
    padding = 10

    c.execute(f"SELECT s_id FROM stories ORDER BY s_id")
    story_id_list_raw = c.fetchall()
    story_id_list = []
    for tp in story_id_list_raw:
        for item in tp:
            story_id_list.append(item)

    # Create Canvas
    tab_canvas = Canvas(pg_main_story_frame)

    # Create ScrollBar
    tab_y_scrollbar = Scrollbar(pg_main_story_frame, orient="vertical", command=tab_canvas.yview)
    tab_y_scrollbar.pack(side="right", fill="y")
    tab_x_scrollbar = Scrollbar(pg_main_story_frame, orient="horizontal", command=tab_canvas.xview)
    tab_x_scrollbar.pack(side="bottom", fill="x")

    # Frame To Put Objects in
    tab_main_frame_2 = Frame(tab_canvas)
    tab_main_frame_2.bind("<Configure>", lambda e: tab_canvas.configure(scrollregion=tab_canvas.bbox("all")))

    # Canvas Config
    tab_canvas.create_window((0, 0), window=tab_main_frame_2, anchor="nw")
    tab_canvas.configure(yscrollcommand=tab_y_scrollbar.set)
    tab_canvas.configure(xscrollcommand=tab_x_scrollbar.set)
    tab_canvas.pack(side="left", fill="both", expand=True)

    for s_id in story_id_list:
        main_story_info_frame = LabelFrame(tab_main_frame_2, text=f'STORY NUMBER {id.id_int(s_id)}', font=main_font)
        main_story_info_frame.pack(fill="both")

        # Display All initial Paragraphs With Their Info
        c.execute(
            f"""SELECT ip_id, ip_text FROM initial_paragraphs WHERE s_id = '{s_id}'""")
        initial_paragraphs_info_list = c.fetchall()

        if initial_paragraphs_info_list:
            main_initial_paragraph_info_frame = LabelFrame(main_story_info_frame, text=f'INITIAL PARAGRAPH', font=main_font)
            main_initial_paragraph_info_frame.pack(fill="both", side=LEFT)
        else:
            main_initial_paragraph_info_frame = None

        for paragraph in initial_paragraphs_info_list:

            ip_id = paragraph[0]
            ip_text = paragraph[1]

            initial_paragraph_info_frame = Frame(main_initial_paragraph_info_frame)
            initial_paragraph_info_frame.pack(fill="both", side=LEFT)

            initial_paragraph_text_frame = LabelFrame(initial_paragraph_info_frame, text='Initial Paragaph Text',
                                                      font=main_font, labelanchor="n")
            initial_paragraph_text_frame.pack(fill="both")

            initial_paragraph_message = Message(initial_paragraph_text_frame, text=ip_text, width=messages_width, font=main_font,
                                        anchor=NW)
            initial_paragraph_message.pack(padx=padding, pady=padding)

            c.execute(f"""SELECT c_id, c_text, obj_id FROM choices WHERE c_id LIKE '{ip_id}%'""")
            choices_info_list = c.fetchall()

            if choices_info_list:
                initial_paragraph_choices_frame = LabelFrame(initial_paragraph_info_frame, text='Initial Paragraph Choices', font=main_font,
                                                     labelanchor="n")
                initial_paragraph_choices_frame.pack(fill="both")
            else:
                initial_paragraph_choices_frame = None

            for choice in choices_info_list:
                c_id = choice[0]
                c_text = choice[1]
                obj_id = choice[2]

                c.execute(f"""SELECT obj_name FROM objects WHERE obj_id = '{obj_id}'""")
                obj_name_raw = c.fetchall()
                obj_name = id.raw_conv(obj_name_raw)

                if not obj_name:
                    obj = "No Condition"
                else:
                    obj = obj_name[0]

                if len(id.decoder_2(c_id)) == 3:
                    choice_number = id.int_list(id.decoder_2(c_id))[-1]
                    to_paragraph = "Unassigned"
                else:
                    choice_number = id.int_list(id.decoder_2(c_id))[-2]
                    to_paragraph = f"To {id.decoder_5(id.decoder_2(c_id)[-1])}"

                int_pg_choice_frame = LabelFrame(initial_paragraph_choices_frame, text=f'Choice N.{choice_number}\t {to_paragraph}', font=main_font, labelanchor="n")
                int_pg_choice_frame.pack(fill="both")

                # Labels Inside each Choice Frame
                int_pg_choice_text_label = Label(int_pg_choice_frame, text='Choice Text:', width=labels_width, font=main_font, anchor=NW)
                int_pg_choice_text_label.grid(column=0, row=0, stick="w", padx=padding, pady=padding)

                int_pg_choice_condition_label = Label(int_pg_choice_frame, text='Choice Condition:', width=labels_width, font=main_font, anchor=NW)
                int_pg_choice_condition_label.grid(column=0, row=1, stick="w", padx=padding, pady=padding)

                # Messages To display in each choice frame
                int_pg_choice_text_message = Message(int_pg_choice_frame, text=f'{c_text}', width=messages_width, font=main_font, anchor=NW)
                int_pg_choice_text_message.grid(column=1, row=0, stick="nw", padx=padding, pady=padding)

                int_pg_choice_condition_message = Message(int_pg_choice_frame, text=f'{obj}', width=messages_width, font=main_font, anchor=NW)
                int_pg_choice_condition_message.grid(column=1, row=1, stick="nw", padx=padding, pady=padding)

        # Display All Paragraphs With Their Info
        c.execute(f"""SELECT pl_id, p_text, npc_id, mst_id, obj_id FROM paragraphs_list WHERE s_id = '{s_id}' 
        EXCEPT SELECT pl_id, p_text, npc_id, mst_id, obj_id FROM paragraphs_list WHERE end_bool = {1}""")
        paragraphs_info_list = c.fetchall()

        if paragraphs_info_list:
            main_paragraph_info_frame = LabelFrame(main_story_info_frame, text=f'PARAGRAPHS LIST', font=main_font)
            main_paragraph_info_frame.pack(fill="both", side=LEFT)
        else:
            main_paragraph_info_frame = None

        for paragraph in paragraphs_info_list:

            pl_id = paragraph[0]
            p_text = paragraph[1]
            npc_id = paragraph[2]
            mst_id = paragraph[3]
            obj_id = paragraph[4]

            c.execute(f"""SELECT obj_name from objects WHERE obj_id = '{obj_id}'""")
            obj_name_raw = c.fetchall()
            obj_name = id.raw_conv(obj_name_raw)

            if not obj_name:
                obj = "No Drop Assigned"
            else:
                obj = obj_name

            if npc_id == 'None' and mst_id == "None":
                enemy = "Unassigned NPC"
            elif npc_id == "None":
                enemy = mst_id
            else:
                enemy = npc_id

            paragraph_info_frame = LabelFrame(main_paragraph_info_frame, text=f'{id.decoder_5(pl_id)}\t{enemy}', font=main_font, labelanchor="n")
            paragraph_info_frame.pack(fill="both", side=LEFT)

            paragraph_object_frame = LabelFrame(paragraph_info_frame, text='Paragraph Object', font=main_font, labelanchor="n")
            paragraph_object_frame.pack(fill="both")

            paragraph_object_message = Message(paragraph_object_frame, text=obj, width=messages_width, font=main_font, anchor=NW)
            paragraph_object_message.pack(padx=padding, pady=padding)

            paragraph_text_frame = LabelFrame(paragraph_info_frame, text='Paragraph Text', font=main_font, labelanchor="n")
            paragraph_text_frame.pack(fill="both")

            paragraph_text_message = Message(paragraph_text_frame, text=p_text, width=messages_width, font=main_font, anchor=NW)
            paragraph_text_message.pack(padx=padding, pady=padding)

            c.execute(f"""SELECT c_id, c_text, obj_id FROM choices WHERE c_id LIKE '{pl_id}%'""")
            choices_info_list = c.fetchall()

            if choices_info_list:
                paragraph_choices_frame = LabelFrame(paragraph_info_frame, text='Paragraph Choices', font=main_font, labelanchor="n")
                paragraph_choices_frame.pack(fill="both")
            else:
                paragraph_choices_frame = None

            for choice in choices_info_list:
                c_id = choice[0]
                c_text = choice[1]
                obj_id = choice[2]

                c.execute(f"""SELECT obj_name FROM objects WHERE obj_id = '{obj_id}'""")
                obj_name_raw = c.fetchall()
                obj_name = id.raw_conv(obj_name_raw)

                if not obj_name:
                    obj = "No Condition"
                else:
                    obj = obj_name[0]

                if len(id.decoder_2(c_id)) == 3:
                    choice_number = id.int_list(id.decoder_2(c_id))[-1]
                    to_paragraph = "Unassigned"
                else:
                    choice_number = id.int_list(id.decoder_2(c_id))[-2]
                    to_paragraph = f'To {id.decoder_5(id.decoder_2(c_id)[-1])}'

                pg_choice_frame = LabelFrame(paragraph_choices_frame, text=f'Choice N.{choice_number}\t {to_paragraph}', font=main_font, labelanchor="n")
                pg_choice_frame.pack(fill="both")

                # Labels Inside each Choice Frame
                pg_choice_text_label = Label(pg_choice_frame, text='Choice Text:', width=labels_width, font=main_font, anchor=NW)
                pg_choice_text_label.grid(column=0, row=0, stick="w", padx=padding, pady=padding)

                pg_choice_condition_label = Label(pg_choice_frame, text='Choice Condition:', width=labels_width, font=main_font, anchor=NW)
                pg_choice_condition_label.grid(column=0, row=1, stick="w", padx=padding, pady=padding)

                # Messages To display in each choice frame
                pg_choice_text_message = Message(pg_choice_frame, text=f'{c_text}', width=messages_width, font=main_font, anchor=NW)
                pg_choice_text_message.grid(column=1, row=0, stick="nw", padx=padding, pady=padding)

                pg_choice_condition_message = Message(pg_choice_frame, text=f'{obj}', width=messages_width, font=main_font, anchor=NW)
                pg_choice_condition_message.grid(column=1, row=1, stick="nw", padx=padding, pady=padding)

        # Display All Ending Paragraphs With Their Info
        c.execute(f"""SELECT pl_id, p_text, npc_id, mst_id FROM paragraphs_list WHERE s_id = '{s_id}' 
                        EXCEPT SELECT pl_id, p_text, npc_id, mst_id FROM paragraphs_list WHERE end_bool = {0}""")
        end_paragraphs_info_list = c.fetchall()

        if end_paragraphs_info_list:
            main_end_paragraph_info_frame = LabelFrame(main_story_info_frame, text=f'ENDING PARAGRAPHS LIST',
                                                       font=main_font)
            main_end_paragraph_info_frame.pack(fill="both", side=LEFT)
        else:
            main_end_paragraph_info_frame = None

        for end_paragraph in end_paragraphs_info_list:

            pl_id = end_paragraph[0]
            p_text = end_paragraph[1]
            npc_id = end_paragraph[2]
            mst_id = end_paragraph[3]

            if npc_id == 'None' and mst_id == "None":
                enemy = "Unassigned NPC"
            elif npc_id == "None":
                enemy = mst_id
            else:
                enemy = npc_id

            paragraph_info_frame = LabelFrame(main_end_paragraph_info_frame, text=f'{id.decoder_5(pl_id)}\t{enemy}',
                                              font=main_font, labelanchor="n")
            paragraph_info_frame.pack(fill="both", side=LEFT)

            paragraph_text_frame = LabelFrame(paragraph_info_frame, text='Paragraph Text', font=main_font,
                                              labelanchor="n")
            paragraph_text_frame.pack(fill="both")

            paragraph_text_message = Message(paragraph_text_frame, text=p_text, width=messages_width,
                                             font=main_font, anchor=NW)
            paragraph_text_message.pack(padx=padding, pady=padding)

    conn.commit()


# Create ALL necessary tables in the database
connection = sqlite3.connect(database, uri=True)
cursor = connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS stories 
                                                   (s_id text, 
                                                   s_text text,
                                                   ch_id text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS initial_paragraphs
                                                       (s_id text, 
                                                       ip_id text,
                                                       ip_text text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS paragraphs_list
                                                           (s_id text,
                                                           pl_id text,
                                                           p_text text,
                                                           npc_id text,
                                                           mst_id text,
                                                           npc_bool integer,
                                                           mst_bool integer,
                                                           obj_id text,
                                                           end_bool integer)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS choices
                                                       (s_id text,
                                                       ip_id text,
                                                       c_id text,
                                                       obj_id text,
                                                       c_text text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS characters
                                                                (ch_id text,
                                                                ch_name text, 
                                                                ch_breed text,
                                                                ch_life integer,
                                                                ch_speed integer,
                                                                ch_defense integer,
                                                                ch_attack integer,
                                                                ch_background text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS npcs
                                                                (npc_id text,
                                                                npc_name text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS monsters
                                                                (mst_id text,
                                                                mst_name text,
                                                                mst_type text)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS objects
                                                                    (obj_id text,
                                                                    obj_name text)""")

connection.commit()

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

window_x = editor.winfo_screenwidth()-30
window_y = editor.winfo_screenheight()-110
editor.geometry(f"{window_x}x{window_y}+{10}+{10}")

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
story_tab = ttk.Frame(tabControl)
test_tab = ttk.Frame(tabControl)

# Adding Tabs
tabControl.add(story_tab, text="Create a Story")
tabControl.add(test_tab, text="Test / Compile")

# Positioning the Tabs
tabControl.pack(expand=1, fill="both")

# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "PARAGRAPH" TAB
# -------------------------------------------
# ALL MAIN FRAMES

# Left Frame
pg_left_frame_width = int(0.65 * window_x)
pg_left_frame = Frame(story_tab)
pg_left_frame.pack(fill="both", side=LEFT)

# List Frame
pg_right_frame = LabelFrame(story_tab, height=window_y)
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
pg_main_buttons_frame = LabelFrame(pg_left_frame)
pg_main_buttons_frame.pack(fill="both", ipadx=500)

# Scroll Bar stuff
button_main_frame_1 = Frame(pg_main_buttons_frame)
button_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
button_canvas = Canvas(button_main_frame_1)

# Create ScrollBar
button_y_scrollbar = Scrollbar(button_main_frame_1, orient="vertical", command=button_canvas.yview)
button_y_scrollbar.pack(side="right", fill="y")
button_x_scrollbar = Scrollbar(button_main_frame_1, orient="horizontal", command=button_canvas.xview)
button_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
button_main_frame_2 = Frame(button_canvas)
button_main_frame_2.bind("<Configure>", lambda e: button_canvas.configure(scrollregion=button_canvas.bbox("all")))

# Canvas Config
button_canvas.create_window((0, 0), window=button_main_frame_2, anchor="nw")
button_canvas.configure(yscrollcommand=button_y_scrollbar.set)
button_canvas.configure(xscrollcommand=button_x_scrollbar.set)
button_canvas.pack(side="left", fill="both", expand=True)

# Story Frame
pg_main_story_frame = LabelFrame(pg_left_frame)
pg_main_story_frame.pack(fill="both", expand=True)

main_pad_x = 15
main_pad_y = 15
main_buttons_height = 1
main_buttons_width = 20
main_font_size = 18

# Button Pictures
new_ch_image, edit_ch_image = PhotoImage(file='Illustrations/New Character.png'), PhotoImage(file='Illustrations/Edit Character.png')
new_npc_image, edit_npc_image = PhotoImage(file='Illustrations/New  NPC.png'), PhotoImage(file='Illustrations/Edit NPC.png')
new_monster_image, edit_monster_image = PhotoImage(file='Illustrations/New  Monster.png'), PhotoImage(file='Illustrations/Edit Monster.png')
new_object_image, edit_object_image = PhotoImage(file='Illustrations/New  Object.png'), PhotoImage(file='Illustrations/Edit Object.png')


# NEW STORY Button
pg_new_story_button = Button(button_main_frame_2, text="New Story", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, width=main_buttons_width, height=main_buttons_height,
                             command=story_button_func.s_new_window)
pg_new_story_button.grid(row=0, column=0, stick="w", padx=main_pad_x, pady=main_pad_y)

# EDIT STORY  Button
pg_edit_story_button = Button(button_main_frame_2, text="Edit Story", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, width=main_buttons_width, height=main_buttons_height,
                              command=story_button_func.s_edt_window)
pg_edit_story_button.grid(row=1, column=0, stick="w", padx=main_pad_x, pady=main_pad_y)

# ADD INITIAL PARAGRAPH Button
pg_new_int_par_button = Button(button_main_frame_2, text="New Initial Paragraph", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, height=main_buttons_height,
                               width=main_buttons_width, command=initial_paragraph_buttons_func.ip_new_window)
pg_new_int_par_button.grid(row=0, column=1, stick="w", padx=main_pad_x, pady=main_pad_y)

# EDIT INITIAL PARAGRAPH  Button
pg_edit_int_par_button = Button(button_main_frame_2, text="Edit Initial Paragraph", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, height=main_buttons_height,
                                width=main_buttons_width, command=initial_paragraph_buttons_func.ip_edt_window)
pg_edit_int_par_button.grid(row=1, column=1, stick="w", padx=main_pad_x, pady=main_pad_y)

# NEW PARAGRAPH Button
pg_new_paragraph_button = Button(button_main_frame_2, text="New Paragraph", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, height=main_buttons_height,
                                 width=main_buttons_width, command=paragraph_buttons_func.p_new_window)
pg_new_paragraph_button.grid(row=0, column=2, stick="w", padx=main_pad_x, pady=main_pad_y)

# EDIT PARAGRAPH  Button
edit_paragraph_button = Button(button_main_frame_2, text="Edit Paragraph", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, width=main_buttons_width, height=main_buttons_height,
                               command=paragraph_buttons_func.p_edt_window)
edit_paragraph_button.grid(row=1, column=2, stick="w", padx=main_pad_x, pady=main_pad_y)

# ADD CHOICE Button
new_choice_button = Button(button_main_frame_2, text="New Choice", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, width=main_buttons_width, height=main_buttons_height,
                           command=choice_buttons_func.c_new_window)
new_choice_button.grid(row=0, column=3, stick="w", padx=main_pad_x, pady=main_pad_y)

# EDIT CHOICE  Button
edit_choice_button = Button(button_main_frame_2, text="Edit Choice", bg="#5fafde", fg="White", font=("Times New Roman", main_font_size), relief=FLAT, width=main_buttons_width, height=main_buttons_height,
                            command=choice_buttons_func.c_edt_window)
edit_choice_button.grid(row=1, column=3, stick="w", padx=main_pad_x, pady=main_pad_y)

# NEW CHARACTER & EDIT CHARACTER Button
new_ch_button = Button(button_main_frame_2, image=new_ch_image, border=0, command=character_buttons_func.ch_new_window)
new_ch_button.grid(column=4, row=0, padx=main_pad_x, pady=main_pad_y)
edit_ch_button = Button(button_main_frame_2, image=edit_ch_image, border=0, command=character_buttons_func.ch_edt_window)
edit_ch_button.grid(column=4, row=1, padx=main_pad_x, pady=main_pad_y)

# NEW NPC & EDIT NPC Button
new_npc_button = Button(button_main_frame_2, image=new_npc_image, border=0, command=npc_buttons_func.npc_new_window)
new_npc_button.grid(column=5, row=0, padx=main_pad_x, pady=main_pad_y)
edit_npc_button = Button(button_main_frame_2, image=edit_npc_image, border=0, command=npc_buttons_func.npc_edt_window)
edit_npc_button.grid(column=5, row=1, padx=main_pad_x, pady=main_pad_y)

# NEW MONSTER & EDIT MONSTER Button
new_mst_button = Button(button_main_frame_2, image=new_monster_image, border=0, command=monster_enemy_buttons_func.mst_new_window)
new_mst_button.grid(column=6, row=0, padx=main_pad_x, pady=main_pad_y)
new_mst_button = Button(button_main_frame_2, image=edit_monster_image, border=0, command=monster_enemy_buttons_func.mst_edt_window)
new_mst_button.grid(column=6, row=1, padx=main_pad_x, pady=main_pad_y)

# NEW OBJECT & EDIT OBJECT Button
new_obj_button = Button(button_main_frame_2, image=new_object_image, border=0, command=object_buttons_func.obj_new_window)
new_obj_button.grid(column=7, row=0, padx=main_pad_x, pady=main_pad_y)
new_obj_button = Button(button_main_frame_2, image=edit_object_image, border=0, command=object_buttons_func.obj_edt_window)
new_obj_button.grid(column=7, row=1, padx=main_pad_x, pady=main_pad_y)

# -------------------------------------------
# THIS IS THE END OF THE "PARAGRAPH" TAB CODE
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
text_button_x_space = 500
test_button_y_space = 4
test_font_size = 18

check_button, compile_button = PhotoImage(file='Illustrations/Safety Check.png'), PhotoImage(file='Illustrations/Compile.png')

# CHECK ERRORS BUTTON
test_test_script_button = Button(test_main_buttons_frame, image=check_button, border=0, command=error_buttons_func.function_runner)
test_test_script_button.grid(column=1, row=0, padx=630, pady=30)

# COMPILE BUTTON
test_compile_script_button = Button(test_main_buttons_frame, image=compile_button, border=0, command=None)
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
