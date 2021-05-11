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
tabControl = ttk.Notebook(editor)

# Creating Tabs
paragraphs_tab = ttk.Frame(tabControl)
characters_tab = ttk.Frame(tabControl)
objects_tab = ttk.Frame(tabControl)
game_settings_tab = ttk.Frame(tabControl)
test_tab = ttk.Frame(tabControl)

# Adding Tabs
tabControl.add(paragraphs_tab, text="Paragraphs")
tabControl.add(characters_tab, text="Characters")
tabControl.add(objects_tab, text="Objects")
tabControl.add(game_settings_tab, text="Game Settings")
tabControl.add(test_tab, text="Test")

# Positioning the Tabs
tabControl.pack(expand=1, fill="both")

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
    conn = sqlite3.connect("EditorData.db")
    c = conn.cursor()

    record_id = paragraph_number_edit_entry.get()
    c.execute("""UPDATE paragraphs SET
    main_paragraph = :main_paragraph,
    choice_1 = :choice_1,
    choice_2 = :choice_2,
    choice_3 = :choice_3,
    choice_4 = :choice_4
    
    WHERE paragraph_number = :paragraph_number""",
              {
                  "main_paragraph": main_paragraph_edit_entry.get(),
                  "choice_1": choice_1_edit_entry.get(),
                  "choice_2": choice_2_edit_entry.get(),
                  "choice_3": choice_3_edit_entry.get(),
                  "choice_4": choice_4_edit_entry.get(),

                  "paragraph_number": record_id
              })

    # Clear the Text Boxes
    paragraph_number_edit_entry.delete(0, END)
    main_paragraph_edit_entry.delete(0, END)
    choice_1_edit_entry.delete(0, END)
    choice_2_edit_entry.delete(0, END)
    choice_3_edit_entry.delete(0, END)
    choice_4_edit_entry.delete(0, END)

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

    choice_1_label = Label(info_frame, text="Choice 1:")
    choice_1_label.grid(row=2, column=0, pady=(0, 10), padx=2, stick=W)

    choice_2_label = Label(info_frame, text="Choice 2:")
    choice_2_label.grid(row=3, column=0, pady=(0, 10), padx=2, stick=W)

    choice_3_label = Label(info_frame, text="Choice 3:")
    choice_3_label.grid(row=4, column=0, pady=(0, 10), padx=2, stick=W)

    choice_4_label = Label(info_frame, text="Choice 4:")
    choice_4_label.grid(row=5, column=0, pady=(0, 10), padx=2, stick=W)

    # Entries
    global paragraph_number_edit_entry, main_paragraph_edit_entry, choice_1_edit_entry, choice_2_edit_entry, choice_3_edit_entry, choice_4_edit_entry

    paragraph_number_edit_entry = Entry(info_frame, width=30)
    paragraph_number_edit_entry.grid(row=0, column=1, pady=10, padx=10)

    main_paragraph_edit_entry = Entry(info_frame, width=30)
    main_paragraph_edit_entry.grid(row=1, column=1, pady=(0, 10), padx=10)

    choice_1_edit_entry = Entry(info_frame, width=30)
    choice_1_edit_entry.grid(row=2, column=1, pady=(0, 10), padx=10)

    choice_2_edit_entry = Entry(info_frame, width=30)
    choice_2_edit_entry.grid(row=3, column=1, pady=(0, 10), padx=10)

    choice_3_edit_entry = Entry(info_frame, width=30)
    choice_3_edit_entry.grid(row=4, column=1, pady=(0, 10), padx=10)

    choice_4_edit_entry = Entry(info_frame, width=30)
    choice_4_edit_entry.grid(row=5, column=1, pady=(0, 10), padx=10)

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
    # Delete previous paragraphs in the frame
    for widgets in frame_cell_creator.winfo_children():
        widgets.destroy()

    conn = sqlite3.connect("EditorData.db")
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
        conn = sqlite3.connect("EditorData.db")
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
        paragraph_frame = LabelFrame(frame_cell_creator, text=f"Paragraph {number}")
        paragraph_frame.grid(row=number, column=1)

        # Labels
        paragraph_label = Label(paragraph_frame, text="Main Paragraph")
        paragraph_label.grid(row=0, column=0)

        choice_1_label = Label(paragraph_frame, text="Choice 1:")
        choice_1_label.grid(row=1, column=0)

        choice_2_label = Label(paragraph_frame, text="Choice 2:")
        choice_2_label.grid(row=2, column=0)

        choice_3_label = Label(paragraph_frame, text="Choice 3:")
        choice_3_label.grid(row=3, column=0)

        choice_4_label = Label(paragraph_frame, text="Choice 4:")
        choice_4_label.grid(row=4, column=0)

        # Input information
        paragraph_text = Label(paragraph_frame, text=str(info_list[1]))
        paragraph_text.grid(row=0, column=1)

        choice_1_label = Label(paragraph_frame, text=str(info_list[2]))
        choice_1_label.grid(row=1, column=1)

        choice_2_label = Label(paragraph_frame, text=str(info_list[3]))
        choice_2_label.grid(row=2, column=1)

        choice_3_label = Label(paragraph_frame, text=str(info_list[4]))
        choice_3_label.grid(row=3, column=1)

        choice_4_label = Label(paragraph_frame, text=str(info_list[5]))
        choice_4_label.grid(row=4, column=1)


def save_changes():
    # Create a connection to the database
    conn = sqlite3.connect("EditorData.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs 
                (paragraph_number integer,
                main_paragraph text,
                choice_1 text,
                choice_2 text,
                choice_3 text,
                choice_4 text)""")

    # Insert into table
    c.execute("INSERT INTO paragraphs VALUES (:paragraph_number, :main_paragraph, :choice_1, :choice_2, :choice_3, :choice_4)",
              {
                  "paragraph_number": int(paragraph_number_entry.get()),
                  "main_paragraph": str(main_paragraph_entry.get()),
                  "choice_1": str(choice_1_entry.get()),
                  "choice_2": str(choice_2_entry.get()),
                  "choice_3": str(choice_3_entry.get()),
                  "choice_4": str(choice_4_entry.get())
              })

    # Clear the Text Boxes
    paragraph_number_entry.delete(0, END)
    main_paragraph_entry.delete(0, END)
    choice_1_entry.delete(0, END)
    choice_2_entry.delete(0, END)
    choice_3_entry.delete(0, END)
    choice_4_entry.delete(0, END)

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
    window_x_2 = 480
    window_y_2 = 230
    top.minsize(window_x_2, window_y_2)
    top.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    top.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Create a frame for the labels and entries
    info_frame = Frame(top)
    info_frame.grid(row=0, column=0)

    # Labels
    paragraph_number_label = Label(info_frame, text="Paragraph Number (Priority of the Paragraph):")
    paragraph_number_label.grid(row=0, column=0, pady=10, padx=2, stick=W)

    main_paragraph_label = Label(info_frame, text="Main Paragraph:")
    main_paragraph_label.grid(row=1, column=0, pady=(0, 10), padx=2, stick=W)

    choice_1_label = Label(info_frame, text="Choice 1:")
    choice_1_label.grid(row=2, column=0, pady=(0, 10), padx=2, stick=W)

    choice_2_label = Label(info_frame, text="Choice 2:")
    choice_2_label.grid(row=3, column=0, pady=(0, 10), padx=2, stick=W)

    choice_3_label = Label(info_frame, text="Choice 3:")
    choice_3_label.grid(row=4, column=0, pady=(0, 10), padx=2, stick=W)

    choice_4_label = Label(info_frame, text="Choice 4:")
    choice_4_label.grid(row=5, column=0, pady=(0, 10), padx=2, stick=W)

    # Entries
    global paragraph_number_entry, main_paragraph_entry, choice_1_entry, choice_2_entry, choice_3_entry, choice_4_entry

    paragraph_number_entry = Entry(info_frame, width=30)
    paragraph_number_entry.grid(row=0, column=1, pady=10, padx=10)

    main_paragraph_entry = Entry(info_frame, width=30)
    main_paragraph_entry.grid(row=1, column=1, pady=(0, 10), padx=10)

    choice_1_entry = Entry(info_frame, width=30)
    choice_1_entry.grid(row=2, column=1, pady=(0, 10), padx=10)

    choice_2_entry = Entry(info_frame, width=30)
    choice_2_entry.grid(row=3, column=1, pady=(0, 10), padx=10)

    choice_3_entry = Entry(info_frame, width=30)
    choice_3_entry.grid(row=4, column=1, pady=(0, 10), padx=10)

    choice_4_entry = Entry(info_frame, width=30)
    choice_4_entry.grid(row=5, column=1, pady=(0, 10), padx=10)

    # Create a frame for the save and cancel buttons
    button_frame = Frame(top)
    button_frame.grid(row=1, column=0)

    # Save Button
    save_button = Button(button_frame, text="Save Changes", command=save_changes)
    save_button.grid(row=0, column=0, pady=(0, 10), padx=2, ipadx=80, stick="w")

    # Cancel Button
    cancel_button = Button(button_frame, text="Cancel", command=cancel_top)
    cancel_button.grid(row=0, column=1, pady=(0, 10), padx=10, ipadx=40)

    top.mainloop()


# Window Pop-up to get X and Y values for package Frames


def position_window():

    def get_position():
        x_pos = text_pos_x_df.get()
        y_pos = text_pos_y_df.get()
        return x_pos, y_pos

    # Main window
    window = Tk()
    window.title("Select Position")

    # Center the Screen
    screen_x_2 = window.winfo_screenwidth()
    screen_y_2 = window.winfo_screenheight()
    window_x_2 = 390
    window_y_2 = 150

    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)

    window.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Widgets

    package = tkinter.Frame(window)

    label_pos_x = tkinter.Label(package, text="Row", font=("Montserrat", 14), fg="#323232", padx=30, pady=10)
    label_pos_x.grid(row=0, column=0, stick="w")

    label_pos_y = tkinter.Label(package, text="Column", font=("Montserrat", 14), fg="#323232", padx=30, pady=10)
    label_pos_y.grid(row=1, column=0, stick="w")

    text_pos_x_df = IntVar(package, value=0)
    text_pos_x = tkinter.Entry(package, textvariable=text_pos_x_df)
    text_pos_x.grid(row=0, column=1)

    text_pos_y_df = IntVar(package, value=0)
    text_pos_y = tkinter.Entry(package, textvariable=text_pos_y_df)
    text_pos_y.grid(row=1, column=1)

    enter = tkinter.Button(package, text="Enter", bd=0, bg="#3285F4", fg="White", padx=30, pady=10, font="Montserrat",
                           relief=FLAT, command=get_position)
    enter.grid(row=3, column=3)

    package.grid(row=0, column=0)
    window.mainloop()


# Main Frame

main_frame_paragraph = tkinter.Frame(paragraphs_tab, padx=20, pady=20)
main_frame_paragraph.grid(row=0, column=0, columnspan=3, stick="w")

# Cell Frame
global frame_cell_creator
frame_cell_creator = tkinter.LabelFrame(paragraphs_tab, text=f"First Paragraph")
frame_cell_creator.grid(row=1, column=0, columnspan=3, stick="w")

# Create new PARAGRAPH Button

create_paragraph_button = tkinter.Button(main_frame_paragraph,
                                         text="New Paragraph", bg="#3285F4",
                                         fg="White", padx=30, pady=10,
                                         font=("Montserrat", 18),
                                         width=21, command=table_creator)
create_paragraph_button.grid(row=0, column=0, stick="w", padx=(0, 10))

# Create update PARAGRAPH Button

show_paragraphs_button = tkinter.Button(main_frame_paragraph,
                                        text="Show Paragraphs", bg="#3285F4",
                                        fg="White", padx=30, pady=10,
                                        font=("Montserrat", 18),
                                        width=21, command=show_paragraphs)
show_paragraphs_button.grid(row=0, column=1, stick="w", padx=(10, 10))

# Delete Paragraph Button

edit_paragraph_button = tkinter.Button(main_frame_paragraph, text="Edit Paragraph",
                                       bg="#3285F4", fg="White", padx=30, pady=10,
                                       font=("Montserrat", 18), width=21, command=update_paragraph)
edit_paragraph_button.grid(row=0, column=2, stick="w", padx=(10, 0))

# -------------------------------------------
# LOOP END
# -------------------------------------------
editor.config(menu=main_menu)
editor.mainloop()
