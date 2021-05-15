# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id
import widget_func


def save_paragraph():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs
    (s_id text,
    c_id text,
    p_id text,
    p_text text)""")

    # im not gonna explain this stuff 0_o
    s_id = s_id_variable.get()
    c_id = p_id_variable.get()
    print(id.decoder_2(c_id)[-2])
    p_id = int(id.id_int(id.decoder_2(c_id)[-2])) + 1

    text_length = len(paragraph_text_entry.get("1.0", "end"))
    c.execute(f"""SELECT p_id FROM paragraphs WHERE p_id = '{c_id}_{id.p_id(p_id)}'""")
    p_id_raw = c.fetchall()
    c_p_id = id.decoder_2(c_id)[0]

    # I ran out of brain cells for this
    if f'{s_id}' == f'{c_p_id}':
        try:
            p_id = int(p_id)
            if text_length != 1:
                if len(p_id_raw) == 0:
                    # Insert into table if that id does not exist
                    c.execute("INSERT INTO paragraphs VALUES (:s_id, :c_id, :p_id, :p_text)",
                              {
                                  "s_id": f"{s_id}",
                                  "c_id": f"{c_id}",
                                  "p_id": f"{c_id}_{id.id_conv('p_id', p_id)}",
                                  "p_text": str(paragraph_text_entry.get("1.0", "end"))
                              })
                    # Show Success pop-up
                    messagebox.showinfo("Success",
                                        f"Paragraph Number {p_id}\nIn Story Number {id.id_int(s_id)}\nhas been successfully created.")
                else:
                    messagebox.showerror("Duplication Error", f"Paragraph Number {p_id} Already Exists")
            else:
                messagebox.showerror("Input Error", "Paragraph Text Is Empty")

        except ValueError:
            messagebox.showerror("Syntax Error", "Paragraph ID Must Be A Number")
    else:
        messagebox.showerror("ID Error", f"Choice's Story ID is {c_p_id} but Story ID is {s_id}")

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    paragraph_text_entry.delete("1.0", "end")

    option_s_id_menu()
    option_c_id_menu()


def insert_choices():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_id = p_id_variable.get()

    # Fetch Information
    c.execute(f"""SELECT c_text FROM choices WHERE c_id='{c_id}'""")
    text_raw = c.fetchall()
    text_1 = ((text_raw[0])[0])

    # Input data into text box
    choice_message.set(str(text_1))

    # Decode the ID
    decoded_id_choice.set(id.decoder_3(p_id_variable.get()))

    # End Connection
    conn.commit()
    conn.close()


def new_pg_window():
    global new_pg
    # Create New Window
    new_pg = Toplevel()
    new_pg.title("Create A New Paragraph")
    screen_x_2 = new_pg.winfo_screenwidth()
    screen_y_2 = new_pg.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 820
    new_pg.minsize(window_x_2, window_y_2)
    new_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    new_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 200
    rest = window_y_2 - frame_height*2
    # Info Frame 1
    info_frame_1 = LabelFrame(new_pg, width=window_x_2, height=frame_height)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(new_pg, width=window_x_2, height=frame_height)
    info_frame_2.pack(fill="both", side=TOP)

    # Top Button Frame
    button_frame_1 = LabelFrame(new_pg, height=rest / 2, width=window_x_2)
    button_frame_1.pack(fill="both")

    # Choice Frame
    paragraph_frame = LabelFrame(new_pg, width=window_x_2, height=frame_height)
    paragraph_frame.pack(fill="both", expand=True)

    # Bottom Buttons Frame
    button_frame_2 = LabelFrame(new_pg, height=rest / 2, width=window_x_2)
    button_frame_2.pack(fill="both")

    width = 42
    pad = 10
    # Labels
    get_story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width / 2), anchor=W)
    get_story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    get_choice_id_label = Label(info_frame_1, text="Select Choice ID:", width=int(width / 2), anchor=W)
    get_choice_id_label.grid(row=1, column=0, padx=pad, pady=pad, stick="w")

    decode_c_id_label = Label(info_frame_1, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_c_id_label.grid(row=2, column=0, padx=pad, pady=(pad, 100), stick="nw")

    choice_text_label = Label(info_frame_2, text="Choice Text:", width=int(width / 2), anchor=NW)
    choice_text_label.grid(row=2, column=0, padx=pad, pady=(pad, 100), stick="nw")

    paragraph_text_label = Label(paragraph_frame, text="Paragraph Text:", width=int(width / 2), anchor=NW)
    paragraph_text_label.grid(row=1, column=0, padx=(pad, pad+5), pady=pad, stick="nw")

    # Entries
    global paragraph_text_entry, choice_message, decoded_id_choice

    paragraph_text_entry = Text(paragraph_frame, width=37, height=20)
    paragraph_text_entry.grid(row=1, column=1, padx=pad, pady=pad)

    # Message Box
    choice_message = StringVar()
    show_choice_message = Message(info_frame_2, textvariable=choice_message, width=280, anchor=NW)
    show_choice_message.grid(row=2, column=1, padx=pad, pady=pad, stick="nw")

    decoded_id_choice = StringVar()
    show_decoded_pg_id = Message(info_frame_1, textvariable=decoded_id_choice, width=280, anchor=NW)
    show_decoded_pg_id.grid(row=2, column=1, padx=pad, pady=pad, stick="nw")

    # Buttons
    submit_button = Button(button_frame_1, text="Submit", width=int(width / 2), command=insert_choices)
    submit_button.grid(row=0, column=0, padx=pad, pady=pad, ipadx=160)

    save_choice_button = Button(button_frame_2, text="Save Paragraph", width=int(width / 2), command=save_paragraph)
    save_choice_button.grid(row=2, column=0, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame_2, text="Cancel", width=width, command=new_pg.destroy)
    cancel_button.grid(row=2, column=1, padx=pad, pady=pad, stick="w")

    global option_s_id_menu, option_c_id_menu

    def option_s_id_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices""")
        s_id_list_paragraphs_raw = c.fetchall()

        s_id_paragraphs_list = []
        for tp in s_id_list_paragraphs_raw:
            for item in tp:
                s_id_paragraphs_list.append(item)

        s_id_list = s_id_paragraphs_list

        if s_id_list:
            global s_id_variable
            s_id_variable = StringVar()
            s_id_variable.set(s_id_list[0])
            s_id_opmenu = OptionMenu(info_frame_1, s_id_variable, *s_id_list)
            s_id_opmenu.config(width=width)
            s_id_opmenu.grid(row=0, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_c_id_menu():
        global p_id_variable, c_id_list
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices""")
        c_id_list_paragraphs_raw = c.fetchall()
        c_id_choices_list = []
        for tp in c_id_list_paragraphs_raw:
            for item in tp:
                c_id_choices_list.append(item)

        c.execute(f"""SELECT c_id FROM paragraphs""")
        c_id_list_paragraphs_raw = c.fetchall()
        c_id_paragraphs_list = []
        for tp in c_id_list_paragraphs_raw:
            for item in tp:
                c_id_paragraphs_list.append(item)

        for item in c_id_paragraphs_list:
            c_id_choices_list.remove(item)

        c_id_list = c_id_choices_list

        if c_id_list:
            p_id_variable = StringVar()
            p_id_variable.set(c_id_list[0])
            c_id_opmenu = OptionMenu(info_frame_1, p_id_variable, *c_id_list)
            c_id_opmenu.config(width=width)
            c_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choice were Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_c_id_menu()

    new_pg.mainloop()


# Function to edit choices
def edit_paragraph():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Update Table
    s_id = s_id_variable.get()
    p_id = p_id_variable.get()
    if len(edit_paragraph_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE paragraphs SET p_text = :p_text WHERE p_id = :p_id""",
                  {
                      "p_text": edit_paragraph_entry.get("1.0", "end"),
                      "p_id": f'{p_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Paragraph Number {id.id_int(p_id)} in Story Number {id.id_int(s_id)} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Paragraph Text is Empty', icon='warning')

    # Clear the Text Boxes
    edit_paragraph_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to insert already written choice
def insert_paragraph():
    # Delete Previous Input
    edit_paragraph_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    p_id = p_id_variable.get()

    c.execute(f"""SELECT p_text FROM paragraphs WHERE p_id = '{p_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    edit_paragraph_entry.insert(END, f'{original_text_2}')

    conn.commit()
    conn.close()


# Function to insert decoded id
def decode_id_edit():
    decode_id_text.set(id.decoder_3(p_id_variable.get()))


# Function to open edit window
def edit_pg_window():
    global edit_pg
    # Create New Window
    edit_pg = Toplevel()
    edit_pg.title("Edit Paragraphs")
    screen_x_2 = edit_pg.winfo_screenwidth()
    screen_y_2 = edit_pg.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 620
    edit_pg.minsize(window_x_2, window_y_2)
    edit_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    edit_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 57

    # Info Frame 1
    info_frame_1 = LabelFrame(edit_pg, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(edit_pg, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(edit_pg, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame 4
    info_frame_4 = LabelFrame(edit_pg, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    button_frame = LabelFrame(edit_pg, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    entry_width = 37
    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Choice ID:", width=int(width / 2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    decode_id_label_text = Label(info_frame_2, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_id_label_text.grid(row=0, column=0, padx=pad, pady=(pad, 180), stick="nw")

    edit_par_label = Label(info_frame_4, text="Edit Paragraph:", width=int(width / 2) - 1, anchor=NW)
    edit_par_label.grid(row=0, column=0, padx=pad, pady=pad, stick="nw")

    global decode_id_text
    decode_id_text = StringVar()
    decode_id_label = Message(info_frame_2, textvariable=decode_id_text, width=280, anchor=NW)
    decode_id_label.grid(row=0, column=1, padx=pad, pady=pad, stick="nw")

    # Text
    global edit_paragraph_entry
    edit_paragraph_entry = Text(info_frame_4, width=entry_width, height=10)
    edit_paragraph_entry.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    submit_id_button = Button(info_frame_3, text="Decode ID", width=int(width / 2), command=decode_id_edit)
    submit_id_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w", ipadx=157)

    width_buttons = 19
    save_paragraph_button = Button(button_frame, text="Save Changes", width=width_buttons, command=edit_paragraph)
    save_paragraph_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    load_paragraphs_button = Button(button_frame, text="Load Choice", width=width_buttons, command=insert_paragraph)
    load_paragraphs_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=edit_pg.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    def option_s_id_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs UNION SELECT s_id FROM paragraphs""")
        s_id_list_raw = c.fetchall()

        s_id_list = []
        for tp in s_id_list_raw:
            for item in tp:
                s_id_list.append(item)

        if s_id_list:
            global s_id_variable
            s_id_variable = StringVar()
            s_id_variable.set(s_id_list[0])
            s_id_opmenu = OptionMenu(info_frame_1, s_id_variable, *s_id_list)
            s_id_opmenu.config(width=width)
            s_id_opmenu.grid(row=0, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_p_id_menu():
        global p_id_variable
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT p_id FROM paragraphs""")
        p_id_list_raw = c.fetchall()

        p_id_list = []
        for tp in p_id_list_raw:
            for item in tp:
                p_id_list.append(item)

        if p_id_list:
            p_id_variable = StringVar()
            p_id_variable.set(p_id_list[0])
            p_id_opmenu = OptionMenu(info_frame_1, p_id_variable, *p_id_list)
            p_id_opmenu.config(width=width)
            p_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Paragraphs Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_p_id_menu()

    edit_pg.mainloop()


# Function to delete a story from the delete window
def delete_pg():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    s_id = s_id_variable.get()
    p_id = p_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Paragraph Number {id.id_int(p_id)}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM paragraphs WHERE p_id LIKE '{p_id}%'""")
        c.execute(f"""DELETE FROM choices WHERE p_id LIKE '{p_id}%'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Paragraph Number {id.id_int(p_id)} In Story Number {id.id_int(s_id)}\nhas been successfully deleted."
                                       f"\nAll Paragraphs and Choices connected to Paragraph Number {id.id_int(p_id)} were also Deleted.")
        del_text.set("")
        decode_id_text.set("")

    conn.commit()
    conn.close()

    option_s_id_menu()
    option_p_id_menu()


# Function to insert old text in a label in the delete story window
def insert_del():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    p_id = p_id_variable.get()

    c.execute(f"""SELECT p_text FROM paragraphs WHERE p_id = '{p_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    del_text.set(str(original_text_2))

    conn.commit()
    conn.close()


# Function to decode id in delete choice window
def decode_id_del():
    decode_id_text.set(id.decoder_3(p_id_variable.get()))


# Function to open delete window
def delete_pg_window():
    global del_pg
    del_pg = Toplevel()
    del_pg.title("Delete A Paragraph")
    screen_x_2 = del_pg.winfo_screenwidth()
    screen_y_2 = del_pg.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 650
    del_pg.minsize(window_x_2, window_y_2)
    del_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    del_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame 1
    info_frame_1 = LabelFrame(del_pg, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(del_pg, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(del_pg, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame
    info_frame_4 = LabelFrame(del_pg, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Bottom Frame
    button_frame = LabelFrame(del_pg, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width / 2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    p_id_label = Label(info_frame_1, text="Select Paragraph ID:", width=int(width/2), anchor=W)
    p_id_label.grid(row=1, column=0, padx=pad, pady=pad, stick="w")

    text_label = Label(info_frame_4, text="Paragraph Text:", width=int(width/2), anchor=NW)
    text_label.grid(row=1, column=0, padx=pad, pady=pad, stick="nw")

    decode_id_label_text = Label(info_frame_2, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_id_label_text.grid(row=0, column=0, padx=pad, pady=(pad, 180), stick="nw")

    # Message Box
    global del_text
    del_text = StringVar()
    story_del_message = Message(info_frame_4, textvariable=del_text, width=280, anchor=W)
    story_del_message.grid(row=1, column=1, padx=pad, pady=pad, stick="w")

    global decode_id_text
    decode_id_text = StringVar()
    decode_id_label = Message(info_frame_2, textvariable=decode_id_text, width=280, anchor=NW)
    decode_id_label.grid(row=0, column=1, padx=pad, pady=pad, stick="nw")

    # Buttons
    submit_id_button = Button(info_frame_3, text="Decode ID", width=int(width / 2), command=decode_id_del)
    submit_id_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w", ipadx=157)

    width_buttons = 19
    delete_text_button = Button(button_frame, text="Delete Paragraph", width=width_buttons, command=delete_pg)
    delete_text_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    check_text_button = Button(button_frame, text="Check Paragraph Text", width=width_buttons, command=insert_del)
    check_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=del_pg.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    global option_s_id_menu, option_p_id_menu

    def option_s_id_menu():
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs UNION SELECT s_id FROM paragraphs""")
        s_id_list_raw = c.fetchall()

        s_id_list = []
        for tp in s_id_list_raw:
            for item in tp:
                s_id_list.append(item)

        if s_id_list:
            global s_id_variable
            s_id_variable = StringVar()
            s_id_variable.set(s_id_list[0])
            s_id_opmenu = OptionMenu(info_frame_1, s_id_variable, *s_id_list)
            s_id_opmenu.config(width=width)
            s_id_opmenu.grid(row=0, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_p_id_menu():
        global p_id_variable
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT p_id FROM paragraphs""")
        p_id_list_raw = c.fetchall()

        p_id_list = []
        for tp in p_id_list_raw:
            for item in tp:
                p_id_list.append(item)

        if p_id_list:
            p_id_variable = StringVar()
            p_id_variable.set(p_id_list[0])
            p_id_opmenu = OptionMenu(info_frame_1, p_id_variable, *p_id_list)
            p_id_opmenu.config(width=width)
            p_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            new_pg.destroy()

        conn.commit()
        conn.close()

    option_p_id_menu()

    del_pg.mainloop()








