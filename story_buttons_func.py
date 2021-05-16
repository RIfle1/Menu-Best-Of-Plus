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
def s_new_save():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS stories
    (s_id text, 
    s_text text)""")

    s_new_s_id = s_new_story_id_entry.get()
    s_new_text_length = len(s_new_beginning_story_entry.get("1.0", "end"))
    c.execute(f"""SELECT s_id FROM stories WHERE s_id = '{id.id_conv('s_id', s_new_s_id)}'""")
    s_new_s_id_raw = c.fetchall()

    if s_new_text_length != 1:
        if len(s_new_s_id_raw) == 0:
            try:
                s_new_s_id = int(s_new_story_id_entry.get())
                if s_new_s_id > 0:
                    # Insert into table if that id does not exist
                    c.execute(
                        "INSERT INTO stories VALUES (:s_id, :s_text)",
                        {
                            "s_id": f"{id.s_id(s_new_s_id)}",
                            "s_text": str(s_new_beginning_story_entry.get("1.0", "end"))
                        })
                    # Show Success pop-up
                    messagebox.showinfo("Success", f"Story Number {s_new_s_id} has been successfully created.")
                    s_new_beginning_story_entry.delete("1.0", "end")

                else:
                    messagebox.showerror("Syntax Error", "Story ID Must Be Positive", icon='warning')

            except ValueError:
                messagebox.showerror("Syntax Error", "Story ID Must Be A Number", icon='warning')

        else:
            messagebox.showerror("Duplication Error", f"Story Number {s_new_s_id} Already Exists", icon='warning')

    else:
        messagebox.showerror("Input Error", "Story Text Is Empty", icon='warning')

    # End Connection
    conn.commit()
    conn.close()

    # Clear the Text Boxes
    s_new_story_id_entry.delete(0, END)


# Function for new story window
def s_new_window():
    global s_new_wd
    # Create New Window
    s_new_wd = Toplevel()
    s_new_wd.title("Create A New Story")
    screen_x_2 = s_new_wd.winfo_screenwidth()
    screen_y_2 = s_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 500
    s_new_wd.minsize(window_x_2, window_y_2)
    s_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    s_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Main Frame
    s_new_main_frame = LabelFrame(s_new_wd, height=window_y_2, width=window_x_2)
    s_new_main_frame.pack(fill="both", expand=True)

    width = 42
    height = 10
    # Labels
    s_new_story_id_label = Label(s_new_main_frame, text="Story Number:", width=int(width/2), anchor=W)
    s_new_story_id_label.grid(row=0, column=0, padx=height, pady=height, stick="w")

    s_new_beginning_label = Label(s_new_main_frame, text="Beginning Text:", width=int(width/2), anchor=NW)
    s_new_beginning_label.grid(row=1, column=0, padx=height, pady=height, stick="nw")

    # Entries
    global s_new_story_id_entry, s_new_beginning_story_entry
    s_new_story_id_entry = Entry(s_new_main_frame, width=48)
    s_new_story_id_entry.grid(row=0, column=1, padx=height, pady=height)

    s_new_beginning_story_entry = Text(s_new_main_frame, width=36)
    s_new_beginning_story_entry.grid(row=1, column=1, padx=height, pady=height)

    # Buttons
    s_new_save_story_button = Button(s_new_main_frame, text="Save Story", width=int(width/2), command=s_new_save)
    s_new_save_story_button.grid(row=2, column=0, padx=height, pady=height, stick="w")

    s_new_cancel_button = Button(s_new_main_frame, text="Cancel", width=width, command=s_new_wd.destroy)
    s_new_cancel_button.grid(row=2, column=1, padx=height, pady=height, stick="w")

    s_new_wd.mainloop()


# Function to insert already written text
def s_edt_insert():
    # Delete Previous Input
    s_edt_edit_text_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_edt_s_id = s_edt_s_id_variable.get()

    c.execute(f"""SELECT s_text FROM stories WHERE s_id = '{s_edt_s_id}'""")
    s_edt_text_raw = c.fetchall()
    s_edt_text = ((s_edt_text_raw[0])[0])

    # Input data into text box
    s_edt_edit_text_entry.insert(END, f'{s_edt_text}')

    conn.commit()
    conn.close()


# Function to edit stories
def s_edt_edit():
    # Create a connection to the database
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    # Update Table
    s_edt_s_id = s_edt_s_id_variable.get()
    if len(s_edt_edit_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE stories SET s_text = :s_text WHERE s_id = :s_id""",
                  {
                      "s_text": s_edt_edit_text_entry.get("1.0", "end"),
                      "s_id": f'{s_edt_s_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {s_edt_s_id} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Story Text is Empty', icon='warning')

    # Clear the Text Boxes
    s_edt_edit_text_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to delete a story from the delete window
def s_del_delete():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    s_del_s_id = s_edt_s_id_variable.get()

    s_del_warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete story Number {id.id_int(s_del_s_id)}?', icon='warning')

    if s_del_warning == 'yes':
        c.execute(f"""DELETE FROM stories WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM initial_paragraphs WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM paragraphs WHERE s_id = '{s_del_s_id}'""")
        c.execute(f"""DELETE FROM choices WHERE s_id = '{s_del_s_id}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Story Number {id.id_int(s_del_s_id)} has been successfully deleted\nAll Paragraphs And Choices From Story Number {id.id_int(s_del_s_id)} Have Also Been Deleted.")

    conn.commit()
    conn.close()

    s_edt_edit_text_entry.delete("1.0", "end")

    s_edt_s_id_opt_menu()


# Function to open edit window
def s_edt_window():
    global s_edt_wd
    # Create New Window
    s_edt_wd = Toplevel()
    s_edt_wd.title("Edit A Story")
    screen_x_2 = s_edt_wd.winfo_screenwidth()
    screen_y_2 = s_edt_wd.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 450
    s_edt_wd.minsize(window_x_2, window_y_2)
    s_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    s_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    frame_height = 400
    info_frame_height = 100

    # Info Frame
    s_edt_info_frame_1 = LabelFrame(s_edt_wd, height=info_frame_height, width=window_x_2)
    s_edt_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame
    s_edt_info_frame_2 = LabelFrame(s_edt_wd, height=frame_height, width=window_x_2)
    s_edt_info_frame_2.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    s_edt_button_frame = LabelFrame(s_edt_wd, height=window_y_2 - frame_height, width=window_x_2)
    s_edt_button_frame.pack(fill="both", side=BOTTOM)

    s_edt_width = 42
    s_edt_pad = 10

    # Labels
    s_edt_story_id_label = Label(s_edt_info_frame_1, text="Select Story ID:", width=int(s_edt_width/2), anchor=W)
    s_edt_story_id_label.grid(row=0, column=0, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_beginning_label = Label(s_edt_info_frame_2, text="Edit Text:", width=int(s_edt_width/2)-1, anchor=NW)
    s_edt_beginning_label.grid(row=0, column=0, padx=s_edt_pad, pady=s_edt_pad, stick="nw")

    # Text
    global s_edt_edit_text_entry
    s_edt_edit_text_entry = Text(s_edt_info_frame_2, width=37, height=20)
    s_edt_edit_text_entry.grid(row=0, column=1, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    # Buttons
    s_edt_width_buttons = 13
    s_edt_save_story_button = Button(s_edt_button_frame, text="Save Changes", width=s_edt_width_buttons, command=s_edt_edit)
    s_edt_save_story_button.grid(row=0, column=0, padx=(s_edt_pad+3, s_edt_pad), pady=s_edt_pad, stick="w")

    s_edt_load_text_button = Button(s_edt_button_frame, text="Load Story", width=s_edt_width_buttons, command=s_edt_insert)
    s_edt_load_text_button.grid(row=0, column=1, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_delete_text_button = Button(s_edt_button_frame, text="Delete Story", width=s_edt_width_buttons, command=s_del_delete)
    s_edt_delete_text_button.grid(row=0, column=2, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    s_edt_cancel_button = Button(s_edt_button_frame, text="Cancel", width=s_edt_width_buttons, command=s_edt_wd.destroy)
    s_edt_cancel_button.grid(row=0, column=3, padx=s_edt_pad, pady=s_edt_pad, stick="w")

    global s_edt_s_id_opt_menu

    def s_edt_s_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories""")
        s_edt_s_id_list_raw = c.fetchall()
        s_edt_s_id_list = []
        for tp in s_edt_s_id_list_raw:
            for item in tp:
                s_edt_s_id_list.append(item)

        if s_edt_s_id_list:
            global s_edt_s_id_variable
            s_edt_s_id_variable = StringVar()
            s_edt_s_id_variable.set(s_edt_s_id_list[0])
            s_edt_s_id_opt_menu_var = OptionMenu(s_edt_info_frame_1, s_edt_s_id_variable, *s_edt_s_id_list)
            s_edt_s_id_opt_menu_var.config(width=s_edt_width-2)
            s_edt_s_id_opt_menu_var.grid(row=0, column=1, ipadx=s_edt_pad, pady=s_edt_pad, stick="w")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            s_edt_wd.destroy()

        conn.commit()
        conn.close()

    s_edt_s_id_opt_menu()

    s_edt_wd.mainloop()
