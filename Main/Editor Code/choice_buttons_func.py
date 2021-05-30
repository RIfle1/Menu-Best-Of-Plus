# Imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id
import editor_settings
import test_buttons_func


def style_func():
    c_font_size = 11
    c_style = ttk.Style()
    c_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', c_font_size))
    c_style.configure("TButton", font=('Times New Roman', c_font_size))
    c_style.configure("TLabel", font=('Times New Roman', c_font_size))


def c_new_insert():
    conn = sqlite3.connect(database, uri=True)
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


def c_new_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS choices
    (s_id text,
    ip_id text,
    c_id text,
    con_id text,
    obj_id text,
    c_text text)""")

    c_new_s_id = c_new_s_id_variable.get()
    c_new_ip_id = id.ip_id(c_new_s_id)

    # Id sandwich
    c_new_from_p_id = id.decoder_2(c_new_from_p_id_variable.get())[-1]
    c_new_p_id = c_new_from_p_id_variable.get()
    c_new_c_number = c_new_get_choice_id_entry.get()

    if c_new_to_p_id_variable.get() == 'Assign No Paragraph':
        c_new_to_p_id = ''
        c_new_c_id = f'{c_new_s_id}_{c_new_from_p_id}_C{c_new_c_number}'
    else:
        c_new_to_p_id = id.decoder_2(c_new_to_p_id_variable.get())[-1]
        c_new_c_id = f'{c_new_s_id}_{c_new_from_p_id}_C{c_new_c_number}_{c_new_to_p_id}'

    c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE '{c_new_p_id}%'""")
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
                            c.execute("INSERT INTO choices VALUES (:s_id, :ip_id, :c_id, :con_id, :obj_id, :c_text)",
                                      {
                                          "s_id": f"{c_new_s_id}",
                                          "ip_id": f"{c_new_ip_id}",
                                          "c_id": f"{c_new_c_id}",
                                          "con_id": 'None',
                                          "obj_id": 'None',
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

    c_new_get_choice_id_entry.delete(0, END)
    c_new_choice_text_entry.delete("1.0", "end")

    c_new_insert()


def c_new_window():
    style_func()
    global c_new_wd, database
    database = editor_settings.database_module.database
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
    c_new_get_story_id_label = ttk.Label(c_new_info_frame_1, text="Select Story ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_story_id_label.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_get_p_id_label = ttk.Label(c_new_info_frame_1, text="From Paragraph ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_p_id_label.grid(row=1, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_get_p_id_label = ttk.Label(c_new_info_frame_1, text="To Paragraph ID:", width=int(c_new_width / 2), anchor=W)
    c_new_get_p_id_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_decode_p_id_label = ttk.Label(c_new_info_frame_1, text="Decoded ID:", width=int(c_new_width / 2), anchor=NW)
    c_new_decode_p_id_label.grid(row=3, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_choice_counter_label = ttk.Label(c_new_info_frame_1, text="The 'Paragraph From'\nHas:", width=int(c_new_width / 2),anchor=W)
    c_new_choice_counter_label.grid(row=4, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_p_text_label = ttk.Label(c_new_info_frame_2, text="Paragraph Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_p_text_label.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    c_new_get_c_id_label = ttk.Label(c_new_choice_create_frame, text="Enter Choice Number:", width=int(c_new_width / 2), anchor=NW)
    c_new_get_c_id_label.grid(row=0, column=0, padx=(c_new_pad, c_new_pad-5), pady=c_new_pad, stick="nw")

    c_new_c_text_label = ttk.Label(c_new_choice_create_frame, text="Choice Text:", width=int(c_new_width / 2), anchor=NW)
    c_new_c_text_label.grid(row=1, column=0, padx=c_new_pad, pady=c_new_pad, stick="nw")

    # Entries
    global c_new_choice_text_entry, c_new_p_text_var, c_new_get_choice_id_entry, c_new_decoded_id, c_new_c_id_counter_var
    c_new_get_choice_id_entry = ttk.Entry(c_new_choice_create_frame, width=49)
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

    c_new_c_id_counter_var = Text(c_new_info_frame_1, width=c_new_entry_width, height=5)
    c_new_c_id_counter_var.bind("<Key>", lambda a: "break")
    c_new_c_id_counter_var.grid(row=4, column=1, padx=c_new_pad, pady=c_new_pad, stick="w")

    # Buttons Save choice
    c_new_submit_button = ttk.Button(c_new_button_frame_1, text="Load Information", width=int(c_new_width / 2), command=c_new_insert)
    c_new_submit_button.grid(row=0, column=0, padx=c_new_pad, pady=c_new_pad, ipadx=412)

    c_new_save_choice_button = ttk.Button(c_new_button_frame_2, text="Save Choice", width=int(c_new_width / 2), command=c_new_save)
    c_new_save_choice_button.grid(row=2, column=0, padx=c_new_pad, pady=c_new_pad, stick="w")

    c_new_cancel_button = ttk.Button(c_new_button_frame_2, text="Cancel", width=c_new_width, command=c_new_wd.destroy)
    c_new_cancel_button.grid(row=2, column=1, padx=(c_new_pad-1, c_new_pad), pady=c_new_pad, stick="w")

    global c_new_c_id_counter_message_func, c_new_from_p_id_opt_menu, c_new_s_id_opt_menu, c_new_to_p_id_opt_menu

    def c_new_s_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM initial_paragraphs ORDER BY s_id""")
        c_new_s_id_list_raw = c.fetchall()
        c_new_s_id_list = id.raw_conv(c_new_s_id_list_raw)

        if c_new_s_id_list:
            global c_new_s_id_variable
            c_new_s_id_variable = StringVar()
            c_new_s_id_opt_menu_var = ttk.OptionMenu(c_new_info_frame_1, c_new_s_id_variable, c_new_s_id_list[0], *c_new_s_id_list)
            c_new_s_id_opt_menu_var.grid(row=0, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

            c_new_from_p_id_opt_menu()

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_new_wd.destroy()

        conn.commit()

    def c_new_from_p_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list UNION SELECT ip_id FROM initial_paragraphs EXCEPT SELECT pl_id FROM paragraphs_list WHERE end_bool = {1} ORDER BY pl_id""")
        c_new_from_p_id_list_raw = c.fetchall()
        c_new_from_p_id_list = id.raw_conv(c_new_from_p_id_list_raw)

        if c_new_from_p_id_list:
            global c_new_from_p_id_variable
            c_new_from_p_id_variable = StringVar()
            c_new_from_p_id_opt_menu_var = ttk.OptionMenu(c_new_info_frame_1, c_new_from_p_id_variable, c_new_from_p_id_list[0], *c_new_from_p_id_list)
            c_new_from_p_id_opt_menu_var.grid(row=1, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

            c_new_to_p_id_opt_menu()

        else:
            messagebox.showerror("Index Error", "No Existing 'From Paragraphs' Found")
            c_new_wd.destroy()

        conn.commit()

    def c_new_to_p_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list EXCEPT SELECT pl_id FROM paragraphs_list WHERE end_bool = {1} ORDER BY pl_id""")
        c_new_to_p_id_list_raw = c.fetchall()
        c_new_to_p_id_list = id.raw_conv(c_new_to_p_id_list_raw)

        global c_new_to_p_id_variable
        c_new_to_p_id_variable = StringVar()
        c_new_to_p_id_list.append('Assign No Paragraph')
        c_new_to_p_id_opt_menu_var = ttk.OptionMenu(c_new_info_frame_1, c_new_to_p_id_variable, c_new_to_p_id_list[-1], *c_new_to_p_id_list)
        c_new_to_p_id_opt_menu_var.grid(row=2, column=1, pady=c_new_pad, padx=c_new_pad, stick="ew")

        conn.commit()

    c_new_s_id_opt_menu()

    test_buttons_func.error_update()

    c_new_wd.mainloop()


def c_edt_edit():
    conn = sqlite3.connect(database, uri=True)
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


# Function to insert already written choice
def c_edt_insert():
    # Delete Previous Input
    c_edt_edit_c_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    c_id = c_edt_c_id_variable.get()

    c.execute(f"""SELECT c_text FROM choices WHERE c_id = '{c_id}'""")
    c_edt_text_raw = c.fetchall()
    c_edt_text = ((c_edt_text_raw[0])[0])

    # Input data into text box
    c_edt_edit_c_text_entry.insert(END, f'{c_edt_text}')

    conn.commit()


# Function to insert decoded id
def c_edt_decode_id():
    c_edt_decode_id_variable.delete("1.0", "end")
    c_edt_decode_id_variable.insert(END, id.decoder_3(c_edt_c_id_variable.get()))

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    c_edt_pl_id = c_edt_pl_id_variable.get()

    if c_edt_pl_id != 'Assign No Paragraph':
        c.execute(f"""SELECT p_text FROM paragraphs_list WHERE pl_id='{c_edt_pl_id}'""")
        c_edt_pl_text_raw = c.fetchall()
        c_edt_pl_text = id.raw_conv(c_edt_pl_text_raw)[0]
    else:
        c_edt_pl_text = ''

    conn.commit()

    c_edt_pl_text_variable.delete("1.0", "end")
    c_edt_pl_text_variable.insert(END, c_edt_pl_text)


def c_del_delete():
    conn = sqlite3.connect(database, uri=True)
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

    c_edt_s_id_opt_menu()
    c_edt_c_id_opt_menu()


def c_edt_assign_paragraph_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get pl_id and old c_id
    c_edt_c_id = c_edt_c_id_variable.get()
    # Avoid getting an error when choosing 'Assign no Paragraph' and pressing the button
    c_edt_pl_id = c_edt_pl_id_variable.get()
    if c_edt_pl_id == 'Assign No Paragraph':
        messagebox.showerror('Error', 'Action Not Possible', icon='warning')
    else:
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
                    else:
                        messagebox.showerror('Assignment Error', "Choice Can't Loop Back To Root Paragraph", icon='warning')
                else:
                    messagebox.showerror('Loop Error', f"Choice Number {c_edt_c_id_num} Already Has A 'To Paragraph' Assigned.", icon='warning')
            else:
                messagebox.showerror('Loop Error', f"Assigning Choice Number {c_edt_c_id_num} To Paragraph Number {c_edt_pl_id_from_num} Will Create A Loop.", icon='warning')
        else:
            messagebox.showerror('Priority Error', f"'To Paragraph' ID ({c_edt_c_id_p_from_num}) has to be Bigger than 'From Paragraph' ID ({c_edt_pl_id_from_num})", icon='warning')

        conn.commit()

        c_edt_c_id_opt_menu()


def c_del_assign_paragraph_delete():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get c_id to modify
    c_del_c_id_old = c_edt_c_id_variable.get()

    # Check that the selected id has a paragraph connected to it
    if c_del_c_id_old[-2] == 'P':
        warning = messagebox.askquestion('Confirm Deletion',
                                         f'Are you sure you want to Remove Paragraph Number '
                                         f'{id.id_int(id.decoder_2(c_del_c_id_old)[-1])} From '
                                         f'Choice Number {id.id_int(id.decoder_2(c_del_c_id_old)[-2])}?'
                                         f'\nIf That Paragraph Has No Other Choices Connected To It, It will be deleted '
                                         f"as well as all of it's information",
                                         icon='warning')
        if warning == 'yes':
            # Modify id
            c_del_c_id_new = id.p_del(c_del_c_id_old)

            # Update table
            c.execute("""UPDATE choices SET c_id = :c_id_new WHERE c_id = :c_id_old""",
                      {
                          "c_id_new": f"{c_del_c_id_new}",
                          "c_id_old": f'{c_del_c_id_old}'
                      })

            # Delete Paragraph If No Choices Are Connected to it
            c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE '%{id.decoder_2(c_del_c_id_old)[-1]}'""")
            c_del_c_id_list_raw = c.fetchall()
            c_del_c_id_list = id.raw_conv(c_del_c_id_list_raw)

            number = len(c_del_c_id_list)

            if number == 0:
                c.execute(f"""DELETE FROM paragraphs_list WHERE pl_id LIKE '%{id.decoder_2(c_del_c_id_old)[-1]}'""")
                c.execute(f"""DELETE FROM choices WHERE c_id LIKE'%{id.decoder_2(c_del_c_id_old)[-1]}%'""")
    else:
        messagebox.showerror('Error', f'Choice Number {id.id_int(c_del_c_id_old)} Has No Paragraphs Assigned to it.', icon='warning')

    conn.commit()

    c_edt_c_id_opt_menu()


def c_edt_assign_object_save():  # (Drop)
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get Object's Name
    c_edt_obj_name = c_edt_obj_name_variable.get()

    # Get c_id
    c_edt_c_id = c_edt_c_id_variable.get()

    if len(id.decoder_2(c_edt_c_id)) == 3:
        # Get c_id number
        c_ed_c_id_num = id.id_int(c_edt_c_id)
        c_ed_p_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-2])
    else:
        c_ed_c_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-2])
        c_ed_p_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-3])

    if c_edt_obj_name != 'Assign No Object':
        # Get Object's id
        c.execute(f"""SELECT obj_id FROM objects where obj_name ='{c_edt_obj_name}'""")
        c_edt_obj_id_raw = c.fetchall()
        c_edt_obj_id = id.raw_conv(c_edt_obj_id_raw)[0]

        c.execute(f"""UPDATE choices SET obj_id = '{c_edt_obj_id}' WHERE c_id = '{c_edt_c_id}'""")
        messagebox.showinfo("Success",
                            f"Choice Number {c_ed_c_id_num} In Paragraph Number {c_ed_p_id_num} Has Been Assigned Object '{c_edt_obj_name}' As A Drop.")

    else:
        c.execute(f"""UPDATE choices SET obj_id = 'None' WHERE c_id = '{c_edt_c_id}'""")
        messagebox.showinfo("Success",
                            f"Choice Number {c_ed_c_id_num}'s Drop In Paragraph Number {c_ed_p_id_num} Has Been Removed.")

    conn.commit()


def c_edt_assign_condition_save():  # (Condition)
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get Condition's Name
    c_edt_con_name = c_edt_con_name_variable.get()

    # Get c_id
    c_edt_c_id = c_edt_c_id_variable.get()

    if len(id.decoder_2(c_edt_c_id)) == 3:
        # Get c_id number
        c_ed_c_id_num = id.id_int(c_edt_c_id)
        c_ed_p_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-2])
    else:
        c_ed_c_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-2])
        c_ed_p_id_num = id.id_int(id.decoder_2(c_edt_c_id)[-3])

    if c_edt_con_name != 'Assign No Condition':
        # Get Object's id
        c.execute(f"""SELECT obj_id FROM objects where obj_name ='{c_edt_con_name}'""")
        c_edt_con_id_raw = c.fetchall()
        c_edt_con_id = id.raw_conv(c_edt_con_id_raw)[0]

        c.execute(f"""UPDATE choices SET con_id = '{c_edt_con_id}' WHERE c_id = '{c_edt_c_id}'""")
        messagebox.showinfo("Success", f"Choice Number {c_ed_c_id_num} In Paragraph Number {c_ed_p_id_num} Has Been Assigned Object '{c_edt_con_name}' As A Condition.")


    else:
        c.execute(f"""UPDATE choices SET con_id = 'None' WHERE c_id = '{c_edt_c_id}'""")
        messagebox.showinfo("Success", f"Choice Number {c_ed_c_id_num}'s Condition In Paragraph Number {c_ed_p_id_num} Has Been Removed.")


    conn.commit()


# Function to open edit window
def c_edt_window():
    style_func()
    global c_edt_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    c_edt_wd = Toplevel()
    c_edt_wd.title("Edit Choices")
    screen_x_2 = c_edt_wd.winfo_screenwidth()
    screen_y_2 = c_edt_wd.winfo_screenheight()
    window_x_2 = 1000
    window_y_2 = 653
    c_edt_wd.minsize(window_x_2, window_y_2)
    c_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    c_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    c_edt_frame_height = 400
    c_edt_info_frame_height = 57

    # Info Frame UP
    c_edt_info_frame_up = Frame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_up.pack(fill="both", side=TOP)


    # Select Info MAIN Frame
    c_edt_select_info_frame_0 = LabelFrame(c_edt_info_frame_up, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_info_frame_0.pack(fill="both", side=LEFT, expand=True)

    # Select Info Frame 1
    c_edt_select_info_frame_1 = Frame(c_edt_select_info_frame_0, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_info_frame_1.pack(fill="both", expand=True)

    # Select Info Frame 3
    c_edt_select_info_frame_2 = Frame(c_edt_select_info_frame_0, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_info_frame_2.pack(fill="y")


    # Assign OBJECT AND CONDITION MAIN FRAME
    c_edt_assign_object_frame = Frame(c_edt_info_frame_up, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_assign_object_frame.pack(fill="both", side=RIGHT)

    # Assign Object MAIN Frame
    c_edt_assign_object_frame_0 = LabelFrame(c_edt_assign_object_frame, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_assign_object_frame_0.pack(fill="both")

    # Assign Object Frame 1
    c_edt_assign_object_frame_1 = Frame(c_edt_assign_object_frame_0, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_assign_object_frame_1.pack(fill="y", side=TOP, expand=True)

    # Assign Object Frame 2
    c_edt_assign_object_frame_2 = Frame(c_edt_assign_object_frame_0, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_assign_object_frame_2.pack(fill="y", side=BOTTOM)

    # Select Condition MAIN Frame
    c_edt_select_condition_frame = LabelFrame(c_edt_assign_object_frame, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_condition_frame.pack(fill="both", expand=True)

    # Select Condition Frame 1
    c_edt_select_condition_frame_1 = Frame(c_edt_select_condition_frame, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_condition_frame_1.pack(fill="y")

    # Select Condition Frame 2
    c_edt_select_condition_frame_2 = Frame(c_edt_select_condition_frame, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_select_condition_frame_2.pack(fill="y", side=BOTTOM)


    # Info Frame DOWN
    c_edt_info_frame_down = Frame(c_edt_wd, height=c_edt_info_frame_height, width=window_x_2)
    c_edt_info_frame_down.pack(fill="both")


    # Edit Choice MAIN Frame
    c_edt_edit_choice_frame_0 = LabelFrame(c_edt_info_frame_down, height=c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_frame_0.pack(fill="both", side=RIGHT)

    # Edit Choice Text Frame
    c_edt_edit_choice_frame_1 = Frame(c_edt_edit_choice_frame_0, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_frame_1.pack(fill="both")

    # Edit Choice Buttons Frame
    c_edt_edit_choice_frame_2 = Frame(c_edt_edit_choice_frame_0, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_edit_choice_frame_2.pack(fill="both")


    # Assign Choice MAIN Frame
    c_edt_assign_choice_frame_0 = LabelFrame(c_edt_info_frame_down, height=c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_frame_0.pack(fill="both", side=LEFT, expand=True)

    # Assign Choice Select Frame
    c_edt_assign_choice_frame_1 = Frame(c_edt_assign_choice_frame_0, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_frame_1.pack(fill="both")

    # Assign Choice Buttons Frame
    c_edt_assign_choice_frame_2 = Frame(c_edt_assign_choice_frame_0, height=window_y_2 - c_edt_frame_height, width=window_x_2)
    c_edt_assign_choice_frame_2.pack(fill="both")

    c_edt_entry_width = 37
    c_edt_width = 42
    c_edt_option_width = 37
    c_edt_pad = 10

    # Labels
    c_edt_story_id_label = ttk.Label(c_edt_select_info_frame_1, text="Select Story ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_story_id_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_choice_id_label = ttk.Label(c_edt_select_info_frame_1, text="Select Choice ID:", width=int(c_edt_width / 2), anchor=W)
    c_edt_choice_id_label.grid(row=1, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_decode_id_label = ttk.Label(c_edt_select_info_frame_1, text="Decoded Choice ID:", width=int(c_edt_width / 2), anchor=NW)
    c_edt_decode_id_label.grid(row=2, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    #

    c_edt_object_id_label = ttk.Label(c_edt_assign_object_frame_1, text="Select Object Drop:", width=int(c_edt_width / 2), anchor=W)
    c_edt_object_id_label.grid(row=0, column=0, padx=c_edt_pad-3, pady=c_edt_pad, stick="w")

    #

    p_edt_obj_name_label = ttk.Label(c_edt_select_condition_frame_1, text="Select Condition:", width=int(c_edt_width / 2), anchor=W)
    p_edt_obj_name_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    #

    c_edt_edit_c_text_label = ttk.Label(c_edt_edit_choice_frame_1, text="Edit Choice:", width=int(c_edt_width / 2) - 1, anchor=NW)
    c_edt_edit_c_text_label.grid(row=0, column=0, padx=(c_edt_pad+4, c_edt_pad), pady=c_edt_pad, stick="nw")

    #

    c_edt_to_p_id_label = ttk.Label(c_edt_assign_choice_frame_1, text="Select 'To Paragraph' id:",
                                width=int(c_edt_width / 2), anchor=W)
    c_edt_to_p_id_label.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_edit_c_text_label = ttk.Label(c_edt_assign_choice_frame_1, text="'To Paragraph' Text:", width=int(c_edt_width / 2) - 1, anchor=NW)
    c_edt_edit_c_text_label.grid(row=1, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="nw")

    global c_edt_decode_id_variable, c_edt_edit_c_text_entry, c_edt_pl_text_variable

    # Message
    c_edt_decode_id_variable = Text(c_edt_select_info_frame_1, width=c_edt_entry_width, height=5)
    c_edt_decode_id_variable.bind("<Key>", lambda a: "break")
    c_edt_decode_id_variable.grid(row=2, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    c_edt_pl_text_variable = Text(c_edt_assign_choice_frame_1, width=c_edt_entry_width, height=18)
    c_edt_pl_text_variable.bind("<Key>", lambda a: "break")
    c_edt_pl_text_variable.grid(row=1, column=1, padx=c_edt_pad, pady=c_edt_pad, stick="w")

    # Text Entry
    c_edt_edit_c_text_entry = Text(c_edt_edit_choice_frame_1, width=c_edt_entry_width, height=20)
    c_edt_edit_c_text_entry.grid(row=0, column=1, padx=(0, c_edt_pad), pady=(c_edt_pad+2, c_edt_pad), stick="w")

    # Buttons Edit Choice
    p_edt_width_buttons = 13
    p_edt_save_choice_button = ttk.Button(c_edt_edit_choice_frame_2, text="Save Changes", width=p_edt_width_buttons,
                                     command=c_edt_edit)
    p_edt_save_choice_button.grid(row=0, column=0, padx=(c_edt_pad + 1, c_edt_pad), pady=(c_edt_pad+11, c_edt_pad), stick="w")

    p_edt_load_choice_button = ttk.Button(c_edt_edit_choice_frame_2, text="Load Choice", width=p_edt_width_buttons,
                                    command=c_edt_insert)
    p_edt_load_choice_button.grid(row=0, column=1, padx=(c_edt_pad + 1, c_edt_pad), pady=(c_edt_pad+11, c_edt_pad), stick="w")

    p_edt_delete_choice_button = ttk.Button(c_edt_edit_choice_frame_2, text="Delete Choice", width=p_edt_width_buttons,
                                      command=c_del_delete)
    p_edt_delete_choice_button.grid(row=0, column=2, padx=c_edt_pad, pady=(c_edt_pad+11, c_edt_pad), stick="w")

    p_edt_cancel_button = ttk.Button(c_edt_edit_choice_frame_2, text="Cancel", width=p_edt_width_buttons,
                                 command=c_edt_wd.destroy)
    p_edt_cancel_button.grid(row=0, column=3, padx=(c_edt_pad, c_edt_pad + 1), pady=(c_edt_pad+11, c_edt_pad), stick="w")

    # Buttons Assign Choice
    p_edt_width_buttons_2 = 30
    p_edt_save_p_to_c_button = ttk.Button(c_edt_assign_choice_frame_2, text="Assign Choice To Paragraph ", width=p_edt_width_buttons_2, command=c_edt_assign_paragraph_save)
    p_edt_save_p_to_c_button.pack(padx=(c_edt_pad+10, c_edt_pad), pady=c_edt_pad, side=LEFT)

    p_edt_delete_p_from_c_button = ttk.Button(c_edt_assign_choice_frame_2, text="Delete Paragraph From Choice", width=p_edt_width_buttons_2, command=c_del_assign_paragraph_delete)
    p_edt_delete_p_from_c_button.pack(padx=c_edt_pad, pady=c_edt_pad, side=LEFT)

    # Buttons Assign Object
    p_edt_width_buttons_3 = 31
    p_edt_save_p_to_c_button = ttk.Button(c_edt_assign_object_frame_2, text="Submit Object Changes", width=p_edt_width_buttons_3, command=c_edt_assign_object_save)
    p_edt_save_p_to_c_button.grid(row=0, column=0, padx=c_edt_pad, pady=(c_edt_pad+25, c_edt_pad), stick="w", ipadx=120)

    # Buttons Assign Condition
    p_edt_submit_object_button = ttk.Button(c_edt_select_condition_frame_2, text="Submit Condition Changes", width=p_edt_width_buttons_3, command=c_edt_assign_condition_save)
    p_edt_submit_object_button.grid(row=0, column=0, padx=c_edt_pad, pady=c_edt_pad, stick="w", ipadx=120)

    # Button Submit
    c_edt_submit_id_button = ttk.Button(c_edt_select_info_frame_2, text="Submit Information", width=p_edt_width_buttons_3, command=c_edt_decode_id)
    c_edt_submit_id_button.grid(row=0, column=0, padx=(c_edt_pad, c_edt_pad+2), pady=c_edt_pad, stick="w", ipadx=128)

    global c_edt_s_id_opt_menu, c_edt_c_id_opt_menu

    def c_edt_s_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices ORDER BY s_id""")
        c_edt_s_id_list_raw = c.fetchall()
        c_edt_s_id_list = id.raw_conv(c_edt_s_id_list_raw)

        if c_edt_s_id_list:
            global c_edt_s_id_variable
            c_edt_s_id_variable = StringVar()
            c_edt_s_id_opt_menu_var = ttk.OptionMenu(c_edt_select_info_frame_1, c_edt_s_id_variable, c_edt_s_id_list[0], *c_edt_s_id_list)
            c_edt_s_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

            c_edt_c_id_opt_menu()

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            c_edt_wd.destroy()

        conn.commit()

    def c_edt_c_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices""")
        c_edt_c_id_list_raw = c.fetchall()
        c_edt_c_id_list = id.raw_conv(c_edt_c_id_list_raw)

        if c_edt_c_id_list:
            global c_edt_c_id_variable
            c_edt_c_id_variable = StringVar()
            c_edt_c_id_opt_menu_var = ttk.OptionMenu(c_edt_select_info_frame_1, c_edt_c_id_variable, c_edt_c_id_list[0], *c_edt_c_id_list)
            c_edt_c_id_opt_menu_var.grid(row=1, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

            c_edt_pl_id_opt_menu()

        else:
            messagebox.showerror("Index Error", "No Existing Choices Found")
            c_edt_wd.destroy()

        conn.commit()

    def c_edt_pl_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list ORDER BY pl_id""")
        c_edt_pl_id_list_raw = c.fetchall()
        c_edt_pl_id_list = id.raw_conv(c_edt_pl_id_list_raw)

        global c_edt_pl_id_variable
        c_edt_pl_id_variable = StringVar()

        if c_edt_pl_id_list:
            default = c_edt_pl_id_list[0]
        else:
            c_edt_pl_id_list.append('Assign No Paragraph')
            default = c_edt_pl_id_list[0]

        c_edt_pl_id_opt_menu_var = ttk.OptionMenu(c_edt_assign_choice_frame_1, c_edt_pl_id_variable, default, *c_edt_pl_id_list)
        c_edt_pl_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        conn.commit()

    def c_edt_obj_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT obj_name FROM objects""")
        c_edt_obj_name_list_raw = c.fetchall()
        c_edt_obj_name_list = id.raw_conv(c_edt_obj_name_list_raw)

        global c_edt_obj_name_variable
        c_edt_obj_name_variable = StringVar()
        c_edt_obj_name_list.append('Assign No Object')
        c_edt_obj_id_opt_menu_var = ttk.OptionMenu(c_edt_assign_object_frame_1, c_edt_obj_name_variable, c_edt_obj_name_list[-1], *c_edt_obj_name_list)
        c_edt_obj_id_opt_menu_var.config(width=c_edt_option_width)
        c_edt_obj_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        conn.commit()

    def c_edt_con_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT obj_id FROM choices""")
        c_edt_obj_id_list_raw = c.fetchall()
        c_edt_obj_id_list_raw_2 = id.raw_conv(c_edt_obj_id_list_raw)

        c_edt_obj_id_list = []
        for obj_id in c_edt_obj_id_list_raw_2:
            if obj_id != 'None':
                c_edt_obj_id_list.append(obj_id)

        c_edt_con_name_list = []
        for obj_id in c_edt_obj_id_list:
            c.execute(f"""SELECT obj_name FROM objects WHERE obj_id = '{obj_id}'""")
            c_edt_con_name_raw = c.fetchall()
            c_edt_con_name = id.raw_conv(c_edt_con_name_raw)[0]
            c_edt_con_name_list.append(c_edt_con_name)

        global c_edt_con_name_variable
        c_edt_con_name_variable = StringVar()
        c_edt_con_name_list.append('Assign No Condition')
        c_edt_con_id_opt_menu_var = ttk.OptionMenu(c_edt_select_condition_frame_1, c_edt_con_name_variable, c_edt_con_name_list[-1], *c_edt_con_name_list)
        c_edt_con_id_opt_menu_var.config(width=c_edt_option_width)
        c_edt_con_id_opt_menu_var.grid(row=0, column=1, pady=c_edt_pad, padx=c_edt_pad, stick="ew")

        conn.commit()

    c_edt_obj_id_opt_menu()
    c_edt_con_id_opt_menu()
    c_edt_s_id_opt_menu()

    test_buttons_func.error_update()

    c_edt_wd.mainloop()
