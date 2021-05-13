# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id


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
    c.execute(f"""SELECT s_id FROM stories WHERE s_id = '{id.story_id(s_id)}'""")
    s_id_raw = c.fetchall()

    if text_length != 1:
        if len(s_id_raw) == 0:
            try:
                s_id = int(story_id_entry.get())
                if s_id > 0:
                    # Insert into table if that id does not exist
                    c.execute(
                        "INSERT INTO stories VALUES (:s_id, :s_text)",
                        {
                            "s_id": f"{id.story_id(s_id)}",
                            "s_text": str(beginning_story_entry.get("1.0", "end"))
                        })
                    # Show Success pop-up
                    messagebox.showinfo("Success", f"Story Number {s_id} has been successfully created.")

                else:
                    messagebox.showerror("Syntax Error", "Story ID Must Be Positive")

            except ValueError:
                messagebox.showerror("Syntax Error", "Story ID Must Be A Number")

        else:
            messagebox.showerror("Duplication Error", f"Story Number {s_id} Already Exists")

    else:
        messagebox.showerror("Input Error", "Story Text Is Empty")

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

    text_length = len(beginning_story_edit_entry.get("1.0", "end"))

    if text_length != 1:
        try:
            s_id = int(story_id_edit_entry.get())
            if s_id > 0:
                try:
                    # Check if the story id exists
                    c.execute(f"SELECT s_id FROM stories WHERE s_id = '{id.story_id(s_id)}'")
                    list_id = c.fetchall()

                    if list_id:
                        # Update Table
                        s_id = story_id_edit_entry.get()
                        c.execute("""UPDATE stories SET
                                    s_text = :s_text
        
                                     WHERE s_id = :s_id""",
                                  {
                                        "s_text": beginning_story_edit_entry.get("1.0", "end"),
                                        "s_id": f'{id.story_id(s_id)}'
                                  })

                        # Show Success pop-up
                        messagebox.showinfo("Success", f"Story Number {s_id} has been successfully modified.")

                    else:
                        messagebox.showerror("Index Error", f"Paragraph Number {s_id} Does Not Exist")

                except sqlite3.OperationalError as e:
                    messagebox.showerror("Operational Error", "You Must Input A Story ID")
                    print(e)

            else:
                messagebox.showerror("Syntax Error", "Story ID Must Be Positive")

        except ValueError:
            messagebox.showerror("Syntax Error", "Story ID Must Be A Number")

    else:
        messagebox.showerror("Input Error", "You Must Write Something In The Beginning Paragraph")

    # Clear the Text Boxes
    story_id_edit_entry.delete(0, END)
    beginning_story_edit_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to insert already written text
def insert_edit():
    # Delete Previous Input
    beginning_story_edit_entry.delete("1.0", "end")

    # Create a connection
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    try:
        s_id = int(story_id_edit_entry.get())

        if s_id > 0:
            try:
                # Insert Stored Data Into Text Box
                s_id = story_id_edit_entry.get()
                c.execute(f"SELECT s_text FROM stories WHERE s_id = '{id.story_id(s_id)}'")
                text_raw = c.fetchall()
                original_text = ((text_raw[0])[0])

                # Input data into text box
                beginning_story_edit_entry.insert(END, str(original_text))

            except sqlite3.OperationalError:
                messagebox.showerror("Operational Error", "You Must Input A Story ID")

            except IndexError:
                messagebox.showerror("Index Error", f"Story Number {s_id} Does Not Exist")

        else:
            messagebox.showerror("Syntax Error", "Story ID Must Be Positive")

    except ValueError:
        messagebox.showerror("Syntax Error", "Story ID Must Be A Number")

    finally:
        conn.commit()
        conn.close()

        # Clear the Text Boxes
        story_id_edit_entry.delete(0, END)


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

    # Info Frame
    info_frame = LabelFrame(top_new_ed, height=frame_height, width=window_x_2)
    info_frame.pack(fill="both", expand=True, side=TOP)

    width_info = 42
    height = 10
    # Labels
    story_id_label = Label(info_frame, text="Select Story ID:", width=int(width_info/2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=height, pady=height, stick="w")

    beginning_label = Label(info_frame, text="Edit Text:", width=int(width_info/2), anchor=NW)
    beginning_label.grid(row=1, column=0, padx=height, pady=height, stick="nw")

    # Entries
    global story_id_edit_entry, beginning_story_edit_entry
    story_id_edit_entry = Entry(info_frame, width=48)
    story_id_edit_entry.grid(row=0, column=1, padx=height, pady=height)

    beginning_story_edit_entry = Text(info_frame, width=36)
    beginning_story_edit_entry.grid(row=1, column=1, padx=height, pady=height)

    # Buttons Frame
    button_frame = LabelFrame(top_new_ed, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    # Buttons
    width_buttons = 19
    save_story_button = Button(button_frame, text="Save Changes", width=width_buttons, command=edit_story)
    save_story_button.grid(row=0, column=0, padx=height, pady=height, stick="w")

    load_text_button = Button(button_frame, text="Load Text", width=width_buttons, command=insert_edit)
    load_text_button.grid(row=0, column=1, padx=height, pady=height, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=top_new_ed.destroy)
    cancel_button.grid(row=0, column=2, padx=height, pady=height, stick="w")

    top_new_ed.mainloop()


# Function to delete a story from the delete window
def delete_story():
    # Create connection to retrieve data
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    s_id = story_id_del_entry.get()

    try:
        c.execute(f"SELECT *, oid FROM stories WHERE s_id = '{id.story_id(s_id)}'")
        lt = c.fetchall()

        if not lt:
            messagebox.showerror("Index Error", f" Story ID Number {story_id_del_entry.get()} Does Not Exist")

        else:
            c.execute(f"DELETE FROM stories WHERE s_id = '{id.story_id(s_id)}'")

            # Show Success pop-up
            messagebox.showinfo("Success", f"Story Number {s_id} has been successfully deleted.")

    except sqlite3.OperationalError as e:
        messagebox.showerror("Operational Error", "You Must Input A Story ID")
        print(e)

    finally:
        old_text.set("")
        story_id_del_entry.delete(0, END)

        conn.commit()
        conn.close()


# Function to insert old text in a label in the delete story window
def insert_del():
    try:
        # Create connection to retrieve data
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        s_id = story_id_del_entry.get()
        c.execute(f"SELECT s_text FROM stories WHERE s_id = '{id.story_id(s_id)}'")
        text_raw = c.fetchall()
        original_text_2 = ((text_raw[0])[0])

        # Input data into text box
        old_text.set(str(original_text_2))

        conn.commit()
        conn.close()

    except IndexError as error:
        print(error)
        messagebox.showerror("Index Error", f"Story ID Number {story_id_del_entry.get()} Does Not Exist")

    except sqlite3.OperationalError as e:
        messagebox.showerror("Operational Error", "You Must Select A Story ID")
        print(e)

    finally:
        story_id_del_entry.delete(0, END)


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

    # Info Frame
    info_frame = LabelFrame(top_new_del, height=frame_height, width=window_x_2)
    info_frame.pack(fill="both", expand=True, side=TOP)

    width_info = 42
    height = 10

    # Labels
    story_id_label = Label(info_frame, text="Select Story ID:", width=int(width_info/2), anchor=W)
    story_id_label.grid(row=0, column=0, padx=height, pady=height, stick="w")

    text_label = Label(info_frame, text="Output:", width=int(width_info/2), anchor=NW)
    text_label.grid(row=1, column=0, padx=height, pady=height, stick="nw")

    # Entries
    global story_id_del_entry, story_del_message, old_text
    story_id_del_entry = Entry(info_frame, width=48)
    story_id_del_entry.grid(row=0, column=1, padx=height, pady=height)

    # Message Box
    old_text = StringVar()
    story_del_message = Message(info_frame, textvariable=old_text, width=280, anchor=W)
    story_del_message.grid(row=1, column=1, padx=height, pady=height, stick="w")

    # Buttons Frame
    button_frame = LabelFrame(top_new_del, height=window_y_2 - frame_height, width=window_x_2)
    button_frame.pack(fill="both", side=BOTTOM)

    # Buttons
    width_buttons = 19
    delete_text_button = Button(button_frame, text="Delete Text", width=width_buttons, command=delete_story)
    delete_text_button.grid(row=0, column=0, padx=height, pady=height, stick="w")

    check_text_button = Button(button_frame, text="Check Text", width=width_buttons, command=insert_del)
    check_text_button.grid(row=0, column=1, padx=height, pady=height, stick="w")

    cancel_button = Button(button_frame, text="Cancel", width=width_buttons, command=top_new_del.destroy)
    cancel_button.grid(row=0, column=2, padx=height, pady=height, stick="w")

    top_new_del.mainloop()
