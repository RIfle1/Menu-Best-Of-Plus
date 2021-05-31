import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import player_settings
import id
from functools import partial

database = player_settings.database_module.database

main_font = ("Times New Roman", 12)

progress_list = []
inventory = []


def style_func():
    ch_font_size = 11
    ch_style = ttk.Style()
    ch_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', ch_font_size))
    ch_style.configure("TButton", font=('Times New Roman', ch_font_size))
    ch_style.configure("TLabel", font=('Times New Roman', ch_font_size))


def load_story():
    player_settings.load_story()
    character_select()


def clear_frame():
    for widget in game_frame.winfo_children():
        widget.destroy()
    for widget in inventory_frame.winfo_children():
        widget.destroy()


def print_paragraph(choice_id):
    global database
    database = player_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    clear_frame()

    messages_width = 200
    padding = 10

    s_id = progress_list[0]
    ch_name = progress_list[1]

    p_id = f'{s_id}_{id.decoder_2(choice_id)[-1]}'
    p_id_number = id.id_int(p_id)

    # Main Frames
    paragraph_text_frame = LabelFrame(game_frame, text=f"PARAGRAPH N.{p_id_number}\t Character: {ch_name}", font=main_font, labelanchor="n")
    paragraph_text_frame.pack(fill='both', side=TOP)

    paragraph_choices_frame = LabelFrame(game_frame, text=f"PARAGRAPH CHOICES", font=main_font, labelanchor="n")
    paragraph_choices_frame.pack(fill='both', side=TOP)

    next_button_frame = LabelFrame(game_frame)
    next_button_frame.pack(fill='both', side=BOTTOM)

    # Story Message
    c.execute(f"""SELECT p_text from paragraphs_list WHERE pl_id = '{p_id}'""")
    p_text_raw = c.fetchall()
    p_text = id.raw_conv(p_text_raw)[0]

    p_text_message = Message(paragraph_text_frame, text=p_text, width=messages_width, font=main_font, anchor=N)
    p_text_message.pack(padx=padding, pady=padding, anchor="center")

    # Scroll Bar stuff
    inv_scroll_bar_frame = Frame(inventory_frame)
    inv_scroll_bar_frame.pack(fill="both", expand=True)

    # Create Canvas
    inv_canvas = Canvas(inv_scroll_bar_frame)

    # Create ScrollBar
    inv_button_y_scrollbar = Scrollbar(inv_scroll_bar_frame, orient="vertical", command=inv_canvas.yview)
    inv_button_y_scrollbar.pack(side="right", fill="y")
    inv_button_x_scrollbar = Scrollbar(inv_scroll_bar_frame, orient="horizontal", command=inv_canvas.xview)
    inv_button_x_scrollbar.pack(side="bottom", fill="x")

    # Frame To Put Objects in
    inv_inside_frame = Frame(inv_canvas)
    inv_inside_frame.bind("<Configure>", lambda e: inv_canvas.configure(scrollregion=inv_canvas.bbox("all")))

    # Canvas Config
    inv_canvas.create_window((0, 0), window=inv_inside_frame, anchor="nw")
    inv_canvas.configure(yscrollcommand=inv_button_y_scrollbar.set)
    inv_canvas.configure(xscrollcommand=inv_button_x_scrollbar.set)
    inv_canvas.pack(side="left", fill="both", expand=True)

    for obj_name in inventory:
        # Add Frame For Each Item
        item_frame = LabelFrame(inv_inside_frame)
        item_frame.pack(fill="x", side=TOP)

        # Add Message with Item Into Frame
        item_message = Message(item_frame, text=obj_name, width=messages_width, font=main_font, anchor=N)
        item_message.pack(padx=padding, pady=padding, anchor="center")

    # Add Object Assigned To Paragraph To Inventory
    c.execute(f"""SELECT obj_id from paragraphs_list WHERE pl_id = '{p_id}'""")
    obj_id_raw = c.fetchall()
    obj_id = id.raw_conv(obj_id_raw)[0]

    if obj_id != 'None':
        c.execute(f"""SELECT obj_name from objects WHERE obj_id = '{obj_id}'""")
        obj_name_raw = c.fetchall()
        obj_name = id.raw_conv(obj_name_raw)[0]

        inventory.append(obj_name)

    # Paragraph Choices Message
    c.execute(f"""SELECT c_id, c_text, obj_id FROM choices WHERE c_id LIKE '{p_id}%'""")
    choices_info_list = c.fetchall()

    choice_button_list = []

    for choice in choices_info_list:
        c_id = choice[0]
        c_text = choice[1]
        obj_id = choice[2]
        choice_number = id.int_list(id.decoder_2(c_id))[-2]

        int_pg_choice_frame = LabelFrame(paragraph_choices_frame, text=f'Choice N.{choice_number}', font=main_font,
                                         labelanchor="n")
        int_pg_choice_frame.pack(fill="both")

        # Choice To display in each choice frame
        int_pg_choice_text_message = Message(int_pg_choice_frame, text=f'{c_text}', width=messages_width,
                                             font=main_font, anchor=NW)
        int_pg_choice_text_message.grid(column=0, row=0, stick="n", padx=padding, pady=padding)

        # Choice Button
        choice_button = ttk.Button(next_button_frame, text=f"Choice N.{choice_number}", command=partial(print_paragraph, c_id))
        choice_button.pack(padx=padding, pady=padding, anchor="center")

        choice_button_list.append(choice_button)

    conn.commit()


def print_ip():
    global database
    database = player_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    clear_frame()

    messages_width = 200
    padding = 10

    s_id = progress_list[0]
    ch_name = progress_list[1]

    progress_list.append(f'{s_id}_IP')

    ip_id = progress_list[2]

    # Main Frames
    ip_text_frame = LabelFrame(game_frame, text=f"INITIAL PARAGRAPH\t Character: {ch_name}", font=main_font, labelanchor="n")
    ip_text_frame.pack(fill='both', side=TOP)

    ip_choices_frame = LabelFrame(game_frame, text=f"INITIAL PARAGRAPH CHOICES", font=main_font, labelanchor="n")
    ip_choices_frame.pack(fill='both', side=TOP)

    next_button_frame = LabelFrame(game_frame)
    next_button_frame.pack(fill='both', side=BOTTOM)

    # Initial Paragraph Text Message
    c.execute(f"""SELECT ip_text from initial_paragraphs WHERE s_id = '{s_id}'""")
    ip_text_raw = c.fetchall()
    ip_text = id.raw_conv(ip_text_raw)[0]

    ip_text_message = Message(ip_text_frame, text=ip_text, width=messages_width, font=main_font, anchor=N)
    ip_text_message.pack(padx=padding, pady=padding, anchor="center")

    # Initial Paragraph Choices Message
    c.execute(f"""SELECT c_id, c_text, obj_id FROM choices WHERE c_id LIKE '{ip_id}%'""")
    choices_info_list = c.fetchall()

    for choice in choices_info_list:
        c_id = choice[0]
        c_text = choice[1]
        obj_id = choice[2]
        choice_number = id.int_list(id.decoder_2(c_id))[-2]

        int_pg_choice_frame = LabelFrame(ip_choices_frame, text=f'Choice N.{choice_number}', font=main_font, labelanchor="n")
        int_pg_choice_frame.pack(fill="both")

        # Choice To display in each choice frame
        int_pg_choice_text_message = Message(int_pg_choice_frame, text=f'{c_text}', width=messages_width, font=main_font, anchor=NW)
        int_pg_choice_text_message.grid(column=0, row=0, stick="n", padx=padding, pady=padding)

        # Choice Button
        choice_button = ttk.Button(next_button_frame, text=f"Choice N.{choice_number}", command=partial(print_paragraph, c_id))
        choice_button.pack(padx=padding, pady=padding, anchor="center")

    conn.commit()


def print_story():
    global database
    database = player_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    clear_frame()

    messages_width = 200
    padding = 10

    s_id = progress_list[0]
    ch_name = progress_list[1]

    # Main Frames
    story_frame = LabelFrame(game_frame, text=f"STORY\tCharacter: {ch_name}", font=main_font, labelanchor="n")
    story_frame.pack(fill='both', side=TOP)

    next_button_frame = LabelFrame(game_frame)
    next_button_frame.pack(fill='both', side=BOTTOM)



    # Story Message
    c.execute(f"""SELECT s_text from stories WHERE s_id = '{s_id}'""")
    s_text_raw = c.fetchall()
    s_text = id.raw_conv(s_text_raw)[0]

    story_text_message = Message(story_frame, text=s_text, width=messages_width, font=main_font, anchor=N)
    story_text_message.pack(padx=padding, pady=padding, anchor="center")

    # Next Button
    next_button = ttk.Button(next_button_frame, text="Next", command=print_ip)
    next_button.pack(padx=padding, pady=padding, anchor="center")

    conn.commit()


def save_ch_progress():
    global database
    database = player_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ch_name = ch_edt_ch_name_id_var.get()
    c.execute(f"""SELECT ch_id FROM characters WHERE ch_name = '{ch_name}'""")
    ch_id_raw = c.fetchall()
    ch_id = id.raw_conv(ch_id_raw)[0]

    c.execute(f"""SELECT s_id FROM stories WHERE ch_id = '{ch_id}'""")
    s_id_raw = c.fetchall()
    s_id = id.raw_conv(s_id_raw)[0]

    progress_list.append(s_id)
    progress_list.append(ch_name)

    conn.commit()

    print_story()


def character_select():
    global database
    database = player_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    clear_frame()

    labels_width = 10
    messages_width = 200
    padding = 10

    characters_list_info = []

    try:
        # Get All Info From Characters
        c.execute(
            f"""SELECT ch_name, ch_breed, ch_life, ch_speed, ch_defense, ch_attack, ch_background FROM characters""")
        characters_list_info = c.fetchall()
    except sqlite3.OperationalError:
        print("check character_select in player")

    main_character_frame = Frame(game_frame)
    main_character_frame.pack(fill="both")

    # Scroll Bar stuff
    ch_scroll_bar_frame = Frame(main_character_frame)
    ch_scroll_bar_frame.pack(fill="both", expand=True)

    # Create Canvas
    global ch_canvas
    ch_canvas = Canvas(ch_scroll_bar_frame, height=600)

    # Create ScrollBar
    ch_button_x_scrollbar = Scrollbar(ch_scroll_bar_frame, orient="horizontal", command=ch_canvas.xview)
    ch_button_x_scrollbar.pack(side="bottom", fill="x")

    # Frame To Put Objects in
    inside_character_frame = Frame(ch_canvas)
    inside_character_frame.bind("<Configure>", lambda e: ch_canvas.configure(scrollregion=ch_canvas.bbox("all")))

    # Canvas Config
    ch_canvas.create_window((0, 0), window=inside_character_frame, anchor="nw")
    ch_canvas.configure(xscrollcommand=ch_button_x_scrollbar.set)
    ch_canvas.pack(side="left", fill="both", expand=True)

    select_character_main_frame = LabelFrame(game_frame)
    select_character_main_frame.pack(fill="both", side=BOTTOM)

    select_character_inside_frame = Frame(select_character_main_frame)
    select_character_inside_frame.pack(fill="y")

    for ch in characters_list_info:
        # Frame For each character
        ch_info_frame = LabelFrame(inside_character_frame, text=f'{ch[0]}', font=main_font)
        ch_info_frame.pack(fill="both", side=LEFT)

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

    c.execute(f"""SELECT ch_name FROM characters""")
    ch_new_ch_name_id_ist_raw = c.fetchall()
    ch_new_ch_name_id_list = id.raw_conv(ch_new_ch_name_id_ist_raw)

    global ch_edt_ch_name_id_var
    ch_edt_ch_name_id_var = StringVar()
    ch_edt_ch_name_id_opt_menu_var = ttk.OptionMenu(select_character_inside_frame, ch_edt_ch_name_id_var,
                                                    ch_new_ch_name_id_list[0], *ch_new_ch_name_id_list)
    ch_edt_ch_name_id_opt_menu_var.pack(pady=padding, padx=padding, anchor=NW)

    button_width = 15

    select_button = ttk.Button(select_character_inside_frame, text="Select Character", width=button_width,
                               command=save_ch_progress)
    select_button.pack(padx=padding, pady=padding, anchor=NW)

    conn.commit()


player = Tk()
style_func()
player.title("Story Game")

window_x = player.winfo_screenwidth()-30
window_y = player.winfo_screenheight()-110
player.minsize(window_x, window_y)
player.geometry(f"{window_x}x{window_y}+{10}+{10}")

# Adding the Menus
main_menu = tkinter.Menu(player)

file_menu = tkinter.Menu(main_menu, tearoff=0)
file_menu.add_command(label="Load Story", command=load_story)
file_menu.add_command(label="Save Position In Story", command=None)

options_menu = tkinter.Menu(main_menu, tearoff=0)
options_menu.add_command(label="Dark Mode")
options_menu.add_command(label="Refresh", command=None)
options_menu.add_command(label="Quit", command=None)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Options", menu=options_menu)

# Game Frame
game_frame = LabelFrame(player)
game_frame.pack(fill="both", side=LEFT, expand=True)

# Inventory Frame
inventory_frame = LabelFrame(player, text="Inventory", width=300, font=main_font)
inventory_frame.pack(fill="both", side=RIGHT)

info_message = Message(game_frame, text="LOAD A STORY IN FILE", width=600, font=("Times New Roman", 40))
info_message.place(relx=.5, rely=.5, anchor="center")

player.config(menu=main_menu)
player.mainloop()

