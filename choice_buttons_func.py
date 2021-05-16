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


def c_new_insert():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_new_p_id = c_new_p_id_variable.get()

    # Insert Text
    c.execute(f"""SELECT ip_text FROM initial_paragraphs WHERE ip_id='{c_new_p_id}' UNION SELECT p_text FROM paragraphs WHERE p_id='{c_new_p_id}'""")
    c_new_text_raw = c.fetchall()
    c_new_text = ((c_new_text_raw[0])[0])

    c_new_p_text_var.delete("1.0", "end")
    c_new_p_text_var.insert(END, c_new_text)

    c_new_decoded_id.delete("1.0", "end")
    c_new_decoded_id.insert(END, id.decoder_3(c_new_p_id_variable.get()))

    # Insert Number of choices
    c.execute(f"""SELECT c_id FROM choices WHERE p_id='{c_new_p_id}'""")
    c_new_c_id_list_raw = c.fetchall()
    c_new_c_id_list = []

    # ok... i'll explain this
    # convert list of tuples into list
    for lt in c_new_c_id_list_raw:
        for item in lt:
            c_new_c_id_list.append(item)

    # Take only the ending number of each c_id and make a list of 'str' numbers with it
    c_new_c_id_numbers_list = []
    for c_id in c_new_c_id_list:
        c_new_c_id_numbers_list.append(id.id_int(c_id))

    # Convert the list of 'str' numbers to 'int' numbers
    for i in range(0, len(c_new_c_id_numbers_list)):
        c_new_c_id_numbers_list[i] = int(c_new_c_id_numbers_list[i])

    # Order the list of 'int' numbers from smallest to biggest
    sorted(c_new_c_id_numbers_list)
    c_new_c_id_numbers_final = sorted(c_new_c_id_numbers_list)

    # Convert each number into a 'str' with a comma
    c_new_c_id_numbers_text = ''
    for c_id in c_new_c_id_numbers_final:
        c_new_c_id_numbers_text += f'{c_id}, '

    c_new_c_id_counter_var.delete("1.0", "end")

    if c_new_c_id_list:
        c_new_c_id_counter_var.insert(END, f'Choices Number:\n{c_new_c_id_numbers_text[0:-2]}')

    else:
        c_new_c_id_counter_var.insert(END, 'No Existing Choices')

    conn.commit()
    conn.close()


def c_new_save():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS choices
    (s_id text,
    ip_id text,
    p_id text,
    c_id text,
    c_text text)""")

    # im not gonna explain this stuff 0_o
    c_new_s_id = c_new_s_id_variable.get()
    c_new_ip_id = c_new_p_id_variable.get()
    c_new_p_id = c_new_p_id_variable.get()
    c_new_c_id = c_new_get_choice_id_entry.get()
    c_new_c_text_length = len(c_new_choice_text_entry.get("1.0", "end"))
    c.execute(f"""SELECT c_id FROM choices WHERE c_id = '{c_new_p_id}_{id.c_id(c_new_c_id)}'""")
    c_new_c_id_raw = c.fetchall()
    c_new_d_p_id = id.decoder_2(c_new_p_id)[0]

    # I ran out of brain cells for this
    if f'{c_new_s_id}' == f'{c_new_d_p_id}':
        try:
            c_new_c_id = int(c_new_c_id)
            if c_new_c_text_length != 1:
                if len(c_new_c_id_raw) == 0:
                    if c_new_c_id > 0:
                        # Insert into table if that id does not exist
                        c.execute("INSERT INTO choices VALUES (:s_id, :ip_id, :p_id, :c_id, :c_text)",
                                  {
                                      "s_id": f"{c_new_s_id}",
                                      "ip_id": f"{c_new_ip_id}",
                                      "p_id": f"{c_new_p_id}",
                                      "c_id": f"{c_new_p_id}_{id.id_conv('c_id', c_new_c_id)}",
                                      "c_text": str(c_new_choice_text_entry.get("1.0", "end"))
                                  })
                        # Show Success pop-up
                        messagebox.showinfo("Success", f"Choice Number {c_new_c_id}\nIn Story Number {id.id_int(c_new_s_id)}\nhas been successfully created.")
                    else:
                        messagebox.showerror("Syntax Error", "Choice ID Must Be Positive")
                else:
                    messagebox.showerror("Duplication Error", f"Choice Number {c_new_c_id} Already Exists")
            else:
                messagebox.showerror("Input Error", "Choice Text Is Empty")

        except ValueError:
            messagebox.showerror("Syntax Error", "Story ID Must Be A Number")
    else:
        messagebox.showerror("ID Error", f"Choice's Story ID is {c_new_d_p_id} but Story ID is {c_new_s_id}")

    conn.commit()
    conn.close()

    c_new_get_choice_id_entry.delete(0, END)
    c_new_choice_text_entry.delete("1.0", "end")

    c_new_insert()


def c_new_window():
    global c_new_wd
    # Create New Window
    c_new_wd = Toplevel()
    c_new_wd.title("Create A New Choice")
    screen_x_2 = c_new_wd.winfo_screenwidth()
    screen_y_2 = c_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 943
    c_new_wd.minsize(window_x_2, window_y_2)
    c_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    c_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    c_new_frame_height = 200
    c_new_rest = window_y_2 - c_new_frame_height*2
    # Info Frame 1
    c_new_info_frame_1 = LabelFrame(c_new_wd, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    c_new_info_frame_2 = LabelFrame(c_new_wd, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_2.pack(fill="both", side=TOP, expand=True)

    # Top Button Frame
    c_new_button_frame_1 = LabelFrame(c_new_wd, height=c_new_rest / 2, width=window_x_2)
    c_new_button_frame_1.pack(fill="both")

    # Choice Frame
    c_new_choice_frame = LabelFrame(c_new_wd, width=window_x_2, height=c_new_frame_height)
    c_new_choice_frame.pack(fill="both")

    # Bottom Buttons Frame
    c_new_button_frame_2 = LabelFrame(c_new_wd, height=c_new_rest / 2, width=window_x_2)
    c_new_button_frame_2.pack(fill="both")

    c_new_width = 42
    c_new_pad = 10
    c_new_entry_width = 37
    # Labels
    c_new_get_story_id_label = Label(c_new_info_frame_1, text="Select Story ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_story_id_label.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_get_p_id_label = Label(c_new_info_frame_1, text="Select Paragraph ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_p_id_label.grid(row=1, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_decode_p_id_label = Label(c_new_info_frame_1, text="Decoded ID:", width=int(c_new_width / 2), anchor=NW)
    c_new_decode_p_id_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_choice_counter_label = Label(c_new_info_frame_1, text="This Paragraph Has:", width=int(c_new_width / 2),anchor=W)
    c_new_choice_counter_label.grid(row=3, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_p_text_label = Label(c_new_info_frame_2, text="Paragraph Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_p_text_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_get_c_id_label = Label(c_new_choice_frame, text="Enter Choice Number:", width=int(c_new_width / 2), anchor=NW)
    c_new_get_c_id_label.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_c_text_label = Label(c_new_choice_frame, text="Choice Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_c_text_label.grid(row=1, column=0, padx=(c_new_pad, c_new_pad+5), pady=c_new_pad, stick="nw")

    # Entries
    global c_new_choice_text_entry, c_new_p_text_var, c_new_get_choice_id_entry, c_new_decoded_id, c_new_c_id_counter_var
    c_new_get_choice_id_entry = Entry(c_new_choice_frame, width=49)
    c_new_get_choice_id_entry.grid(row=0, column=1, padx=c_new_pad, pady=c_new_pad)

    c_new_choice_text_entry = Text(c_new_choice_frame, width=c_new_entry_width, height=10)
    c_new_choice_text_entry.grid(row=1, column=1, padx=c_new_pad, pady=c_new_pad)

    # Message Box
    """c_new_p_message_var = StringVar()
    show_paragraph_message = Message(c_new_info_frame_2, textvariable=c_new_p_message_var, width=280, anchor=NW)
    show_paragraph_message.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="nw")"""

    c_new_p_text_var = Text(c_new_info_frame_2, width=c_new_entry_width, height=20)
    c_new_p_text_var.bind("<Key>", lambda a: "break")
    c_new_p_text_var.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    """c_new_decoded_id = StringVar()
    c_new_decoded_p_id_message = Message(c_new_info_frame_1, textvariable=c_new_decoded_id, width=280, anchor=NW)
    c_new_decoded_p_id_message.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="nw")"""

    c_new_decoded_id = Text(c_new_info_frame_1, width=c_new_entry_width, height=5)
    c_new_decoded_id.bind("<Key>", lambda a: "break")
    c_new_decoded_id.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    """c_new_c_id_counter_var = StringVar()
    c_new_c_id_counter_message = Message(c_new_info_frame_1, textvariable=c_new_c_id_counter_var, width=280, anchor=NW)
    c_new_c_id_counter_message.grid(row=3, column=1, padx=c_new_pad, pady=c_new_pad, stick="nw")"""

    c_new_c_id_counter_var = Text(c_new_info_frame_1, width=c_new_entry_width, height=2)
    c_new_c_id_counter_var.bind("<Key>", lambda a: "break")
    c_new_c_id_counter_var.grid(row=3, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    # Buttons
    c_new_submit_button = Button(c_new_button_frame_1, text="Submit", width=int(c_new_width / 2), command=c_new_insert)
    c_new_submit_button.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, ipadx=160)

    c_new_save_choice_button = Button(c_new_button_frame_2, text="Save Choice", width=int(c_new_width / 2), command=c_new_save)
    c_new_save_choice_button.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_cancel_button = Button(c_new_button_frame_2, text="Cancel", width=c_new_width, command=c_new_wd.destroy)
    c_new_cancel_button.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    global c_new_c_id_counter_message_func, c_new_p_id_opt_menu, c_new_s_id_opt_menu

    def c_new_s_id_opt_menu():
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs UNION SELECT s_id FROM initial_paragraphs""")
        c_new_s_id_list_raw = c.fetchall()
        c_new_s_id_list = []

        for tp in c_new_s_id_list_raw:
            for item in tp:
                c_new_s_id_list.append(item)

        if c_new_s_id_list:
            global c_new_s_id_variable
            c_new_s_id_variable = StringVar()
            c_new_s_id_variable.set(c_new_s_id_list[0])
            c_new_s_id_opt_menu_var = OptionMenu(c_new_info_frame_1, c_new_s_id_variable, *c_new_s_id_list)
            c_new_s_id_opt_menu_var.config(width=c_new_width)
            c_new_s_id_opt_menu_var.grid(row=0, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_new_wd.destroy()

        conn.commit()
        conn.close()

    c_new_s_id_opt_menu()

    def c_new_p_id_opt_menu():
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT ip_id FROM initial_paragraphs 
            UNION SELECT p_id FROM paragraphs
            UNION SELECT ip_id FROM choices""")
        c_new_p_id_list_raw = c.fetchall()
        c_new_p_id_list = []

        for tp in c_new_p_id_list_raw:
            for item in tp:
                c_new_p_id_list.append(item)

        if c_new_p_id_list:
            global c_new_p_id_variable
            c_new_p_id_variable = StringVar()
            c_new_p_id_variable.set(c_new_p_id_list[0])
            c_new_p_id_opt_menu_var = OptionMenu(c_new_info_frame_1, c_new_p_id_variable, *c_new_p_id_list)
            c_new_p_id_opt_menu_var.config(width=c_new_width)
            c_new_p_id_opt_menu_var.grid(row=1, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_new_wd.destroy()

        conn.commit()
        conn.close()

    c_new_p_id_opt_menu()

    c_new_wd.mainloop()


def c_edt_edit():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_edt_s_id = c_edt_s_id_variable.get()
    c_edt_c_id = c_edt_c_id_variable.get()
    if len(c_edt_edit_c_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE choices SET c_text = :c_text WHERE c_id = :c_id""",
                  {
                      "c_text": c_edt_edit_c_text_entry.get("1.0", "end"),
                      "c_id": f'{c_edt_c_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Choice Number {id.id_int(c_edt_c_id)} in Story Number {id.id_int(c_edt_s_id)} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Choice Text is Empty', icon='warning')

    # Clear the Text Boxes
    c_edt_edit_c_text_entry.delete("1.0", "end")

    conn.commit()
    conn.close()


# Function to insert already written choice
def c_edt_insert():
    # Delete Previous Input
    c_edt_edit_c_text_entry.delete("1.0", "end")

    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()

    c_id = c_edt_c_id_variable.get()

    c.execute(f"""SELECT c_text FROM choices WHERE c_id = '{c_id}'""")
    c_edt_text_raw = c.fetchall()
    c_edt_text = ((c_edt_text_raw[0])[0])

    # Input data into text box
    c_edt_edit_c_text_entry.insert(END, f'{c_edt_text}')

    conn.commit()
    conn.close()


# Function to insert decoded id
def c_edt_decode_id():
    c_edt_decode_id_variable.delete("1.0", "end")
    c_edt_decode_id_variable.insert(END, id.decoder_3(c_edt_c_id_variable.get()))


def c_del_delete():
    conn = sqlite3.connect("EditorDataV3.db")
    c = conn.cursor()
    c_del_s_id = c_edt_s_id_variable.get()
    c_del_c_id = c_edt_c_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Choice Number {id.id_int(c_del_c_id)}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM paragraphs WHERE c_id LIKE '{c_del_c_id}%'""")
        c.execute(f"""DELETE FROM choices WHERE c_id LIKE '{c_del_c_id}%'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Choice Number {id.id_int(c_del_c_id)} In Story Number {id.id_int(c_del_s_id)}\nhas been successfully deleted."
                                       f"\nAll Choices and Paragraphs connected to Choice Number {id.id_int(c_del_c_id)} were also Deleted.")

        c_edt_edit_c_text_entry.insert("1.0", "end")
        c_edt_decode_id_variable.insert("1.0", "end")

    conn.commit()
    conn.close()

    c_edt_s_id_opt_menu()
    c_edt_c_id_opt_menu()


# Function to open edit window
def c_edt__window():
    global c_edt_wd
    # Create New Window
    c_edt_wd = Toplevel()
    c_edt_wd.title("Edit Choices")
    screen_x_2 = c_edt_wd.winfo_screenwidth()
    screen_y_2 = c_edt_wd.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 663
    c_edt_wd.minsize(window_x_2, window_y_2)
    c_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    c_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    c_edt_frame_height = 400
    c_edt_info_frame_height = 57

    # Info Frame 1
    c_edt_info_frame_1 = LabelFrame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    c_edt_info_frame_2 = LabelFrame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    c_edt_info_frame_3 = LabelFrame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_3.pack(fill="both", side=TOP)

    # Info Frame 4
    c_edt_info_frame_4 = LabelFrame(c_edt_wd, height=c_edt_frame_height, width=window_x_2)
    c_edt_info_frame_4.pack(fill="both", side=TOP, expand=True)

    # Buttons Frame
    c_edt_button_frame = LabelFrame(c_edt_wd, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_button_frame.pack(fill="both", side=BOTTOM)

    c_edt_entry_width = 37
    c_edt_width = 42
    c_edt_pad = 10

    # Labels
    c_edt_story_id_label = Label(c_edt_info_frame_1, text="Select Choice ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_story_id_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_decode_id_label = Label(c_edt_info_frame_2, text="Decoded ID:", width=int(c_edt_width / 2), anchor=NW)
    c_edt_decode_id_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    c_edt_edit_c_text_label = Label(c_edt_info_frame_4, text="Edit Choice:", width=int(c_edt_width / 2) - 1, anchor=NW)
    c_edt_edit_c_text_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    global c_edt_decode_id_variable, c_edt_edit_c_text_entry

    # Message
    c_edt_decode_id_variable = Text(c_edt_info_frame_2, width=c_edt_entry_width, height=5)
    c_edt_decode_id_variable.bind("<Key>", lambda a: "break")
    c_edt_decode_id_variable.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Text Entry
    c_edt_edit_c_text_entry = Text(c_edt_info_frame_4, width=c_edt_entry_width, height=20)
    c_edt_edit_c_text_entry.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Buttons
    c_edt_submit_id_button = Button(c_edt_info_frame_3, text="Decode ID", width=int(c_edt_width / 2), command=c_edt_decode_id)
    c_edt_submit_id_button.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w", ipadx=157)

    p_edt_width_buttons = 13
    p_edt_save_story_button = Button(c_edt_button_frame, text="Save Changes", width=p_edt_width_buttons,
                                     command=c_edt_edit)
    p_edt_save_story_button.grid(row=0, column=0, padx=(c_edt_pad + 3, c_edt_pad), pady=c_edt_pad, stick="w")

    p_edt_load_text_button = Button(c_edt_button_frame, text="Load Choice", width=p_edt_width_buttons,
                                    command=c_edt_insert)
    p_edt_load_text_button.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    p_edt_delete_text_button = Button(c_edt_button_frame, text="Delete Choice", width=p_edt_width_buttons,
                                      command=c_del_delete)
    p_edt_delete_text_button.grid(row=0, column=2, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    p_edt_cancel_button = Button(c_edt_button_frame, text="Cancel", width=p_edt_width_buttons,
                                 command=c_edt_wd.destroy)
    p_edt_cancel_button.grid(row=0, column=3, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    global c_edt_s_id_opt_menu, c_edt_c_id_opt_menu

    def c_edt_s_id_opt_menu():
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices""")
        c_edt_s_id_list_raw = c.fetchall()
        c_edt_s_id_list = []

        for tp in c_edt_s_id_list_raw:
            for item in tp:
                c_edt_s_id_list.append(item)

        if c_edt_s_id_list:
            global c_edt_s_id_variable
            c_edt_s_id_variable = StringVar()
            c_edt_s_id_variable.set(c_edt_s_id_list[0])
            c_edt_s_id_opt_menu_var = OptionMenu(c_edt_info_frame_1, c_edt_s_id_variable, *c_edt_s_id_list)
            c_edt_s_id_opt_menu_var.config(width=c_edt_width)
            c_edt_s_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_edt_wd.destroy()

        conn.commit()
        conn.close()

    def c_edt_c_id_opt_menu():
        conn = sqlite3.connect("EditorDataV3.db")
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices """)
        c_edt_c_id_list_raw = c.fetchall()
        c_edt_c_id_list = []

        for tp in c_edt_c_id_list_raw:
            for item in tp:
                c_edt_c_id_list.append(item)

        if c_edt_c_id_list:
            global c_edt_c_id_variable
            c_edt_c_id_variable = StringVar()
            c_edt_c_id_variable.set(c_edt_c_id_list[0])
            c_edt_c_id_opt_menu_var = OptionMenu(c_edt_info_frame_1, c_edt_c_id_variable, *c_edt_c_id_list)
            c_edt_c_id_opt_menu_var.config(width=c_edt_width)
            c_edt_c_id_opt_menu_var.grid(row=1, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            c_new_wd.destroy()

        conn.commit()
        conn.close()

    c_edt_s_id_opt_menu()
    c_edt_c_id_opt_menu()

    c_edt_wd.mainloop()