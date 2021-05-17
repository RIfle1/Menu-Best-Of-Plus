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


def p_new_save():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs
    (s_id text,
    p_id text)""")

    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs_list
        (s_id text,
        pl_id text,
        p_text text,
        npc_id text,
        mst_id text)""")

    # Get all needed id's
    p_new_s_id = p_new_s_id_variable.get()
    p_new_c_id = p_new_p_id_variable.get()

    # Get entry text length for error checking
    p_new_text_length = len(p_new_paragraph_text_entry.get("1.0", "end"))

    c.execute("""SELECT pl_id FROM paragraphs_list ORDER BY pl_id""")
    p_new_p_id_list_raw = c.fetchall()
    p_new_p_id = id.raw_conv(p_new_p_id_list_raw)
    p_new_p_id_num_max = id.max_num(id.int_list(p_new_p_id))

    if p_new_p_id_num_max == '':
        p_new_new_p_id = 0
    else:
        p_new_new_p_id = p_new_p_id_num_max + 1
    
    p_new_c_p_id = id.decoder_2(p_new_c_id)[0]

    if f'{p_new_s_id}' == f'{p_new_c_p_id}':
        if p_new_text_length != 1:
            c.execute("INSERT INTO paragraphs_list VALUES (:s_id, :lp_id, :p_text)",
                      {
                          "s_id": f"{p_new_s_id}",
                          "lp_id": f"{p_new_s_id}_{id.conv('p_id', p_new_new_p_id)}",
                          "p_text": str(p_new_paragraph_text_entry.get("1.0", "end"))
                      })

            messagebox.showinfo("Success", f"Paragraph Number {p_new_new_p_id}\nIn Story Number {id.id_int(p_new_s_id)}\nhas been successfully created.")
        else:
            messagebox.showerror("Input Error", "Paragraph Text Is Empty")
    else:
        messagebox.showerror("ID Error", f"Choice's Story ID is {p_new_c_p_id} but Story ID is {p_new_s_id}")

    conn.commit()
    conn.close()

    # Clear the Text Boxes
    p_new_paragraph_text_entry.delete("1.0", "end")

    p_new_s_id_opt_menu()
    p_new_c_id_opt_menu()


def p_new_insert():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    p_new_c_id = p_new_p_id_variable.get()

    c.execute(f"""SELECT c_text FROM choices WHERE c_id='{p_new_c_id}'""")
    p_new_text_raw = c.fetchall()
    p_new_text = ((p_new_text_raw[0])[0])

    # Input data into text box
    p_new_choice_message_var.delete("1.0", "end")
    p_new_choice_message_var.insert(END, str(p_new_text))

    # Decode the ID
    p_new_decoded_id_variable.delete("1.0", "end")
    p_new_decoded_id_variable.insert(END, id.decoder_3(p_new_p_id_variable.get()))

    # End Connection
    conn.commit()
    conn.close()


def p_new_window():
    global p_new_wd
    # Create New Window
    p_new_wd = Toplevel()
    p_new_wd.title("Create A New Paragraph")
    screen_x_2 = p_new_wd.winfo_screenwidth()
    screen_y_2 = p_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 848
    p_new_wd.minsize(window_x_2, window_y_2)
    p_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    p_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    p_new_frame_height = 200
    p_new_rest = window_y_2 - p_new_frame_height*2
    # Info Frame 1
    p_new_info_frame_1 = LabelFrame(p_new_wd, width=window_x_2, height=p_new_frame_height)
    p_new_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    p_new_info_frame_2 = LabelFrame(p_new_wd, width=window_x_2, height=p_new_frame_height)
    p_new_info_frame_2.pack(fill="both", side=TOP)

    # Top Button Frame
    p_new_button_frame_1 = LabelFrame(p_new_wd, height=p_new_rest / 2, width=window_x_2)
    p_new_button_frame_1.pack(fill="both")

    # Choice Frame
    p_new_paragraph_frame = LabelFrame(p_new_wd, width=window_x_2, height=p_new_frame_height)
    p_new_paragraph_frame.pack(fill="both")

    # Bottom Buttons Frame
    p_new_button_frame_2 = LabelFrame(p_new_wd, height=p_new_rest / 2, width=window_x_2)
    p_new_button_frame_2.pack(fill="both", expand=True)

    p_new_width = 42
    p_new_pad = 10
    p_new_entry_width = 37
    # Labels
    p_new_get_story_id_label = Label(p_new_info_frame_1, text="Select Story ID:", width=int(p_new_width / 2), anchor=W)
    p_new_get_story_id_label.grid(row=0, column=0, padx=(p_new_pad, p_new_pad+1), pady=p_new_pad, stick="w")

    p_new_get_choice_id_label = Label(p_new_info_frame_1, text="Select Choice ID:", width=int(p_new_width / 2), anchor=W)
    p_new_get_choice_id_label.grid(row=1, column=0, padx=(p_new_pad, p_new_pad+1), pady=p_new_pad, stick="w")

    p_new_decode_c_id_label = Label(p_new_info_frame_1, text="Decoded ID:", width=int(p_new_width / 2), anchor=NW)
    p_new_decode_c_id_label.grid(row=2, column=0, padx=(p_new_pad, p_new_pad+5), pady=p_new_pad, stick="nw")

    p_new_choice_message_label = Label(p_new_info_frame_2, text="Choice Text:", width=int(p_new_width / 2), anchor=NW)
    p_new_choice_message_label.grid(row=2, column=0, padx=(p_new_pad, p_new_pad+5), pady=p_new_pad, stick="nw")

    p_new_paragraph_text_label = Label(p_new_paragraph_frame, text="Paragraph Text:", width=int(p_new_width / 2), anchor=NW)
    p_new_paragraph_text_label.grid(row=1, column=0, padx=(p_new_pad, p_new_pad+5), pady=p_new_pad, stick="nw")

    global p_new_paragraph_text_entry, p_new_choice_message_var, p_new_decoded_id_variable
    # Entries
    p_new_paragraph_text_entry = Text(p_new_paragraph_frame, width=37, height=20)
    p_new_paragraph_text_entry.grid(row=1, column=1, padx=p_new_pad, pady=p_new_pad)

    # Message Box
    p_new_choice_message_var = Text(p_new_info_frame_2, width=p_new_entry_width, height=10)
    p_new_choice_message_var.bind("<Key>", lambda a: "break")
    p_new_choice_message_var.grid(row=2, column=1, padx=p_new_pad, pady=p_new_pad, stick="w")

    p_new_decoded_id_variable = Text(p_new_info_frame_1, width=p_new_entry_width, height=5)
    p_new_decoded_id_variable.bind("<Key>", lambda a: "break")
    p_new_decoded_id_variable.grid(row=2, column=1, padx=p_new_pad, pady=p_new_pad, stick="w")

    # Buttons
    p_new_submit_button = Button(p_new_button_frame_1, text="Submit", width=int(p_new_width / 2), command=p_new_insert)
    p_new_submit_button.grid(row=0, column=0, padx=p_new_pad, pady=p_new_pad, ipadx=160)

    p_new_save_choice_button = Button(p_new_button_frame_2, text="Save Paragraph", width=int(p_new_width / 2), command=p_new_save)
    p_new_save_choice_button.grid(row=2, column=0, padx=p_new_pad, pady=p_new_pad, stick="w")

    p_new_cancel_button = Button(p_new_button_frame_2, text="Cancel", width=p_new_width, command=p_new_wd.destroy)
    p_new_cancel_button.grid(row=2, column=1, padx=p_new_pad, pady=p_new_pad, stick="w")

    global p_new_s_id_opt_menu, p_new_c_id_opt_menu

    def p_new_s_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices""")
        p_new_s_id_list_raw = c.fetchall()

        p_new_s_id_list = []
        for tp in p_new_s_id_list_raw:
            for item in tp:
                p_new_s_id_list.append(item)

        if p_new_s_id_list:
            global p_new_s_id_variable
            p_new_s_id_variable = StringVar()
            p_new_s_id_variable.set(p_new_s_id_list[0])
            p_new_s_id_opt_menu_var = OptionMenu(p_new_info_frame_1, p_new_s_id_variable, *p_new_s_id_list)
            p_new_s_id_opt_menu_var.config(width=p_new_width+1)
            p_new_s_id_opt_menu_var.grid(row=0, column=1, pady=p_new_pad, padx=p_new_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            p_new_wd.destroy()

        conn.commit()
        conn.close()

    p_new_s_id_opt_menu()

    def p_new_c_id_opt_menu():
        # Options Menu For all existing paragraphs
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices ORDER BY c_id""")
        p_new_c_id_ist_raw = c.fetchall()
        p_new_c_id_list = id.c_id_sorter(id.raw_conv(p_new_c_id_ist_raw))

        if p_new_c_id_list:
            global p_new_p_id_variable
            p_new_p_id_variable = StringVar()
            p_new_p_id_variable.set(p_new_c_id_list[0])
            p_new_c_id_opt_menu_var = OptionMenu(p_new_info_frame_1, p_new_p_id_variable, *p_new_c_id_list)
            p_new_c_id_opt_menu_var.config(width=p_new_width+1)
            p_new_c_id_opt_menu_var.grid(row=1, column=1, pady=p_new_pad, padx=p_new_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Choices were Found")
            p_new_wd.destroy()

        conn.commit()
        conn.close()

    p_new_c_id_opt_menu()

    p_new_wd.mainloop()


def p_edt_edit():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    p_edt_s_id = p_edt_s_id_variable.get()
    p_edt_p_id = p_edt_p_id_variable.get()
    if len(p_edt_paragraph_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE paragraphs_list SET p_text = :p_text WHERE pl_id = :pl_id""",
                  {
                      "p_text": p_edt_paragraph_text_entry.get("1.0", "end"),
                      "pl_id": f'{p_edt_p_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Paragraph Number {id.id_int(p_edt_p_id)} in Story Number {id.id_int(p_edt_s_id)} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Paragraph Text is Empty', icon='warning')

    # Clear the Text Boxes
    p_edt_paragraph_text_entry.delete("1.0", "end")

    conn.commit()
    conn.close()

    p_edt_s_id_opt_menu()
    p_edt_p_id_opt_menu()


def p_edt_insert():
    p_edt_paragraph_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database)
    c = conn.cursor()

    p_edt_p_id = p_edt_p_id_variable.get()

    c.execute(f"""SELECT p_text FROM paragraphs_list WHERE pl_id = '{p_edt_p_id}'""")
    p_edt_text_raw = c.fetchall()
    p_edt_text = ((p_edt_text_raw[0])[0])

    p_edt_paragraph_text_entry.insert(END, f'{p_edt_text}')

    conn.commit()
    conn.close()


def p_edt_decode_id():
    p_edt_decode_id_variable.delete("1.0", "end")
    p_edt_decode_id_variable.insert(END, id.decoder_3(p_edt_p_id_variable.get()))


def p_del_delete():
    conn = sqlite3.connect(database)
    c = conn.cursor()
    p_del_s_id = p_edt_s_id_variable.get()
    p_del_p_id = p_edt_p_id_variable.get()

    p_del_warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete Paragraph Number {id.id_int(p_del_p_id)}?', icon='warning')

    if p_del_warning == 'yes':
        c.execute(f"""DELETE FROM paragraphs_list WHERE pl_id LIKE '{p_del_p_id}%'""")
        c.execute(f"""DELETE FROM choices WHERE c_id LIKE '{p_del_p_id}%'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"Paragraph Number {id.id_int(p_del_p_id)} In Story Number {id.id_int(p_del_s_id)}\nhas been successfully deleted."
                                       f"\nAll Paragraphs and Choices connected to Paragraph Number {id.id_int(p_del_p_id)} were also Deleted.")
        p_edt_paragraph_text_entry.delete("1.0", "end")
        p_edt_decode_id_variable.delete("1.0", "end")

    conn.commit()
    conn.close()

    p_edt_p_id_opt_menu()
    p_edt_s_id_opt_menu()


def p_edt_window():
    global p_edt_wd
    p_edt_wd = Toplevel()
    p_edt_wd.title("Edit Paragraphs")
    screen_x_2 = p_edt_wd.winfo_screenwidth()
    screen_y_2 = p_edt_wd.winfo_screenheight()
    window_x_2 = 500
    window_y_2 = 663
    p_edt_wd.minsize(window_x_2, window_y_2)
    p_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    p_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    p_edt_frame_height = 400
    p_edt_info_frame_height = 57

    # Info Frame 1
    p_edt_info_frame_1 = LabelFrame(p_edt_wd, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 2
    p_edt_info_frame_2 = LabelFrame(p_edt_wd, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_info_frame_2.pack(fill="both", side=TOP)

    # Info Frame 3
    p_edt_info_frame_3 = LabelFrame(p_edt_wd, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_info_frame_3.pack(fill="both", side=TOP)

    # Info Frame 4
    p_edt_info_frame_4 = LabelFrame(p_edt_wd, height=p_edt_frame_height, width=window_x_2)
    p_edt_info_frame_4.pack(fill="both", side=TOP)

    # Buttons Frame
    p_edt_button_frame = LabelFrame(p_edt_wd, height=window_y_2 - p_edt_frame_height, width=window_x_2)
    p_edt_button_frame.pack(fill="both", side=BOTTOM, expand=True)

    p_edt_entry_width = 37
    p_edt_width = 42
    p_edt_pad = 10

    # Labels
    p_edt_story_id_label = Label(p_edt_info_frame_1, text="Select Choice ID:", width=int(p_edt_width / 2), anchor=W)
    p_edt_story_id_label.grid(row=0, column=0, padx=(p_edt_pad, p_edt_pad-6), pady=p_edt_pad, stick="w")

    p_edt_decode_id_label_text = Label(p_edt_info_frame_2, text="Decoded ID:", width=int(p_edt_width / 2), anchor=NW)
    p_edt_decode_id_label_text.grid(row=0, column=0, padx=(p_edt_pad, p_edt_pad-5), pady=p_edt_pad, stick="nw")

    p_edt_paragraph_text_label = Label(p_edt_info_frame_4, text="Edit Paragraph:", width=int(p_edt_width / 2) - 1, anchor=NW)
    p_edt_paragraph_text_label.grid(row=0, column=0, padx=p_edt_pad, pady=p_edt_pad, stick="nw")

    # Message Box
    global p_edt_decode_id_variable
    p_edt_decode_id_variable = Text(p_edt_info_frame_2, width=p_edt_entry_width, height=5)
    p_edt_decode_id_variable.bind("<Key>", lambda a: "break")
    p_edt_decode_id_variable.grid(row=0, column=1, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    # Text
    global p_edt_paragraph_text_entry
    p_edt_paragraph_text_entry = Text(p_edt_info_frame_4, width=p_edt_entry_width, height=20)
    p_edt_paragraph_text_entry.grid(row=0, column=1, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    # Buttons
    p_edt_submit_id_button = Button(p_edt_info_frame_3, text="Decode ID", width=int(p_edt_width / 2), command=p_edt_decode_id)
    p_edt_submit_id_button.grid(row=0, column=0, padx=p_edt_pad, pady=p_edt_pad, stick="w", ipadx=157)

    p_edt_width_buttons = 13
    p_edt_save_story_button = Button(p_edt_button_frame, text="Save Changes", width=p_edt_width_buttons,
                                     command=p_edt_edit)
    p_edt_save_story_button.grid(row=0, column=0, padx=(p_edt_pad + 3, p_edt_pad), pady=p_edt_pad, stick="w")

    p_edt_load_text_button = Button(p_edt_button_frame, text="Load Paragraph", width=p_edt_width_buttons,
                                    command=p_edt_insert)
    p_edt_load_text_button.grid(row=0, column=1, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    p_edt_delete_text_button = Button(p_edt_button_frame, text="Delete Paragraph", width=p_edt_width_buttons,
                                      command=p_del_delete)
    p_edt_delete_text_button.grid(row=0, column=2, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    p_edt_cancel_button = Button(p_edt_button_frame, text="Cancel", width=p_edt_width_buttons,
                                 command=p_edt_wd.destroy)
    p_edt_cancel_button.grid(row=0, column=3, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    global p_edt_s_id_opt_menu, p_edt_p_id_opt_menu

    def p_edt_s_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM paragraphs_list""")
        p_edt_s_id_list_raw = c.fetchall()
        p_edt_s_id_list = []

        for tp in p_edt_s_id_list_raw:
            for item in tp:
                p_edt_s_id_list.append(item)

        if p_edt_s_id_list:
            global p_edt_s_id_variable
            p_edt_s_id_variable = StringVar()
            p_edt_s_id_variable.set(p_edt_s_id_list[0])
            p_edt_s_id_opt_menu_var = OptionMenu(p_edt_info_frame_1, p_edt_s_id_variable, *p_edt_s_id_list)
            p_edt_s_id_opt_menu_var.config(width=p_edt_width+1)
            p_edt_s_id_opt_menu_var.grid(row=0, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            p_edt_wd.destroy()

        conn.commit()
        conn.close()

    def p_edt_p_id_opt_menu():
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list""")
        p_edt_p_id_list_raw = c.fetchall()
        p_edt_p_id_list = []

        for tp in p_edt_p_id_list_raw:
            for item in tp:
                p_edt_p_id_list.append(item)

        if p_edt_p_id_list:
            global p_edt_p_id_variable
            p_edt_p_id_variable = StringVar()
            p_edt_p_id_variable.set(p_edt_p_id_list[0])
            p_edt_p_id_opt_menu_var = OptionMenu(p_edt_info_frame_1, p_edt_p_id_variable, *p_edt_p_id_list)
            p_edt_p_id_opt_menu_var.config(width=p_edt_width+1)
            p_edt_p_id_opt_menu_var.grid(row=1, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Paragraphs Found")
            p_edt_wd.destroy()

        conn.commit()
        conn.close()

    p_edt_s_id_opt_menu()
    p_edt_p_id_opt_menu()

    p_edt_wd.mainloop()
