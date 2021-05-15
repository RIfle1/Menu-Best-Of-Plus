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


def save_choice():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS choices
    (s_id text,
    fp_id text,
    p_id text,
    c_id text,
    c_text text)""")

    # im not gonna explain this stuff 0_o
    s_id = s_id_variable.get()
    fp_id = id.fp_id(s_id)
    p_id = c_id_variable.get()
    c_id = get_choice_id_entry.get()
    text_length = len(choice_text_entry.get("1.0", "end"))
    c.execute(f"""SELECT c_id FROM choices WHERE c_id = '{p_id}_{id.c_id(c_id)}'""")
    c_id_raw = c.fetchall()
    d_p_id = id.decoder_2(p_id)[0]

    # I ran out of brain cells for this
    if f'{s_id}' == f'{d_p_id}':
        try:
            c_id = int(c_id)
            if text_length != 1:
                if len(c_id_raw) == 0:
                    if c_id > 0:
                        # Insert into table if that id does not exist
                        c.execute("INSERT INTO choices VALUES (:s_id, :fp_id, :p_id, :c_id, :c_text)",
                                  {
                                      "s_id": f"{s_id}",
                                      "fp_id": f"{fp_id}",
                                      "p_id": f"{p_id}",
                                      "c_id": f"{p_id}_{id.id_conv('c_id', c_id)}",
                                      "c_text": str(choice_text_entry.get("1.0", "end"))
                                  })
                        # Show Success pop-up
                        messagebox.showinfo("Success", f"Choice Number {c_id}\nIn Story Number {id.id_int(s_id)}\nhas been successfully created.")
                    else:
                        messagebox.showerror("Syntax Error", "Choice ID Must Be Positive")
                else:
                    messagebox.showerror("Duplication Error", f"Choice Number {c_id} Already Exists")
            else:
                messagebox.showerror("Input Error", "Choice Text Is Empty")

        except ValueError:
            messagebox.showerror("Syntax Error", "Story ID Must Be A Number")
    else:
        messagebox.showerror("ID Error", f"Paragraph's Story ID is {d_p_id} but Story ID is {s_id}")

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    get_choice_id_entry.delete(0, END)
    choice_text_entry.delete("1.0", "end")


def insert_paragraph():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    p_id = c_id_variable.get()

    # Fetch Information
    c.execute(f"""SELECT fp_text FROM first_paragraphs WHERE fp_id='{p_id}' UNION SELECT p_text FROM paragraphs WHERE p_id='{p_id}'""")
    text_raw = c.fetchall()
    text_1 = ((text_raw[0])[0])

    # Input data into text box
    old_text.set(str(text_1))

    # Decode the ID
    decoded_id_choice.set(id.decoder_3(c_id_variable.get()))

    # End Connection
    conn.commit()
    conn.close()


def new_choice_window():
    global new_choice
    # Create New Window
    new_choice = Toplevel()
    new_choice.title("Create A new Choice")
    screen_x_2 = new_choice.winfo_screenwidth()
    screen_y_2 = new_choice.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 900
    new_choice.minsize(window_x_2, window_y_2)
    new_choice.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    new_choice.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 200
    rest = window_y_2 - frame_height*2
    # Info Frame 1
    info_frame_1 = LabelFrame(new_choice, width=window_x_2, height=frame_height)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(new_choice, width=window_x_2, height=frame_height)
    info_frame_2.pack(fill="both", side=TOP, expand=True)

    # Top Button Frame
    button_frame_1 = LabelFrame(new_choice, height=rest / 2, width=window_x_2)
    button_frame_1.pack(fill="both")

    # Choice Frame
    choice_frame = LabelFrame(new_choice, width=window_x_2, height=frame_height)
    choice_frame.pack(fill="both")

    # Bottom Buttons Frame
    button_frame_2 = LabelFrame(new_choice, height=rest / 2, width=window_x_2)
    button_frame_2.pack(fill="both")

    width = 42
    pad = 10
    # Labels
    get_story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width / 2), anchor=W)
    get_story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    get_pg_id_label = Label(info_frame_1, text="Select Paragraph ID:", width=int(width / 2), anchor=W)
    get_pg_id_label.grid(row=1, column=0, padx=pad, pady=pad, stick="w")

    decode_p_id_label = Label(info_frame_1, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_p_id_label.grid(row=2, column=0, padx=pad, pady=(pad, 200), stick="nw")

    paragraph_text_label = Label(info_frame_2, text="Paragraph Text:", width=int(width / 2), anchor=NW)
    paragraph_text_label.grid(row=2, column=0, padx=pad, pady=pad, stick="nw")

    get_choice_id_label = Label(choice_frame, text="Enter Choice Number:", width=int(width / 2), anchor=NW)
    get_choice_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="nw")

    choice_text_label = Label(choice_frame, text="Choice Text:", width=int(width / 2), anchor=NW)
    choice_text_label.grid(row=1, column=0, padx=(pad, pad+5), pady=pad, stick="nw")

    # Entries
    global choice_text_entry, old_text, get_choice_id_entry, decoded_id_choice
    get_choice_id_entry = Entry(choice_frame, width=49)
    get_choice_id_entry.grid(row=0, column=1, padx=pad, pady=pad)

    choice_text_entry = Text(choice_frame, width=37, height=10)
    choice_text_entry.grid(row=1, column=1, padx=pad, pady=pad)

    # Message Box
    old_text = StringVar()
    show_paragraph_message = Message(info_frame_2, textvariable=old_text, width=280, anchor=NW)
    show_paragraph_message.grid(row=2, column=1, padx=pad, pady=pad, stick="nw")

    decoded_id_choice = StringVar()
    show_decoded_pg_id = Message(info_frame_1, textvariable=decoded_id_choice, width=280, anchor=NW)
    show_decoded_pg_id.grid(row=2, column=1, padx=pad, pady=pad, stick="nw")

    # Buttons
    submit_button = Button(button_frame_1, text="Submit", width=int(width / 2), command=insert_paragraph)
    submit_button.grid(row=0, column=0, padx=pad, pady=pad, ipadx=160)

    save_choice_button = Button(button_frame_2, text="Save Choice", width=int(width / 2), command=save_choice)
    save_choice_button.grid(row=2, column=0, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame_2, text="Cancel", width=width, command=new_choice.destroy)
    cancel_button.grid(row=2, column=1, padx=pad, pady=pad, stick="w")

    def option_s_id_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs UNION SELECT s_id FROM first_paragraphs""")
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
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_p_id_menu():
        global c_id_variable, p_id_list
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT fp_id FROM first_paragraphs 
            UNION SELECT p_id FROM paragraphs
            UNION SELECT fp_id FROM choices""")
        p_id_list_choices_raw = c.fetchall()

        p_id_paragraphs_list = []
        for tp in p_id_list_choices_raw:
            for item in tp:
                p_id_paragraphs_list.append(item)

        p_id_list = p_id_paragraphs_list

        if p_id_list:
            c_id_variable = StringVar()
            c_id_variable.set(p_id_list[0])
            p_id_opmenu = OptionMenu(info_frame_1, c_id_variable, *p_id_list)
            p_id_opmenu.config(width=width)
            p_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_p_id_menu()

    new_choice.mainloop()


# Function to edit choices
def edit_choice():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Update Table
    s_id = s_id_variable.get()
    c_id = c_id_variable.get()
    if len(edit_choice_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE choices SET c_text = :c_text WHERE c_id = :c_id""",
                  {
                      "c_text": edit_choice_entry.get("1.0", "end"),
                      "c_id": f'{c_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Choice Number {id.id_int(c_id)} in Story Number {id.id_int(s_id)} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Choice Text is Empty', icon='warning')

    # Clear the Text Boxes
    edit_choice_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to insert already written choice
def insert_choice():
    # Delete Previous Input
    edit_choice_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_id = c_id_variable.get()

    c.execute(f"""SELECT c_text FROM choices WHERE c_id = '{c_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    edit_choice_entry.insert(END, f'{original_text_2}')

    conn.commit()
    conn.close()


# Function to insert decoded id
def decode_id_edit():
    decode_id_text.set(id.decoder_3(c_id_variable.get()))


# Function to open edit window
def edit_choices_window():
    global edit_choices
    # Create New Window
    edit_choices = Toplevel()
    edit_choices.title("Edit Choices")
    screen_x_2 = edit_choices.winfo_screenwidth()
    screen_y_2 = edit_choices.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 620
    edit_choices.minsize(window_x_2, window_y_2)
    edit_choices.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    edit_choices.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 57

    # Info Frame 1
    info_frame_1 = LabelFrame(edit_choices, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(edit_choices, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(edit_choices, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame 4
    info_frame_4 = LabelFrame(edit_choices, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    button_frame = LabelFrame(edit_choices, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    entry_width = 37
    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Choice ID:", width=int(width / 2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    decode_id_label_text = Label(info_frame_2, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_id_label_text.grid(row=0, column=0, padx=pad, pady=(pad, 180), stick="nw")

    edit_int_par_label = Label(info_frame_4, text="Edit Choice:", width=int(width / 2) - 1, anchor=NW)
    edit_int_par_label.grid(row=0, column=0, padx=pad, pady=pad, stick="nw")

    global decode_id_text
    decode_id_text = StringVar()
    decode_id_label = Message(info_frame_2, textvariable=decode_id_text, width=280, anchor=NW)
    decode_id_label.grid(row=0, column=1, padx=pad, pady=pad, stick="nw")

    # Text
    global edit_choice_entry
    edit_choice_entry = Text(info_frame_4, width=entry_width, height=10)
    edit_choice_entry.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    submit_id_button = Button(info_frame_3, text="Decode ID", width=int(width / 2), command=decode_id_edit)
    submit_id_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w", ipadx=157)

    width_buttons = 19
    save_choice_button = Button(button_frame, text="Save Changes", width=width_buttons, command=edit_choice)
    save_choice_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    load_choice_button = Button(button_frame, text="Load Choice", width=width_buttons, command=insert_choice)
    load_choice_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=edit_choices.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    def option_s_id_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices""")
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
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_c_id_menu():
        global c_id_variable
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices """)
        c_id_list_paragraphs_raw = c.fetchall()

        c_id_paragraphs_list = []
        for tp in c_id_list_paragraphs_raw:
            for item in tp:
                c_id_paragraphs_list.append(item)

        c_id_list = c_id_paragraphs_list

        if c_id_list:
            c_id_variable = StringVar()
            c_id_variable.set(c_id_list[0])
            p_id_opmenu = OptionMenu(info_frame_1, c_id_variable, *c_id_list)
            p_id_opmenu.config(width=width)
            p_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_c_id_menu()

    edit_choices.mainloop()


# Function to delete a story from the delete window
def delete_choice():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    s_id = s_id_variable.get()
    c_id = c_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Choice Number {id.id_int(c_id)}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM paragraphs WHERE c_id LIKE '{c_id}%'""")
        c.execute(f"""DELETE FROM choices WHERE c_id LIKE '{c_id}%'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Choice Number {id.id_int(c_id)} In Story Number {id.id_int(s_id)}\nhas been successfully deleted."
                                       f"\nAll Choices and Paragraphs connected to Choice Number {id.id_int(c_id)} were also Deleted.")
        del_text.set("")
        decode_id_text.set("")

    conn.commit()
    conn.close()

    option_s_id_menu()
    option_c_id_menu()


# Function to insert old text in a label in the delete story window
def insert_del():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_id = c_id_variable.get()

    c.execute(f"""SELECT c_text FROM choices WHERE c_id = '{c_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    del_text.set(str(original_text_2))

    conn.commit()
    conn.close()


# Function to decode id in delete choice window
def decode_id_del():
    decode_id_text.set(id.decoder_3(c_id_variable.get()))


# Function to open delete window
def delete_choice_window():
    global del_choices
    del_choices = Toplevel()
    del_choices.title("Delete A Choice")
    screen_x_2 = del_choices.winfo_screenwidth()
    screen_y_2 = del_choices.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 650
    del_choices.minsize(window_x_2, window_y_2)
    del_choices.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    del_choices.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame 1
    info_frame_1 = LabelFrame(del_choices, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(del_choices, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(del_choices, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame
    info_frame_4 = LabelFrame(del_choices, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Bottom Frame
    button_frame = LabelFrame(del_choices, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width / 2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    c_id_label = Label(info_frame_1, text="Select Choice ID:", width=int(width/2), anchor=W)
    c_id_label.grid(row=1, column=0, padx=pad, pady=pad, stick="w")

    text_label = Label(info_frame_4, text="Choice Text:", width=int(width/2), anchor=NW)
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
    delete_text_button = Button(button_frame, text="Delete Choice", width=width_buttons, command=delete_choice)
    delete_text_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    check_text_button = Button(button_frame, text="Check Choice Text", width=width_buttons, command=insert_del)
    check_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=del_choices.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

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
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_s_id_menu()

    def option_c_id_menu():
        global c_id_variable
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices """)
        c_id_list_paragraphs_raw = c.fetchall()

        c_id_paragraphs_list = []
        for tp in c_id_list_paragraphs_raw:
            for item in tp:
                c_id_paragraphs_list.append(item)

        c_id_list = c_id_paragraphs_list

        if c_id_list:
            c_id_variable = StringVar()
            c_id_variable.set(c_id_list[0])
            c_id_opmenu = OptionMenu(info_frame_1, c_id_variable, *c_id_list)
            c_id_opmenu.config(width=width)
            c_id_opmenu.grid(row=1, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            new_choice.destroy()

        conn.commit()
        conn.close()

    option_c_id_menu()

    del_choices.mainloop()








