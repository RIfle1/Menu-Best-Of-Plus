# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3

# Main App
editor = Tk()
editor.title("Game Editor")

# Center the Screen
screen_x = editor.winfo_screenwidth()
screen_y = editor.winfo_screenheight()
window_x = 1200
window_y = 800

pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)

editor.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# Adding the Menus
main_menu = tkinter.Menu(editor)

file_menu = tkinter.Menu(main_menu, tearoff=0)
file_menu.add_command(label="New Game Editor")
file_menu.add_command(label="Load Game Editor")
file_menu.add_command(label="Save Game Editor")

options_menu = tkinter.Menu(main_menu, tearoff=0)
options_menu.add_command(label="Change Paragraph Order")
options_menu.add_command(label="Dark Mode")
options_menu.add_command(label="Quit", command=editor.quit)

main_menu.add_cascade(label="File", menu=file_menu)
main_menu.add_cascade(label="Options", menu=options_menu)

# Tab Control
tabcontrol = ttk.Notebook(editor)

# Creating Tabs
paragraphs_tab = ttk.Frame(tabcontrol)
characters_tab = ttk.Frame(tabcontrol)
objects_tab = ttk.Frame(tabcontrol)
game_settings_tab = ttk.Frame(tabcontrol)
test_tab = ttk.Frame(tabcontrol)


# Adding Tabs
tabcontrol.add(paragraphs_tab, text="Paragraphs")
tabcontrol.add(characters_tab, text="Characters")
tabcontrol.add(objects_tab, text="Objects")
tabcontrol.add(game_settings_tab, text="Game Settings")
tabcontrol.add(test_tab, text="Test")

# Positioning the Tabs
tabcontrol.pack(expand=1, fill="both")


# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "CHARACTER" TAB
# -------------------------------------------


# ----------------------------------------------------
# THIS IS THE END OF THE CODE FOR THE "CHARACTER" TAB
# ----------------------------------------------------

# ------------------------------------------
# THIS FOLLOWING CODE IS FOR THE "TEST" TAB
# ------------------------------------------


# -----------------------------------------------
# THIS IS THE END OF THE CODE FOR THE "TEST" TAB
# -----------------------------------------------


# -------------------------------------------
# THIS FOLLOWING CODE IS FOR "PARAGRAPH" TAB
# -------------------------------------------

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


# Functions to close the pop-up windows
def cancel_top():
    top.destroy()


def cancel_top_2():
    top_2.destroy()


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


# Create a function that creates tables in the Database connection

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


# Main Frame
main_button_frame = tkinter.Frame(paragraphs_tab, padx=20, pady=20)
main_button_frame.grid(row=0, column=0, columnspan=3, stick="w")

# Cell Frame
global main_paragraph_frame
main_paragraph_frame = tkinter.LabelFrame(paragraphs_tab, text="All Paragraphs")
main_paragraph_frame.grid(row=1, column=0, columnspan=3, stick="w")

# Create new PARAGRAPH Button
create_paragraph_button = tkinter.Button(main_button_frame,
                                         text="New Paragraph", bg="#3285F4",
                                         fg="White", padx=30, pady=10,
                                         font=("Montserrat", 18),
                                         width=21, command=table_creator)
create_paragraph_button.grid(row=0, column=0, stick="w", padx=(0, 10))

# Create update PARAGRAPH Button
show_paragraphs_button = tkinter.Button(main_button_frame,
                                        text="Show / Update Paragraphs", bg="#3285F4",
                                        fg="White", padx=30, pady=10,
                                        font=("Montserrat", 18),
                                        width=21, command=show_paragraphs)
show_paragraphs_button.grid(row=0, column=1, stick="w", padx=(10, 10))

# Delete Paragraph Button
edit_paragraph_button = tkinter.Button(main_button_frame, text="Edit Paragraph",
                                       bg="#3285F4", fg="White", padx=30, pady=10,
                                       font=("Montserrat", 18), width=21, command=update_paragraph)
edit_paragraph_button.grid(row=0, column=2, stick="w", padx=(10, 0))

# -------------------------------------------
# LOOP END
# -------------------------------------------
editor.config(menu=main_menu)
editor.mainloop()
