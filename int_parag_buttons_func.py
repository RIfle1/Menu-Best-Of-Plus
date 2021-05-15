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


def save_int_paragraph_window():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS first_paragraphs
    (s_id text, 
    fp_id text,
    fp_text text)""")

    s_id = fp_id_variable.get()
    fp_id = id.id_conv('fp_id', id.id_int(s_id))
    text_length = len(paragraph_text_entry.get("1.0", "end"))

    if text_length != 1:
        # Insert into table if that id does not exist
        c.execute("INSERT INTO first_paragraphs VALUES (:s_id, :fp_id, :fp_text)",
                  {
                      "s_id": f"{s_id}",
                      "fp_id": f"{s_id}_{fp_id}",
                      "fp_text": str(paragraph_text_entry.get("1.0", "end"))
                  })
        # Show Success pop-up
        messagebox.showinfo("Success", f"First Paragraph of Story {id.id_int(s_id)} has been successfully created.")
    else:
        messagebox.showerror("Input Error", "Story Text Is Empty")

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    paragraph_text_entry.delete("1.0", "end")

    option_int_par_menu()


def insert_int_paragraph():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_id = fp_id_variable.get()

    # Fetch Information
    c.execute(f"""SELECT s_text FROM stories WHERE s_id='{s_id}'""")
    text_raw = c.fetchall()
    text_1 = ((text_raw[0])[0])

    # Input data into text box
    old_text.set(str(text_1))

    # End Connection
    conn.commit()
    conn.close()


def int_paragraph_window():
    global new_int_pg
    # Create New Window
    new_int_pg = Toplevel()
    new_int_pg.title("Create An Initial Paragraph")
    screen_x_2 = new_int_pg.winfo_screenwidth()
    screen_y_2 = new_int_pg.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 800
    new_int_pg.minsize(window_x_2, window_y_2)
    new_int_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    new_int_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 200
    rest = window_y_2 - frame_height*2
    # Story Frame 1
    story_frame_1 = LabelFrame(new_int_pg, width=window_x_2, height=frame_height)
    story_frame_1.pack(fill="both", side=TOP)

    # Story Frame 2
    story_frame_2 = LabelFrame(new_int_pg, width=window_x_2, height=frame_height)
    story_frame_2.pack(fill="both", side=TOP, expand=True)

    # Top Button Frame
    button_frame_1 = LabelFrame(new_int_pg, height=rest / 2, width=window_x_2)
    button_frame_1.pack(fill="both")

    # Paragraph Frame
    paragraph_frame = LabelFrame(new_int_pg, width=window_x_2, height=frame_height)
    paragraph_frame.pack(fill="both")

    # Bottom Buttons Frame
    button_frame = LabelFrame(new_int_pg, height=rest / 2, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10
    # Labels
    get_story_id_label = Label(story_frame_1, text="From Story Number:", width=int(width / 2), anchor=W)
    get_story_id_label.grid(row=0, column=0, padx=(10, 13), pady=pad, stick="w")

    story_text_label = Label(story_frame_2, text="Story Text:", width=int(width / 2), anchor=NW)
    story_text_label.grid(row=1, column=0, padx=pad, pady=pad, stick="nw")

    paragraph_text_label = Label(paragraph_frame, text="Initial Paragraph Text:", width=int(width / 2), anchor=NW)
    paragraph_text_label.grid(row=0, column=0, padx=(10, 13), pady=pad, stick="nw")

    # Entries
    global paragraph_text_entry, old_text
    paragraph_text_entry = Text(paragraph_frame, width=37, height=20)
    paragraph_text_entry.grid(row=0, column=1, padx=pad, pady=pad)

    # Message Box
    old_text = StringVar()
    show_story_message = Message(story_frame_2, textvariable=old_text, width=280, anchor=W)
    show_story_message.grid(row=1, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    submit_button = Button(button_frame_1, text="Submit", width=int(width / 2), command=insert_int_paragraph)
    submit_button.grid(row=0, column=0, padx=pad, pady=pad, ipadx=160)

    save_story_button = Button(button_frame, text="Save Initial Paragraph", width=int(width / 2), command=save_int_paragraph_window)
    save_story_button.grid(row=2, column=0, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width, command=new_int_pg.destroy)
    cancel_button.grid(row=2, column=1, padx=pad, pady=pad, stick="w")
    global option_int_par_menu

    def option_int_par_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories""")
        s_id_list_stories_raw = c.fetchall()
        s_id_stories_list = []
        for tp in s_id_list_stories_raw:
            for item in tp:
                s_id_stories_list.append(item)

        c.execute("""SELECT s_id FROM first_paragraphs""")
        s_id_list_int_pg_raw = c.fetchall()
        s_id_int_pg_list = []
        for tp in s_id_list_int_pg_raw:
            for item in tp:
                s_id_int_pg_list.append(item)

        for item in s_id_int_pg_list:
            s_id_stories_list.remove(item)

        s_id_list = s_id_stories_list

        if s_id_list:
            global fp_id_variable
            fp_id_variable = StringVar()
            fp_id_variable.set(s_id_list[0])
            story_id_del_opmenu = OptionMenu(story_frame_1, fp_id_variable, *s_id_list)
            story_id_del_opmenu.config(width=width)
            story_id_del_opmenu.grid(row=0, column=1, pady=pad, padx=pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            new_int_pg.destroy()

        conn.commit()
        conn.close()

    option_int_par_menu()

    new_int_pg.mainloop()


# Function to edit stories
def edit_initial_pg():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Update Table
    fp_id = id_var.get()
    if len(edit_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE first_paragraphs SET fp_text = :fp_text WHERE fp_id = :fp_id""",
                  {
                      "fp_text": edit_text_entry.get("1.0", "end"),
                      "fp_id": f'{fp_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Initial Paragraph Number {fp_id} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Initial Paragraph Text is Empty', icon='warning')

    # Clear the Text Boxes
    edit_text_entry.delete("1.0", "end")

    conn.commit()
    conn.close()

    option_edit_menu()


# Function to insert already written text
def insert_edit():
    # Delete Previous Input
    edit_text_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    fp_id = id_var.get()

    c.execute(f"""SELECT fp_text FROM first_paragraphs WHERE fp_id = '{fp_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    edit_text_entry.insert(END, f'{original_text_2}')

    conn.commit()
    conn.close()


# Function to insert decoded id
def decode_id_edit():
    decode_id_text.set(id.decoder_3(id_var.get()))


# Function to open edit window
def edit_int_par_window():
    global edit_int_pg
    # Create New Window
    edit_int_pg = Toplevel()
    edit_int_pg.title("Edit Initial Paragraph")
    screen_x_2 = edit_int_pg.winfo_screenwidth()
    screen_y_2 = edit_int_pg.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 560
    edit_int_pg.minsize(window_x_2, window_y_2)
    edit_int_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    edit_int_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 57

    # Info Frame 1
    info_frame_1 = LabelFrame(edit_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(edit_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(edit_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame 4
    info_frame_4 = LabelFrame(edit_int_pg, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    button_frame = LabelFrame(edit_int_pg, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    entry_width = 37
    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Initial Paragraph ID:", width=int(width / 2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    decode_id_label_text = Label(info_frame_2, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_id_label_text.grid(row=0, column=0, padx=pad, pady=(pad, 40), stick="nw")

    edit_int_par_label = Label(info_frame_4, text="Edit Initial Paragraph:", width=int(width / 2) - 1, anchor=NW)
    edit_int_par_label.grid(row=0, column=0, padx=pad, pady=pad, stick="nw")

    global decode_id_text
    decode_id_text = StringVar()
    decode_id_label = Message(info_frame_2, textvariable=decode_id_text, width=280, anchor=NW)
    decode_id_label.grid(row=0, column=1, padx=pad, pady=pad, stick="nw")

    # Text
    global edit_text_entry
    edit_text_entry = Text(info_frame_4, width=entry_width, height=19)
    edit_text_entry.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    submit_id_button = Button(info_frame_3, text="Decode ID", width=int(width / 2), command=decode_id_edit)
    submit_id_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w", ipadx=157)

    width_buttons = 19
    save_int_pg_button = Button(button_frame, text="Save Changes", width=width_buttons, command=edit_initial_pg)
    save_int_pg_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    load_text_button = Button(button_frame, text="Load Initial Paragraph", width=width_buttons, command=insert_edit)
    load_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=edit_int_pg.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    global option_edit_menu

    def option_edit_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT fp_id FROM first_paragraphs""")
        fp_id_list_raw = c.fetchall()
        fp_id_list = []
        for tp in fp_id_list_raw:
            for item in tp:
                fp_id_list.append(item)

        if fp_id_list:
            global id_var
            id_var = StringVar()
            id_var.set(fp_id_list[0])
            story_id_del_opmenu = OptionMenu(info_frame_1, id_var, *fp_id_list)
            story_id_del_opmenu.config(width=width - 1)
            story_id_del_opmenu.grid(row=0, column=1, ipadx=pad, pady=pad, stick="w")

        else:
            messagebox.showerror("Index Error", "No Existing Initial Paragraphs Found")
            edit_int_pg.destroy()

        conn.commit()
        conn.close()

    option_edit_menu()

    edit_int_pg.mainloop()


# Function to delete a story from the delete window
def delete_int_pg():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    fp_id = fp_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Initial Paragraph Number {fp_id}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM first_paragraphs WHERE fp_id = '{fp_id}'""")
        c.execute(f"""DELETE FROM paragraphs WHERE s_id = '{id.id_conv('s_id', id.id_int(fp_id))}'""")
        c.execute(f"""DELETE FROM choices WHERE s_id = '{id.id_conv('s_id', id.id_int(fp_id))}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Initial Paragraph Number {id.id_int(fp_id)} In Story Number {id.id_int(fp_id)}\nhas been successfully deleted."
                                       f"\nAll Paragraphs And Choices Were Also Deleted From Initial Paragraph Number {id.id_int(fp_id)}.")
        del_text.set("")
        decode_id_text.set("")

    conn.commit()
    conn.close()

    option_del_menu()


# Function to insert old text in a label in the delete story window
def insert_del():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    fp_id = fp_id_variable.get()

    c.execute(f"""SELECT fp_text FROM first_paragraphs WHERE fp_id = '{fp_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    del_text.set(str(original_text_2))

    conn.commit()
    conn.close()


# Decode id Function for the delete window
def decode_id_del():
    decode_id_text.set(id.decoder_3(fp_id_variable.get()))


# Function to open delete window
def delete_int_pg_window():
    global del_int_pg
    # Create New Window
    del_int_pg = Toplevel()
    del_int_pg.title("Delete An Initial Paragraph")
    screen_x_2 = del_int_pg.winfo_screenwidth()
    screen_y_2 = del_int_pg.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 500
    del_int_pg.minsize(window_x_2, window_y_2)
    del_int_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    del_int_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame 1
    info_frame_1 = LabelFrame(del_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    info_frame_2 = LabelFrame(del_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    info_frame_3 = LabelFrame(del_int_pg, height=info_frame_height, width=window_x_2)
    info_frame_3.pack(fill="both", side=TOP)

    # Info Frame
    info_frame_4 = LabelFrame(del_int_pg, height=frame_height, width=window_x_2)
    info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Bottom Frame
    button_frame = LabelFrame(del_int_pg, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10

    # Labels
    fp_id_label = Label(info_frame_1, text="Select Initial Paragraph ID:", width=int(width/2), anchor=W)
    fp_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    text_label = Label(info_frame_4, text="Initial Paragraph Text:", width=int(width/2), anchor=NW)
    text_label.grid(row=1, column=0, padx=pad, pady=pad, stick="nw")

    decode_id_label_text = Label(info_frame_2, text="Decoded ID:", width=int(width / 2), anchor=NW)
    decode_id_label_text.grid(row=0, column=0, padx=pad, pady=(pad, 40), stick="nw")

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
    delete_text_button = Button(button_frame, text="Delete Initial Paragraph", width=width_buttons, command=delete_int_pg)
    delete_text_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    check_text_button = Button(button_frame, text="Check Initial Paragraph", width=width_buttons, command=insert_del)
    check_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=del_int_pg.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    global option_del_menu

    def option_del_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT fp_id FROM first_paragraphs""")
        fp_id_list_raw = c.fetchall()
        fp_id_list = []
        for tp in fp_id_list_raw:
            for item in tp:
                fp_id_list.append(item)

        if fp_id_list:
            global fp_id_variable
            fp_id_variable = StringVar()
            fp_id_variable.set(fp_id_list[0])
            fp_id_del_opmenu = OptionMenu(info_frame_1, fp_id_variable, *fp_id_list)
            fp_id_del_opmenu.config(width=width)
            fp_id_del_opmenu.grid(row=0, column=1, ipadx=pad, pady=pad, stick="w")

        else:
            messagebox.showerror("Index Error", "No Existing Initial Paragraphs were Found")
            del_int_pg.destroy()

        conn.commit()
        conn.close()

    option_del_menu()

    del_int_pg.mainloop()




