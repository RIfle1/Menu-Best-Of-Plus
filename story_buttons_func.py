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


# Function to save new stories
def save_story():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS stories
    (s_id text, 
    s_text text)""")

    s_id = story_id_entry.get()
    text_length = len(beginning_story_entry.get("1.0", "end"))
    c.execute(f"""SELECT s_id FROM stories WHERE s_id = '{id.id_conv('s_id', s_id)}'""")
    s_id_raw = c.fetchall()
    print(text_length)

    if text_length != 1:
        if len(s_id_raw) == 0:
            try:
                s_id = int(story_id_entry.get())
                if s_id > 0:
                    # Insert into table if that id does not exist
                    c.execute(
                        "INSERT INTO stories VALUES (:s_id, :s_text)",
                        {
                            "s_id": f"{id.s_id(s_id)}",
                            "s_text": str(beginning_story_entry.get("1.0", "end"))
                        })
                    # Show Success pop-up
                    messagebox.showinfo("Success", f"Story Number {s_id} has been successfully created.")

                else:
                    messagebox.showerror("Syntax Error", "Story ID Must Be Positive", icon='warning')

            except ValueError:
                messagebox.showerror("Syntax Error", "Story ID Must Be A Number", icon='warning')

        else:
            messagebox.showerror("Duplication Error", f"Story Number {s_id} Already Exists", icon='warning')

    else:
        messagebox.showerror("Input Error", "Story Text Is Empty", icon='warning')

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    story_id_entry.delete(0, END)
    beginning_story_entry.delete("1.0", "end")


# Function for new story window
def new_story_window():
    global top_new_st
    # Create New Window
    top_new_st = Toplevel()
    top_new_st.title("Create A New Story")
    screen_x_2 = top_new_st.winfo_screenwidth()
    screen_y_2 = top_new_st.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 500
    top_new_st.minsize(window_x_2, window_y_2)
    top_new_st.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top_new_st.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Main Frame
    main_frame = LabelFrame(top_new_st, height=window_y_2, width=window_x_2)
    main_frame.pack(fill="both", expand=True)

    width = 42
    height = 10
    # Labels
    story_id_label = Label(main_frame, text="Story Number:", width=int(width/2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=height, pady=height, stick="w")

    beginning_label = Label(main_frame, text="Beginning Text:", width=int(width/2), anchor=NW)
    beginning_label.grid(row=1, column=0, padx=height, pady=height, stick="nw")

    # Entries
    global story_id_entry, beginning_story_entry
    story_id_entry = Entry(main_frame, width=48)
    story_id_entry.grid(row=0, column=1, padx=height, pady=height)

    beginning_story_entry = Text(main_frame, width=36)
    beginning_story_entry.grid(row=1, column=1, padx=height, pady=height)

    # Buttons
    save_story_button = Button(main_frame, text="Save Story", width=int(width/2), command=save_story)
    save_story_button.grid(row=2, column=0, padx=height, pady=height, stick="w")

    cancel_button = Button(main_frame, text="Cancel", width=width, command=top_new_st.destroy)
    cancel_button.grid(row=2, column=1, padx=height, pady=height, stick="w")

    top_new_st.mainloop()


# Function to edit stories
def edit_story():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Update Table
    s_id = s_id_variable.get()
    if len(edit_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE stories SET s_text = :s_text WHERE s_id = :s_id""",
                  {
                      "s_text": edit_text_entry.get("1.0", "end"),
                      "s_id": f'{s_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {s_id} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Story Text is Empty', icon='warning')

    # Clear the Text Boxes
    edit_text_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to insert already written text
def insert_edit():
    # Delete Previous Input
    edit_text_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_id = s_id_variable.get()

    c.execute(f"""SELECT s_text FROM stories WHERE s_id = '{s_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    edit_text_entry.insert(END, f'{original_text_2}')

    conn.commit()
    conn.close()


# Function to open edit window
def edit_story_window():
    global top_new_ed
    # Create New Window
    top_new_ed = Toplevel()
    top_new_ed.title("Edit A Story")
    screen_x_2 = top_new_ed.winfo_screenwidth()
    screen_y_2 = top_new_ed.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 500
    top_new_ed.minsize(window_x_2, window_y_2)
    top_new_ed.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top_new_ed.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame
    info_frame_1 = LabelFrame(top_new_ed, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame
    info_frame_2 = LabelFrame(top_new_ed, height=frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    button_frame = LabelFrame(top_new_ed, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width/2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    beginning_label = Label(info_frame_2, text="Edit Text:", width=int(width/2)-1, anchor=NW)
    beginning_label.grid(row=0, column=0, padx=pad, pady=pad, stick="nw")

    # Text
    global edit_text_entry
    edit_text_entry = Text(info_frame_2, width=37, height=20)
    edit_text_entry.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    width_buttons = 19
    save_story_button = Button(button_frame, text="Save Changes", width=width_buttons, command=edit_story)
    save_story_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    load_text_button = Button(button_frame, text="Load Text", width=width_buttons, command=insert_edit)
    load_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=top_new_ed.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    global option_edit_menu

    def option_edit_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories""")
        s_id_list_raw = c.fetchall()
        s_id_list = []
        for tp in s_id_list_raw:
            for item in tp:
                s_id_list.append(item)

        if s_id_list:
            global s_id_variable
            s_id_variable = StringVar()
            s_id_variable.set(s_id_list[0])
            story_id_del_opmenu = OptionMenu(info_frame_1, s_id_variable, *s_id_list)
            story_id_del_opmenu.config(width=width)
            story_id_del_opmenu.grid(row=0, column=1, ipadx=pad, pady=pad, stick="w")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            top_new_ed.destroy()

        conn.commit()
        conn.close()

    option_edit_menu()

    top_new_ed.mainloop()


# Function to delete a story from the delete window
def delete_story():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    s_id = s_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete story Number {s_id}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM stories WHERE s_id = '{s_id}'""")
        c.execute(f"""DELETE FROM first_paragraphs WHERE s_id = '{s_id}'""")
        c.execute(f"""DELETE FROM paragraphs WHERE s_id = '{s_id}'""")
        c.execute(f"""DELETE FROM choices WHERE s_id = '{s_id}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {s_id} has been successfully deleted.")
        old_text.set("")

    conn.commit()
    conn.close()

    option_del_menu()


# Function to insert old text in a label in the delete story window
def insert_del():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_id = s_id_variable.get()

    c.execute(f"""SELECT s_text FROM stories WHERE s_id = '{s_id}'""")
    text_raw = c.fetchall()
    original_text_2 = ((text_raw[0])[0])

    # Input data into text box
    old_text.set(str(original_text_2))

    conn.commit()
    conn.close()


# Function to open delete window
def delete_story_window():
    global top_new_del
    # Create New Window
    top_new_del = Toplevel()
    top_new_del.title("Delete A Story")
    screen_x_2 = top_new_del.winfo_screenwidth()
    screen_y_2 = top_new_del.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 500
    top_new_del.minsize(window_x_2, window_y_2)
    top_new_del.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top_new_del.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame
    info_frame_1 = LabelFrame(top_new_del, height=info_frame_height, width=window_x_2)
    info_frame_1.pack(fill="both", side=TOP)

    # Info Frame
    info_frame_2 = LabelFrame(top_new_del, height=frame_height, width=window_x_2)
    info_frame_2.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    button_frame = LabelFrame(top_new_del, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    pad = 10

    # Labels
    story_id_label = Label(info_frame_1, text="Select Story ID:", width=int(width/2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    text_label = Label(info_frame_2, text="Output:", width=int(width/2), anchor=NW)
    text_label.grid(row=1, column=0, padx=pad, pady=pad, stick="nw")

    # Message Box
    global old_text
    old_text = StringVar()
    story_del_message = Message(info_frame_2, textvariable=old_text, width=280, anchor=W)
    story_del_message.grid(row=1, column=1, padx=pad, pady=pad, stick="w")

    # Buttons
    width_buttons = 19
    delete_text_button = Button(button_frame, text="Delete Text", width=width_buttons, command=delete_story)
    delete_text_button.grid(row=0, column=0, padx=pad, pady=pad, stick="w")

    check_text_button = Button(button_frame, text="Check Text", width=width_buttons, command=insert_del)
    check_text_button.grid(row=0, column=1, padx=pad, pady=pad, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=top_new_del.destroy)
    cancel_button.grid(row=0, column=2, padx=pad, pady=pad, stick="w")

    global option_del_menu

    def option_del_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories""")
        s_id_list_raw = c.fetchall()
        s_id_list = []
        for tp in s_id_list_raw:
            for item in tp:
                s_id_list.append(item)

        if s_id_list:
            global s_id_variable
            s_id_variable = StringVar()
            s_id_variable.set(s_id_list[0])
            story_id_del_opmenu = OptionMenu(info_frame_1, s_id_variable, *s_id_list)
            story_id_del_opmenu.config(width=width)
            story_id_del_opmenu.grid(row=0, column=1, ipadx=pad, pady=pad, stick="w")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            top_new_del.destroy()

        conn.commit()
        conn.close()

    option_del_menu()

    top_new_del.mainloop()
