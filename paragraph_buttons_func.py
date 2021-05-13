# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id


def save_int_paragraph_window():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS first_paragraphs
    (s_id text, 
    fp_id text,
    fp_text text)""")

    s_id = get_story_id_entry.get()
    fp_id = get_story_id_entry.get()
    text_length = len(paragraph_text_entry.get("1.0", "end"))
    c.execute(f"""SELECT fp_id FROM first_paragraphs WHERE fp_id = '{id.fparagraph_id(fp_id)}'""")
    s_id_raw = c.fetchall()

    if text_length != 1:
        if len(s_id_raw) == 0:
            try:
                fp_id = int(get_story_id_entry.get())
                if fp_id > 0:
                    # Insert into table if that id does not exist
                    c.execute("INSERT INTO first_paragraphs VALUES (:s_id, :fp_id, :fp_text)",
                        {
                            "s_id": f"{id.story_id(s_id)}",
                            "fp_id": f"{id.story_id(s_id)}_{id.fparagraph_id(fp_id)}",
                            "fp_text": str(paragraph_text_entry.get("1.0", "end"))
                        })
                    # Show Success pop-up
                    messagebox.showinfo("Success", f"First Paragraph of Story {s_id} has been successfully created.")

                else:
                    messagebox.showerror("Syntax Error", "Story ID Must Be Positive")

            except ValueError:
                messagebox.showerror("Syntax Error", "Story ID Must Be A Number")

        else:
            messagebox.showerror("Duplication Error", f"First Paragraph for Story number {s_id} already exists")

    else:
        messagebox.showerror("Input Error", "Story Text Is Empty")

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    get_story_id_entry.delete(0, END)
    paragraph_text_entry.delete("1.0", "end")


def insert_int_paragraph():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_id = get_story_id_entry.get()
    try:
        s_id = int(s_id)
        if s_id > 0:
            try:
                # Fetch Information
                c.execute(f"SELECT s_text FROM stories WHERE s_id='{id.story_id(s_id)}'")
                text_raw = c.fetchall()
                text_1 = ((text_raw[0])[0])

                # Input data into text box
                old_text.set(str(text_1))
            except IndexError:
                messagebox.showerror("Index Error", f"Story ID Number {s_id} Does Not Exist")
                get_story_id_entry.delete(0, END)
        else:
            messagebox.showerror("Syntax Error", "Story ID Must Be Positive and Different than 0")
            get_story_id_entry.delete(0, END)
    except ValueError:
        messagebox.showerror("Syntax Error", "Story ID Must Be A Number")
        get_story_id_entry.delete(0, END)

    finally:
        # End Connection
        conn.commit()
        conn.close()


def int_paragraph_window():
    global top_new_pg
    # Create New Window
    top_new_pg = Toplevel()
    top_new_pg.title("Create A First Paragraph")
    screen_x_2 = top_new_pg.winfo_screenwidth()
    screen_y_2 = top_new_pg.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 800
    top_new_pg.minsize(window_x_2, window_y_2)
    top_new_pg.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top_new_pg.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 200
    rest = window_y_2 - frame_height*2
    # Story Frame
    story_frame = LabelFrame(top_new_pg, width=window_x_2, height=frame_height)
    story_frame.pack(fill="both", side=TOP, expand=True)

    # Top Button Frame
    button_frame_1 = LabelFrame(top_new_pg, height=rest/2, width=window_x_2)
    button_frame_1.pack(fill="both")

    # Paragraph Frame
    paragraph_frame = LabelFrame(top_new_pg, width=window_x_2, height=frame_height)
    paragraph_frame.pack(fill="both")

    # Bottom Buttons Frame
    button_frame = LabelFrame(top_new_pg, height=rest/2, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    width = 42
    height = 10
    # Labels
    get_story_id_label = Label(story_frame, text="From Story Number:", width=int(width / 2), anchor=W)
    get_story_id_label.grid(row=0, column=0, padx=(10, 13), pady=height, stick="w")

    story_text_label = Label(story_frame, text="Story Text:", width=int(width / 2), anchor=NW)
    story_text_label.grid(row=1, column=0, padx=height, pady=height, stick="nw")

    paragraph_text_label = Label(paragraph_frame, text="Paragraph Text:", width=int(width / 2), anchor=NW)
    paragraph_text_label.grid(row=0, column=0, padx=(10, 13), pady=height, stick="nw")

    # Entries
    global get_story_id_entry, paragraph_text_entry, old_text
    get_story_id_entry = Entry(story_frame, width=50)
    get_story_id_entry.grid(row=0, column=1, padx=height, pady=height)

    paragraph_text_entry = Text(paragraph_frame, width=37, height=20)
    paragraph_text_entry.grid(row=0, column=1, padx=height, pady=height)

    # Message Box
    old_text = StringVar()
    show_story_message = Message(story_frame, textvariable=old_text, width=280, anchor=W)
    show_story_message.grid(row=1, column=1, padx=height, pady=height, stick="w")

    # Buttons
    submit_button = Button(button_frame_1, text="Submit", width=int(width / 2), command=insert_int_paragraph)
    submit_button.grid(row=2, column=0, padx=height, pady=height, stick="w")

    save_story_button = Button(button_frame, text="Save Story", width=int(width / 2), command=save_int_paragraph_window)
    save_story_button.grid(row=2, column=0, padx=height, pady=height, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width, command=None)
    cancel_button.grid(row=2, column=1, padx=height, pady=height, stick="w")

    top_new_pg.mainloop()

