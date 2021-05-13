# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3


# Function to save the changes from the update_paragraph function
def edit_changes():
    conn = sqlite3.connect("EditorDataV2.db")
    c = conn.cursor()

    record_id = paragraph_number_edit_entry.get()
    c.execute("""UPDATE paragraphs SET
    main_paragraph = :main_paragraph

    WHERE paragraph_number = :paragraph_number""",
              {
                  "main_paragraph": main_paragraph_edit_entry.get(),

                  "paragraph_number": record_id
              })

    # Clear the Text Boxes
    paragraph_number_edit_entry.delete(0, END)
    main_paragraph_edit_entry.delete(0, END)

    conn.commit()
    conn.close()


# Function that creates tables in the Database connection
def table_creator():
    global top
    # Create New Window
    top = Toplevel()
    top.title("Add New Paragraph")
    screen_x_2 = top.winfo_screenwidth()
    screen_y_2 = top.winfo_screenheight()
    window_x_2 = 490
    window_y_2 = 230
    top.minsize(window_x_2, window_y_2)
    """top.maxsize(window_x_2, window_y_2)"""
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Frame for the paragraph labels and entries
    info_frame_paragraph = LabelFrame(top)
    info_frame_paragraph.pack(fill="both", expand=True)

    # Paragraph Labels
    paragraph_number_label = Label(info_frame_paragraph, text="Paragraph Number (Priority of the Paragraph):", width=35, anchor=W)
    paragraph_number_label.grid(row=0, column=0, pady=5, padx=5, stick="w")

    main_paragraph_label = Label(info_frame_paragraph, text="Main Paragraph:", width=35, anchor=W)
    main_paragraph_label.grid(row=1, column=0, pady=5, padx=5, stick="w")

    #  Paragraph Entries
    global paragraph_number_entry, main_paragraph_entry

    paragraph_number_entry = Entry(info_frame_paragraph, width=35)
    paragraph_number_entry.grid(row=0, column=1, pady=5, padx=5)

    main_paragraph_entry = Entry(info_frame_paragraph, width=35)
    main_paragraph_entry.grid(row=1, column=1, pady=5, padx=5)

    # Get first frame width
    info_frame_paragraph.update()
    frame_width = paragraph_number_label.winfo_width()
    print(frame_width)

    # Frame for the save button
    button_frame_1 = LabelFrame(top, width=frame_width)
    button_frame_1.pack(fill="both", expand=True)

    # Save Paragraph Button
    save_button = Button(button_frame_1, text="Save Paragraph", command=save_changes)
    save_button.pack(fill="both", expand=True, padx=5)

    # Frame for the choices labels and entries
    info_frame_choice = LabelFrame(top)
    info_frame_choice.pack(fill="both", expand=True)

    # Choice Labels
    select_paragraph_number_label = Label(info_frame_choice, text="Select Paragraph To Add Choices:", width=35, anchor=W)
    select_paragraph_number_label.grid(row=0, column=0, pady=5, padx=5, stick="w")

    choice_number_label = Label(info_frame_choice, text="Choice Number:", width=35, anchor=W)
    choice_number_label.grid(row=1, column=0, pady=5, padx=5, stick="w")

    choice_label = Label(info_frame_choice, text="Choice:", width=35, anchor=W)
    choice_label.grid(row=2, column=0, pady=5, padx=5, stick="w")

    # Choice Entries
    select_paragraph_number_entry = Entry(info_frame_choice, width=35)
    select_paragraph_number_entry.grid(row=0, column=1, pady=5, padx=5)

    choice_number_entry = Entry(info_frame_choice, width=35)
    choice_number_entry.grid(row=1, column=1, pady=5, padx=5)

    choice_entry = Entry(info_frame_choice, width=35)
    choice_entry.grid(row=2, column=1, pady=5, padx=5)

    # Frame for save choice and cancel button
    button_frame_2 = LabelFrame(top)
    button_frame_2.pack(fill="both", expand=True)

    # Save choice Button
    save_button = Button(button_frame_2, text="Save Paragraph", command=None)
    save_button.grid(row=0, column=0, pady=(0, 10), padx=2, ipadx=80, stick="w")

    # Cancel Button
    cancel_button = Button(button_frame_2, text="Cancel", command=cancel_top)
    cancel_button.grid(row=0, column=1, pady=(0, 10), padx=10, ipadx=40)

    top.mainloop()


# Function to insert Data into table
def save_changes():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV2.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs 
                (paragraph_number integer,
                main_paragraph text)""")

    # Insert into table
    c.execute(
        "INSERT INTO paragraphs VALUES (:paragraph_number, :main_paragraph)",
        {
            "paragraph_number": int(paragraph_number_entry.get()),
            "main_paragraph": str(main_paragraph_entry.get())
        })

    # Clear the Text Boxes
    paragraph_number_entry.delete(0, END)
    main_paragraph_entry.delete(0, END)

    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


# Function to Print all info in a frame
def show_paragraphs():
    try:
        # Delete previous paragraphs in the frame
        for widgets in main_paragraph_frame.winfo_children():
            widgets.destroy()

        conn = sqlite3.connect("EditorDataV2.db")
        c = conn.cursor()

        # Fetch the number of the paragraph
        c.execute("SELECT paragraph_number FROM paragraphs")
        paragraph_list_raw = c.fetchall()
        paragraph_list = []

        # Get usable numbers out of paragraph_list_raw
        for i in paragraph_list_raw:
            for numbers in i:
                paragraph_list.append(numbers)

        conn.commit()
        conn.close()

        for number in paragraph_list:
            modified_number = (number,)
            conn = sqlite3.connect("EditorDataV2.db")
            c = conn.cursor()

            # Fetch the rest of the information from the tables
            select_query = f"""SELECT * FROM paragraphs WHERE paragraph_number = ?"""
            c.execute(select_query, modified_number)
            info_list_raw = c.fetchall()
            info_list = info_list_raw[0]
            print(info_list)

            conn.commit()
            conn.close()

            # Creates a new frame
            paragraph_frame = LabelFrame(main_paragraph_frame, text=f"Paragraph {number}")
            paragraph_frame.grid(row=number, column=1)

            # Input information
            paragraph_text = Label(paragraph_frame, text=str(info_list[1]))
            paragraph_text.grid(row=0, column=1)

    except sqlite3.OperationalError as data_error:
        print(str(data_error))
        print("Create New Paragraphs First")


# Function to open a window to edit information on a created paragraph
def update_paragraph():
    global top_2
    # Create New Window
    top_2 = Toplevel()
    top_2.title("Edit Existing Paragraph")
    screen_x_2 = top_2.winfo_screenwidth()
    screen_y_2 = top_2.winfo_screenheight()
    window_x_2 = 480
    window_y_2 = 230
    top_2.minsize(window_x_2, window_y_2)
    top_2.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top_2.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Create a frame for the labels and entries
    info_frame = Frame(top_2)
    info_frame.grid(row=0, column=0)


    # Labels
    paragraph_number_id = Label(info_frame, text="Select Paragraph Number:")
    paragraph_number_id.grid(row=0, column=0, pady=10, padx=2, stick=W)

    main_paragraph_label = Label(info_frame, text="Main Paragraph:")
    main_paragraph_label.grid(row=1, column=0, pady=(0, 10), padx=2, stick=W)

    # Entries
    global paragraph_number_edit_entry, main_paragraph_edit_entry, choice_1_edit_entry, choice_2_edit_entry, choice_3_edit_entry, choice_4_edit_entry

    paragraph_number_edit_entry = Entry(info_frame, width=30)
    paragraph_number_edit_entry.grid(row=0, column=1, pady=10, padx=10)

    main_paragraph_edit_entry = Entry(info_frame, width=30)
    main_paragraph_edit_entry.grid(row=1, column=1, pady=(0, 10), padx=10)

    # Create a frame for the save and cancel buttons
    button_frame = Frame(top_2)
    button_frame.grid(row=1, column=0)

    # Save Button
    save_button = Button(button_frame, text="Save Changes", command=edit_changes)
    save_button.grid(row=0, column=0, pady=(0, 10), padx=2, ipadx=80, stick="w")

    # Cancel Button
    cancel_button = Button(button_frame, text="Cancel", command=cancel_top_2)
    cancel_button.grid(row=0, column=1, pady=(0, 10), padx=10, ipadx=40)

    top_2.mainloop()


# Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    text_length = len(beginning_story_edit_entry.get("1.0", "end"))

    if text_length != 1:
        try:
            story_id = int(story_id_edit_entry.get())

            if story_id > 0:
                try:
                    # Check if the story id exists
                    c.execute(f"SELECT story_id FROM stories WHERE story_id={story_id}")
                    list_id = c.fetchall()

                    if list_id:
                        # Insert Stored Data Into Text Box
                        # Create connection to retrieve data
                        conn = sqlite3.connect("EditorDataV3.db")
                        c = conn.cursor()

                        story_id = story_id_edit_entry.get()
                        c.execute(f"SELECT story_text FROM stories WHERE story_id = {story_id}")
                        text_raw = c.fetchall()
                        global original_text
                        original_text = ((text_raw[0])[0])

                        # Input data into text box
                        beginning_story_edit_entry.insert(END, str(original_text))

                        conn.commit()
                        conn.close()

                    else:
                        messagebox.showerror("Index Error", f"Paragraph Number {story_id} Does Not Exist")

                    # Commit changes
                    conn.commit()
                    # Close Connection
                    conn.close()

                except sqlite3.OperationalError:
                    messagebox.showerror("Operational Error", "You Must Input A Story ID")

            else:
                messagebox.showerror("Syntax Error", "Story ID Must Be Positive")

        except ValueError:
            messagebox.showerror("Syntax Error", "Story ID Must Be A Number")

    else:
        messagebox.showerror("Input Error", "You Must Write Something In The Beginning Paragraph")

    # Clear the Text Boxes
    story_id_edit_entry.delete(0, END)
    beginning_story_edit_entry.delete("1.0", "end")
