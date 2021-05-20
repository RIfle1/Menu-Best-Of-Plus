# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id

database = "EditorDataV3.db"


def c_new_insert():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c_new_p_id = c_new_from_p_id_variable.get()

    # Insert Text
    c.execute(f"""SELECT ip_text FROM initial_paragraphs WHERE ip_id='{c_new_p_id}' UNION SELECT p_text FROM paragraphs_list WHERE pl_id='{c_new_p_id}'""")
    c_new_text_raw = c.fetchall()
    c_new_text = ((c_new_text_raw[0])[0])

    c_new_p_text_var.delete("1.0", "end")
    c_new_p_text_var.insert(END, c_new_text)

    c_new_decoded_id.delete("1.0", "end")
    c_new_decoded_id.insert(END, id.decoder_3(c_new_from_p_id_variable.get()))

    # Insert Number of choices
    c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE '{c_new_p_id}%'""")
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
        # Sorting system for c_id with and without assigned paragraph
        if id.id_str(id.decoder_2(c_id)[-1]) == 'P':
            c_new_c_id_numbers_list.append(id.id_int(id.decoder_2(c_id)[-2]))
        else:
            c_new_c_id_numbers_list.append(id.id_int(id.decoder_2(c_id)[-1]))

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
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS choices
    (s_id text,
    ip_id text,
    c_id text,
    c_text text)""")

    # i'll explain it...
    c_new_s_id = c_new_s_id_variable.get()
    c_new_ip_id = id.ip_id(c_new_s_id)

    # Id sandwich
    c_new_from_p_id = id.decoder_2(c_new_from_p_id_variable.get())[-1]
    c_new_c_number = c_new_get_choice_id_entry.get()

    if c_new_to_p_id_variable.get() == 'Assign No Paragraph':
        c_new_to_p_id = ''
        c_new_c_id = f'{c_new_s_id}_{c_new_from_p_id}_C{c_new_c_number}'
    else:
        c_new_to_p_id = id.decoder_2(c_new_to_p_id_variable.get())[-1]
        c_new_c_id = f'{c_new_s_id}_{c_new_from_p_id}_C{c_new_c_number}_{c_new_to_p_id}'

    c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE '{c_new_from_p_id}%'""")
    c_new_c_id_list_raw = c.fetchall()
    c_new_c_id_list = id.raw_conv(c_new_c_id_list_raw)

    # Take only the ending number of each c_id and make a list of 'str' numbers with it
    c_new_c_id_numbers_list = []
    for c_id in c_new_c_id_list:
        # Sorting system for c_id with and without assigned paragraph
        if id.id_str(id.decoder_2(c_id)[-1]) == 'P':
            c_new_c_id_numbers_list.append(id.id_int(id.decoder_2(c_id)[-2]))
        else:
            c_new_c_id_numbers_list.append(id.id_int(id.decoder_2(c_id)[-1]))

    print(c_new_c_id_numbers_list)

    # Vars for coherence checking
    c_new_from_s_id = id.decoder_2(c_new_from_p_id_variable.get())[0]
    c_new_to_s_id = id.decoder_2(c_new_to_p_id_variable.get())[0]

    # All possible errors
    c_new_c_text_length = len(c_new_choice_text_entry.get("1.0", "end"))
    if c_new_c_number not in c_new_c_id_numbers_list:
        if c_new_from_p_id != c_new_to_p_id:
            if f'{c_new_s_id}' == f'{c_new_from_s_id}' == f'{c_new_to_s_id}' or c_new_to_p_id == '':
                try:
                    c_new_c_number = int(c_new_c_number)
                    if c_new_c_text_length != 1:
                        if c_new_c_number > 0:
                            c.execute("INSERT INTO choices VALUES (:s_id, :ip_id, :c_id, :c_text)",
                                      {
                                          "s_id": f"{c_new_s_id}",
                                          "ip_id": f"{c_new_ip_id}",
                                          "c_id": f"{c_new_c_id}",
                                          "c_text": str(c_new_choice_text_entry.get("1.0", "end"))
                                      })
                            messagebox.showinfo("Success",
                                                f"Choice Number {c_new_c_number}\nIn Paragraph {id.id_int(c_new_from_p_id)}\nhas been successfully created.")
                        else:
                            messagebox.showerror("Syntax Error", "Choice ID Must Be Positive")
                    else:
                        messagebox.showerror("Input Error", "Choice Text Is Empty")
                except ValueError:
                    messagebox.showerror("Syntax Error", "Story ID Must Be A Number")
            else:
                messagebox.showerror("ID Error", f"Choice's Story ID is {c_new_from_s_id} but Story ID is {c_new_s_id}")
        else:
            messagebox.showerror("Loop Error", "From Paragraph ID And To Paragraph ID Must Be Different")
    else:
        messagebox.showerror("Duplication Error", f"Choice Number {c_new_c_number} Already Exists")

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
    window_x_2 = 1000
    window_y_2 = 672
    c_new_wd.minsize(window_x_2, window_y_2)
    c_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    c_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    c_new_frame_height = 200
    c_new_rest = window_y_2 - c_new_frame_height*2
    print(int(c_new_rest/2))
    # Info Frame 0_1
    c_new_info_frame_0_1 = Frame(c_new_wd, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_0_1.pack(fill="both", side=TOP)

    # Info Frame 1
    c_new_info_frame_1 = LabelFrame(c_new_info_frame_0_1, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_1.pack(fill="both", side=LEFT)

    # Info Frame 2
    c_new_info_frame_2 = LabelFrame(c_new_info_frame_0_1, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_2.pack(fill="both", side=RIGHT, expand=True)

    # Top Button Frame
    c_new_button_frame_1 = LabelFrame(c_new_wd, height=c_new_rest / 2, width=window_x_2)
    c_new_button_frame_1.pack(fill="both")

    # Info Frame 0_2
    c_new_info_frame_0_2 = LabelFrame(c_new_wd, width=window_x_2, height=c_new_frame_height)
    c_new_info_frame_0_2.pack(fill="y")

    # Choice Create Frame
    c_new_choice_create_frame = Frame(c_new_info_frame_0_2, height=c_new_frame_height)
    c_new_choice_create_frame.pack(fill="y")

    # Bottom Buttons Create Frame
    c_new_button_frame_2 = Frame(c_new_info_frame_0_2, height=c_new_rest / 12)
    c_new_button_frame_2.pack(fill="y")

    c_new_width = 41
    c_new_pad = 10
    c_new_entry_width = 37
    # Labels
    c_new_get_story_id_label = Label(c_new_info_frame_1, text="Select Story ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_story_id_label.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_get_p_id_label = Label(c_new_info_frame_1, text="From Paragraph ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_p_id_label.grid(row=1, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_get_p_id_label = Label(c_new_info_frame_1, text="To Paragraph ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_p_id_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_decode_p_id_label = Label(c_new_info_frame_1, text="Decoded ID:", width=int(c_new_width / 2), anchor=NW)
    c_new_decode_p_id_label.grid(row=3, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_choice_counter_label = Label(c_new_info_frame_1, text="The Paragraph From Has:", width=int(c_new_width / 2),anchor=W)
    c_new_choice_counter_label.grid(row=4, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_p_text_label = Label(c_new_info_frame_2, text="Paragraph Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_p_text_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_get_c_id_label = Label(c_new_choice_create_frame, text="Enter Choice Number:", width=int(c_new_width / 2), anchor=NW)
    c_new_get_c_id_label.grid(row=0, column=0, padx=(c_new_pad, c_new_pad-5), pady=c_new_pad, stick="nw")

    c_new_c_text_label = Label(c_new_choice_create_frame, text="Choice Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_c_text_label.grid(row=1, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    # Entries
    global c_new_choice_text_entry, c_new_p_text_var, c_new_get_choice_id_entry, c_new_decoded_id, c_new_c_id_counter_var
    c_new_get_choice_id_entry = Entry(c_new_choice_create_frame, width=49)
    c_new_get_choice_id_entry.grid(row=0, column=1, padx=c_new_pad, pady=c_new_pad)

    c_new_choice_text_entry = Text(c_new_choice_create_frame, width=c_new_entry_width, height=10)
    c_new_choice_text_entry.grid(row=1, column=1, padx=c_new_pad, pady=c_new_pad)

    # Message Box
    c_new_p_text_var = Text(c_new_info_frame_2, width=c_new_entry_width, height=20)
    c_new_p_text_var.bind("<Key>", lambda a: "break")
    c_new_p_text_var.grid(row=2, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_decoded_id = Text(c_new_info_frame_1, width=c_new_entry_width, height=5)
    c_new_decoded_id.bind("<Key>", lambda a: "break")
    c_new_decoded_id.grid(row=3, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_c_id_counter_var = Text(c_new_info_frame_1, width=c_new_entry_width, height=2)
    c_new_c_id_counter_var.bind("<Key>", lambda a: "break")
    c_new_c_id_counter_var.grid(row=4, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    # Buttons Save choice
    c_new_submit_button = Button(c_new_button_frame_1, text="Load Information", width=int(c_new_width / 2), command=c_new_insert)
    c_new_submit_button.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, ipadx=412)

    c_new_save_choice_button = Button(c_new_button_frame_2, text="Save Choice", width=int(c_new_width / 2), command=c_new_save)
    c_new_save_choice_button.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_cancel_button = Button(c_new_button_frame_2, text="Cancel", width=c_new_width, command=c_new_wd.destroy)
    c_new_cancel_button.grid(row=2, column=1, padx=(c_new_pad-1, c_new_pad), pady=c_new_pad, stick="w")

    global c_new_c_id_counter_message_func, c_new_from_p_id_opt_menu, c_new_s_id_opt_menu, c_new_to_p_id_opt_menu

    def c_new_s_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM initial_paragraphs""")
        c_new_s_id_list_raw = c.fetchall()
        c_new_s_id_list = id.raw_conv(c_new_s_id_list_raw)

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

    def c_new_from_p_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list UNION SELECT ip_id FROM initial_paragraphs""")
        c_new_from_p_id_list_raw = c.fetchall()
        c_new_from_p_id_list = id.raw_conv(c_new_from_p_id_list_raw)

        if c_new_from_p_id_list:
            global c_new_from_p_id_variable
            c_new_from_p_id_variable = StringVar()
            c_new_from_p_id_variable.set(c_new_from_p_id_list[0])
            c_new_from_p_id_opt_menu_var = OptionMenu(c_new_info_frame_1, c_new_from_p_id_variable, *c_new_from_p_id_list)
            c_new_from_p_id_opt_menu_var.config(width=c_new_width)
            c_new_from_p_id_opt_menu_var.grid(row=1, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")
        else:
            messagebox.showerror("Index Error", "No Existing 'From Paragraphs' Found")
            c_new_wd.destroy()

        conn.commit()
        conn.close()

    c_new_from_p_id_opt_menu()

    def c_new_to_p_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list""")
        c_new_to_p_id_list_raw = c.fetchall()
        c_new_to_p_id_list = id.raw_conv(c_new_to_p_id_list_raw)

        global c_new_to_p_id_variable
        c_new_to_p_id_variable = StringVar()
        c_new_to_p_id_list.append('Assign No Paragraph')
        c_new_to_p_id_variable.set(c_new_to_p_id_list[-1])
        c_new_to_p_id_opt_menu_var = OptionMenu(c_new_info_frame_1, c_new_to_p_id_variable, *c_new_to_p_id_list)
        c_new_to_p_id_opt_menu_var.config(width=c_new_width)
        c_new_to_p_id_opt_menu_var.grid(row=2, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

        conn.commit()
        conn.close()


    c_new_to_p_id_opt_menu()

    c_new_wd.mainloop()


def c_edt_edit():
    conn = sqlite3.connect(database)
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

    conn = sqlite3.connect(database)
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

    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute(f"""SELECT p_text FROM paragraphs_list WHERE pl_id='{c_edt_pl_id_variable.get()}'""")
    c_edt_pl_text_raw = c.fetchall()
    c_edt_pl_text = id.raw_conv(c_edt_pl_text_raw)

    conn.commit()
    conn.close()

    c_edt_pl_text_variable.delete("1.0", "end")
    c_edt_pl_text_variable.insert(END, c_edt_pl_text)


def c_del_delete():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c_del_s_id = c_edt_s_id_variable.get()
    c_del_c_id = c_edt_c_id_variable.get()

    warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Choice Number {id.id_int(c_del_c_id)}?', icon='warning')

    if warning == 'yes':
        c.execute(f"""DELETE FROM choices WHERE c_id = '{c_del_c_id}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Choice Number {id.id_int(c_del_c_id)} In Story Number {id.id_int(c_del_s_id)}\nhas been successfully deleted."
                                       f"\nAll Choices and Paragraphs connected to Choice Number {id.id_int(c_del_c_id)} were also Deleted.")

        c_edt_edit_c_text_entry.delete("1.0", "end")
        c_edt_decode_id_variable.delete("1.0", "end")

    conn.commit()
    conn.close()

    c_edt_s_id_opt_menu()
    c_edt_c_id_opt_menu()


def c_edt_assign_save():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Get pl_id and old c_id
    c_edt_c_id = c_edt_c_id_variable.get()
    c_edt_pl_id = id.decoder_2(c_edt_pl_id_variable.get())[1]

    # Get Paragraph Number "From Paragraph"
    c_edt_pl_id_from_num = id.id_int(id.decoder_2(c_edt_c_id)[1])

    # Get Paragraph Number "To Paragraph"
    c_edt_pl_id_to_num = id.id_int(c_edt_pl_id)

    # Assign 0 If the paragraph ID is 'IP'
    c_edt_c_id_p_from_num = id.id_int(id.decoder_2(c_edt_c_id)[1])
    if c_edt_c_id_p_from_num == 'IP':
        c_edt_c_id_p_from_num = 0
    else:
        c_edt_c_id_p_from_num = int(c_edt_c_id_p_from_num)

    # Get Number of choice
    c_edt_c_id_num = id.id_int(id.decoder_2(c_edt_c_id)[2])

    # Create new c_id
    c_edt_new_c_id = f'{c_edt_c_id}_{c_edt_pl_id}'

    # Create reversed c_id to avoid loops
    c_edt_rev_c_id_1 = id.loop_1(c_edt_new_c_id)
    c_edt_rev_c_id_2 = id.loop_2(c_edt_new_c_id)

    # Check if the reversed id already exists in the database
    c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE'{c_edt_rev_c_id_1}%{c_edt_rev_c_id_2}'""")
    c_edt_c_id_check_raw = c.fetchall()
    c_edt_c_id_check = id.raw_conv(c_edt_c_id_check_raw)

    c_edt_d_c_id = id.decoder_2(c_edt_c_id)[1]

    if int(c_edt_pl_id_to_num) > c_edt_c_id_p_from_num:
        if not c_edt_c_id_check:
            if id.id_str(id.decoder_2(c_edt_c_id)[-1]) == 'C':
                if c_edt_pl_id != c_edt_d_c_id:
                    c.execute("""UPDATE choices SET c_id = :c_id_new WHERE c_id = :c_id_old""",
                              {
                                  "c_id_new": f"{c_edt_new_c_id}",
                                  "c_id_old": f'{c_edt_c_id}'
                              })
                    messagebox.showinfo('Success', f"Choice Number {c_edt_c_id_num} in Paragraph {c_edt_pl_id_from_num} Has Been sucessfully assigned to Paragraph {c_edt_pl_id_to_num}")
                else:
                    messagebox.showerror('Assignment Error', "Choice Can't Loop Back To Root Paragraph", icon='warning')
            else:
                messagebox.showerror('Loop Error', f"Choice Number {c_edt_c_id_num} Already Has A 'To Paragraph' Assigned.", icon='warning')
        else:
            messagebox.showerror('Loop Error', f"Assigning Choice Number {c_edt_c_id_num} To Paragraph Number {c_edt_pl_id_from_num} Will Create A Loop.", icon='warning')
    else:
        messagebox.showerror('Priority Error', f"'To Paragraph' ID ({c_edt_c_id_p_from_num}) has to be Bigger than 'From Paragraph' ID ({c_edt_pl_id_from_num})", icon='warning')

    conn.commit()
    conn.close()

    c_edt_c_id_opt_menu()


def c_del_assign_delete():
    pass


# Function to open edit window
def c_edt_window():
    global c_edt_wd
    # Create New Window
    c_edt_wd = Toplevel()
    c_edt_wd.title("Edit Choices")
    screen_x_2 = c_edt_wd.winfo_screenwidth()
    screen_y_2 = c_edt_wd.winfo_screenheight()
    window_x_2 = 1000
    window_y_2 = 703
    c_edt_wd.minsize(window_x_2, window_y_2)
    c_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    c_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    c_edt_frame_height = 400
    c_edt_info_frame_height = 57

    # Info Frame 0_1
    c_edt_info_frame_0_1 = LabelFrame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_0_1.pack(fill="y", side=TOP)

    # Info Frame 1
    c_edt_info_frame_1 = Frame(c_edt_info_frame_0_1, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_1.pack(fill="y")

    # Info Frame 2
    c_edt_info_frame_2 = Frame(c_edt_info_frame_0_1, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_2.pack(fill="y")

    # Info Frame 3
    c_edt_info_frame_3 = Frame(c_edt_info_frame_0_1, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_3.pack(fill="y")

    # Info Frame 0_2
    c_edt_info_frame_0_2 = LabelFrame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_0_2.pack(fill="both")

    # Edit Choice Frame
    c_edt_edit_choice_frame = LabelFrame(c_edt_info_frame_0_2, height=c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_frame.pack(fill="both", side=LEFT)

    # Edit Choice Text Frame
    c_edt_edit_choice_text_frame = Frame(c_edt_edit_choice_frame, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_text_frame.pack(fill="both")

    # Edit Choice Buttons Frame
    c_edt_edit_choice_button_frame = Frame(c_edt_edit_choice_frame, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_button_frame.pack(fill="both")

    # Assign Choice Frame
    c_edt_assign_choice_frame = LabelFrame(c_edt_info_frame_0_2, height=c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_frame.pack(fill="both", side=RIGHT, expand=True)

    # Assign Choice Select Frame
    c_edt_assign_choice_select_frame = Frame(c_edt_assign_choice_frame, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_select_frame.pack(fill="both")

    # Assign Choice Buttons Frame
    c_edt_assign_choice_button_frame = Frame(c_edt_assign_choice_frame, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_button_frame.pack(fill="both")

    c_edt_entry_width = 37
    c_edt_width = 42
    c_edt_pad = 10

    # Labels
    c_edt_story_id_label = Label(c_edt_info_frame_1, text="Select Story ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_story_id_label.grid(row=0, column=0, padx=c_edt_pad-3, pady=c_edt_pad, stick="w")

    c_edt_choice_id_label = Label(c_edt_info_frame_1, text="Select Choice ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_choice_id_label.grid(row=1, column=0, padx=c_edt_pad-3, pady=c_edt_pad, stick="w")

    c_edt_to_p_id_label = Label(c_edt_info_frame_1, text="Select 'To Paragraph' ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_to_p_id_label.grid(row=2, column=0, padx=c_edt_pad - 3, pady=c_edt_pad, stick="w")

    c_edt_decode_id_label = Label(c_edt_info_frame_2, text="Decoded Choice ID:", width=int(c_edt_width / 2), anchor=NW)
    c_edt_decode_id_label.grid(row=0, column=0, padx=c_edt_pad-2, pady=c_edt_pad, stick="nw")

    c_edt_edit_c_text_label = Label(c_edt_edit_choice_text_frame, text="Edit Choice:", width=int(c_edt_width / 2) - 1, anchor=NW)
    c_edt_edit_c_text_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    c_edt_edit_c_text_label = Label(c_edt_assign_choice_select_frame, text="'To Paragraph' Text:", width=int(c_edt_width / 2) - 1, anchor=NW)
    c_edt_edit_c_text_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    global c_edt_decode_id_variable, c_edt_edit_c_text_entry, c_edt_pl_text_variable

    # Message
    c_edt_decode_id_variable = Text(c_edt_info_frame_2, width=c_edt_entry_width, height=5)
    c_edt_decode_id_variable.bind("<Key>", lambda a: "break")
    c_edt_decode_id_variable.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_pl_text_variable = Text(c_edt_assign_choice_select_frame, width=c_edt_entry_width, height=20)
    c_edt_pl_text_variable.bind("<Key>", lambda a: "break")
    c_edt_pl_text_variable.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Text Entry
    c_edt_edit_c_text_entry = Text(c_edt_edit_choice_text_frame, width=c_edt_entry_width, height=20)
    c_edt_edit_c_text_entry.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Button Submit
    c_edt_submit_id_button = Button(c_edt_info_frame_3, text="Submit Information", width=int(c_edt_width / 2), command=c_edt_decode_id)
    c_edt_submit_id_button.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w", ipadx=157)

    # Buttons Edit Choice
    p_edt_width_buttons = 13
    p_edt_save_choice_button = Button(c_edt_edit_choice_button_frame, text="Save Changes", width=p_edt_width_buttons,
                                     command=c_edt_edit)
    p_edt_save_choice_button.grid(row=0, column=0, padx=(c_edt_pad + 3, c_edt_pad), pady=c_edt_pad, stick="w")

    p_edt_load_choice_button = Button(c_edt_edit_choice_button_frame, text="Load Choice", width=p_edt_width_buttons,
                                    command=c_edt_insert)
    p_edt_load_choice_button.grid(row=0, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    p_edt_delete_choice_button = Button(c_edt_edit_choice_button_frame, text="Delete Choice", width=p_edt_width_buttons,
                                      command=c_del_delete)
    p_edt_delete_choice_button.grid(row=0, column=2, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    p_edt_cancel_button = Button(c_edt_edit_choice_button_frame, text="Cancel", width=p_edt_width_buttons,
                                 command=c_edt_wd.destroy)
    p_edt_cancel_button.grid(row=0, column=3, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Buttons Assign Choice
    p_edt_width_buttons_2 = 31
    p_edt_save_p_to_c_button = Button(c_edt_assign_choice_button_frame, text="Assign Paragraph To Choice", width=p_edt_width_buttons_2, command=c_edt_assign_save)
    p_edt_save_p_to_c_button.grid(row=0, column=0, padx=(c_edt_pad + 3, c_edt_pad), pady=c_edt_pad, stick="w")

    p_edt_delete_p_from_c_button = Button(c_edt_assign_choice_button_frame, text="Delete Paragraph From Choice", width=p_edt_width_buttons_2, command=c_del_assign_delete)
    p_edt_delete_p_from_c_button.grid(row=0, column=2, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    global c_edt_s_id_opt_menu, c_edt_c_id_opt_menu

    def c_edt_s_id_opt_menu():
        conn = sqlite3.connect(database)
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
            c_edt_s_id_opt_menu_var.config(width=c_edt_width+1)
            c_edt_s_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_edt_wd.destroy()

        conn.commit()
        conn.close()

    def c_edt_c_id_opt_menu():
        conn = sqlite3.connect(database)
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
            c_edt_c_id_opt_menu_var.config(width=c_edt_width+1)
            c_edt_c_id_opt_menu_var.grid(row=1, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            c_new_wd.destroy()

        conn.commit()
        conn.close()

    def c_edt_pl_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list""")
        c_edt_pl_id_list_raw = c.fetchall()
        c_edt_pl_id_list = []

        for tp in c_edt_pl_id_list_raw:
            for item in tp:
                c_edt_pl_id_list.append(item)

        if c_edt_pl_id_list:
            global c_edt_pl_id_variable
            c_edt_pl_id_variable = StringVar()
            c_edt_pl_id_variable.set(c_edt_pl_id_list[0])
            c_edt_pl_id_opt_menu_var = OptionMenu(c_edt_info_frame_1, c_edt_pl_id_variable, *c_edt_pl_id_list)
            c_edt_pl_id_opt_menu_var.config(width=c_edt_width+1)
            c_edt_pl_id_opt_menu_var.grid(row=2, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            c_edt_wd.destroy()

        conn.commit()
        conn.close()

    c_edt_pl_id_opt_menu()
    c_edt_s_id_opt_menu()
    c_edt_c_id_opt_menu()

    c_edt_wd.mainloop()