# Imports
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import editor_settings
import test_buttons_func
import id
import os


def style_func():
    p_font_size = 11
    p_style = ttk.Style()
    p_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', p_font_size))
    p_style.configure("TButton", font=('Times New Roman', p_font_size))
    p_style.configure("TLabel", font=('Times New Roman', p_font_size))


def p_new_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Create Id's and stuff in paragraphs list table

    c.execute("""CREATE TABLE IF NOT EXISTS paragraphs_list
        (s_id text,
        pl_id text,
        p_text text,
        npc_id text,
        mst_id text,
        npc_bool integer,
        mst_bool integer,
        end_bool integer)""")

    # Get all needed id's
    p_new_s_id = p_new_s_id_variable.get()
    p_new_c_id = p_new_p_id_variable.get()

    # Get entry text length for error checking
    p_new_text_length = len(p_new_paragraph_text_entry.get("1.0", "end"))

    # Script to create a new paragraph number and to replace a number if a paragraph has been deleted
    c.execute(f"""SELECT pl_id FROM paragraphs_list WHERE s_id='{p_new_s_id}' ORDER BY pl_id""")
    p_new_p_id_list_raw = c.fetchall()
    p_new_p_id_list = id.raw_conv(p_new_p_id_list_raw)

    if p_new_p_id_list:
        p_id_number_list = []
        for p_id in p_new_p_id_list:
            p_id_number_list.append(int(id.id_int(p_id)))

        p_new_p_id_num_max = int(id.max_num(p_id_number_list))

        p_id_number_real_list = []
        for number in range(1, p_new_p_id_num_max+1):
            p_id_number_real_list.append(number)

        p_id_missing_numbers_list = []
        for number in p_id_number_real_list:
            if number not in p_id_number_list:
                p_id_missing_numbers_list.append(number)

        if p_id_missing_numbers_list:
            p_new_new_p_id = p_id_missing_numbers_list[0]
        else:
            p_new_new_p_id = int(p_new_p_id_num_max) + 1
    else:
        p_new_new_p_id = 1

    # ----------------------------------------

    p_new_c_p_id = id.decoder_2(p_new_c_id)[0]

    if f'{p_new_s_id}' == f'{p_new_c_p_id}':
        if p_new_text_length != 1:
            c.execute(
                "INSERT INTO paragraphs_list VALUES (:s_id, :lp_id, :p_text, :npc_id, :mst_id, :npc_bool, :mst_bool, :end_bool)",
                {
                    "s_id": f"{p_new_s_id}",
                    "lp_id": f"{p_new_s_id}_{id.conv('p_id', p_new_new_p_id)}",
                    "p_text": str(p_new_paragraph_text_entry.get("1.0", "end")),
                    "npc_id": 'None',
                    "mst_id": 'None',
                    "npc_bool": 0,
                    "mst_bool": 0,
                    "end_bool": 0
                })

            # Assign Paragraph to choice
            c.execute("""UPDATE choices SET c_id = :c_id_new WHERE c_id = :c_id_old""",
                      {
                          "c_id_new": f"{p_new_c_id}_{id.conv('p_id', p_new_new_p_id)}",
                          "c_id_old": f'{p_new_c_id}'
                      })

            messagebox.showinfo("Success",
                                f"Paragraph Number {p_new_new_p_id}\nIn Story Number {id.id_int(p_new_s_id)}\nhas been successfully created.")
        else:
            messagebox.showerror("Input Error", "Paragraph Text Is Empty")
    else:
        messagebox.showerror("ID Error", f"Choice's Story ID is {p_new_c_p_id} but Story ID is {p_new_s_id}")

    # Clear the Text Boxes
    p_new_paragraph_text_entry.delete("1.0", "end")

    conn.commit()

    p_new_s_id_opt_menu()
    p_new_c_id_opt_menu()


def p_new_insert():
    conn = sqlite3.connect(database, uri=True)
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


def p_new_window():
    style_func()
    global p_new_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    p_new_wd = Toplevel()
    path = os.path.dirname(__file__)
    p_new_wd.iconbitmap(f'{path}/Illustrations/Icon/editor_icon_2.ico')
    p_new_wd.grab_set()
    p_new_wd.title("Create A New Paragraph")
    screen_x_2 = p_new_wd.winfo_screenwidth()
    screen_y_2 = p_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 836
    p_new_wd.minsize(window_x_2, window_y_2)
    p_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    p_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    p_new_frame_height = 200
    p_new_rest = window_y_2 - p_new_frame_height * 2
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
    p_new_button_frame_2.pack(fill="both")

    p_new_width = 42
    p_new_pad = 10
    p_new_entry_width = 37
    # Labels
    p_new_get_story_id_label = ttk.Label(p_new_info_frame_1, text="Select Story ID:", width=int(p_new_width / 2), anchor=W)
    p_new_get_story_id_label.grid(row=0, column=0, padx=(p_new_pad, p_new_pad + 1), pady=p_new_pad, stick="w")

    p_new_get_choice_id_label = ttk.Label(p_new_info_frame_1, text="Select Choice ID:", width=int(p_new_width / 2),
                                      anchor=W)
    p_new_get_choice_id_label.grid(row=1, column=0, padx=(p_new_pad, p_new_pad + 1), pady=p_new_pad, stick="w")

    p_new_decode_c_id_label = ttk.Label(p_new_info_frame_1, text="Decoded ID:", width=int(p_new_width / 2), anchor=NW)
    p_new_decode_c_id_label.grid(row=2, column=0, padx=(p_new_pad, p_new_pad + 5), pady=p_new_pad, stick="nw")

    p_new_choice_message_label = ttk.Label(p_new_info_frame_2, text="Choice Text:", width=int(p_new_width / 2), anchor=NW)
    p_new_choice_message_label.grid(row=2, column=0, padx=(p_new_pad, p_new_pad + 5), pady=p_new_pad, stick="nw")

    p_new_paragraph_text_label = ttk.Label(p_new_paragraph_frame, text="Paragraph Text:", width=int(p_new_width / 2),
                                       anchor=NW)
    p_new_paragraph_text_label.grid(row=1, column=0, padx=(p_new_pad, p_new_pad + 5), pady=p_new_pad, stick="nw")

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
    p_new_submit_button = ttk.Button(p_new_button_frame_1, text="Submit", width=int(p_new_width / 2), command=p_new_insert)
    p_new_submit_button.grid(row=0, column=0, padx=p_new_pad, pady=p_new_pad, ipadx=160)

    p_new_save_choice_button = ttk.Button(p_new_button_frame_2, text="Save Paragraph", width=int(p_new_width / 2),
                                      command=p_new_save)
    p_new_save_choice_button.grid(row=2, column=0, padx=p_new_pad, pady=p_new_pad, stick="w")

    p_new_cancel_button = ttk.Button(p_new_button_frame_2, text="Cancel", width=p_new_width, command=p_new_wd.destroy)
    p_new_cancel_button.grid(row=2, column=1, padx=p_new_pad, pady=p_new_pad, stick="w")

    global p_new_s_id_opt_menu, p_new_c_id_opt_menu

    def p_new_s_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM choices UNION SELECT s_id FROM choices ORDER BY s_id""")
        p_new_s_id_list_raw = c.fetchall()

        p_new_s_id_list = []
        for tp in p_new_s_id_list_raw:
            for item in tp:
                p_new_s_id_list.append(item)

        if p_new_s_id_list:
            global p_new_s_id_variable
            p_new_s_id_variable = StringVar()
            p_new_s_id_opt_menu_var = ttk.OptionMenu(p_new_info_frame_1, p_new_s_id_variable, p_new_s_id_list[0], *p_new_s_id_list)
            p_new_s_id_opt_menu_var.grid(row=0, column=1, pady=p_new_pad, padx=p_new_pad, stick="ew")

        else:
            p_new_wd.destroy()
            messagebox.showerror("Index Error", "No Existing Stories Found")

        conn.commit()

    p_new_s_id_opt_menu()

    def p_new_c_id_opt_menu():
        # Options Menu For all existing choices
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT c_id FROM choices ORDER BY c_id""")
        p_new_c_id_list_raw = c.fetchall()
        p_new_c_id_list_raw_2 = id.raw_conv(p_new_c_id_list_raw)
        # Get Only c_id's with no paragraphs assigned to them
        p_new_c_id_list = id.c_id_sorter(p_new_c_id_list_raw_2)

        if p_new_c_id_list:
            global p_new_p_id_variable
            p_new_p_id_variable = StringVar()
            p_new_c_id_opt_menu_var = ttk.OptionMenu(p_new_info_frame_1, p_new_p_id_variable, p_new_c_id_list[0], *p_new_c_id_list)
            p_new_c_id_opt_menu_var.grid(row=1, column=1, pady=p_new_pad, padx=p_new_pad, stick="ew")

        else:
            p_new_wd.destroy()
            messagebox.showerror("Index Error", "No Existing Choices were Found")

        conn.commit()

    p_new_c_id_opt_menu()

    test_buttons_func.error_update()

    p_new_wd.mainloop()


def p_edt_save_enemy():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    p_edt_p_id = p_edt_p_id_variable.get()

    p_edt_npc_name = p_edt_npc_name_variable.get()
    p_edt_mst_name = p_edt_mst_name_variable.get()

    # Check to see if an npc or mst has been assigned
    if p_edt_npc_name == p_edt_mst_name == 'None':
        messagebox.showerror("Input Error", f'You Must Assign An NPC or A Monster To This Paragraph', icon='warning')
    else:
        if p_edt_npc_name != 'None' and p_edt_mst_name == 'None':
            # Save Paragraph to NPC ID

            # Get npc_id with npc_name
            c.execute(f"""SELECT npc_id FROM npcs WHERE npc_name = '{p_edt_npc_name}'""")
            p_edt_npc_id_raw = c.fetchall()
            p_edt_npc_id = id.raw_conv(p_edt_npc_id_raw)[0]

            c.execute("""UPDATE paragraphs_list SET 
                                npc_id = :npc_id,
                                npc_bool = :npc_bool,
                                mst_id = :mst_id,
                                mst_bool = :mst_bool
                                WHERE pl_id = :pl_id""",
                      {
                          "pl_id": f'{p_edt_p_id}',
                          "npc_id": f'{p_edt_npc_id}',
                          "npc_bool": 1,
                          "mst_id": 'None',
                          "mst_bool": 0,
                      })

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Paragraph Number {id.id_int(p_edt_p_id)} Has Been Assigned NPC {p_edt_npc_name}.")

        elif p_edt_mst_name != 'None' and p_edt_npc_name == 'None':
            # Save paragraph to mst_id
            # Get mst_id with mst_name
            c.execute(f"""SELECT mst_id FROM monsters WHERE mst_name = '{p_edt_mst_name}'""")
            p_edt_mst_id_raw = c.fetchall()
            p_edt_mst_id = id.raw_conv(p_edt_mst_id_raw)[0]

            c.execute("""UPDATE paragraphs_list SET 
                                mst_id = :mst_id,
                                mst_bool = :mst_bool,
                                npc_id = :npc_id,
                                npc_bool = :npc_bool
                                WHERE pl_id = :pl_id""",
                      {
                          "pl_id": f'{p_edt_p_id}',
                          "mst_id": f'{p_edt_mst_id}',
                          "mst_bool": 1,
                          "npc_id": 'None',
                          "npc_bool": 0,
                      })

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Paragraph Number {id.id_int(p_edt_p_id)} Has Been Assigned Enemy {p_edt_mst_name}.")
        else:
            messagebox.showerror("Input Error", f'You Cannot Assign An Enemy And An NPC To A Paragraph', icon='warning')

        # Clear the Text Boxes
        p_edt_paragraph_text_entry.delete("1.0", "end")

    conn.commit()

    p_edt_npc_name_opt_menu()
    p_edt_mst_name_opt_menu()


def p_edt_save_edit():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    p_edt_s_id = p_edt_s_id_variable.get()
    p_edt_p_id = p_edt_p_id_variable.get()

    if len(p_edt_paragraph_text_entry.get("1.0", "end")) != 1:
        c.execute("""UPDATE paragraphs_list SET 
                p_text = :p_text
                
                WHERE pl_id = :pl_id""",
                  {
                      "p_text": p_edt_paragraph_text_entry.get("1.0", "end"),
                      "pl_id": f'{p_edt_p_id}'

                  })

        # Show Success pop-up
        messagebox.showinfo("Success",
                            f"Paragraph Number {id.id_int(p_edt_p_id)} in Story Number {id.id_int(p_edt_s_id)} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Paragraph Text is Empty', icon='warning')

    # Clear the Text Boxes
    p_edt_paragraph_text_entry.delete("1.0", "end")

    conn.commit()


def p_edt_insert():
    p_edt_paragraph_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    p_edt_p_id = p_edt_p_id_variable.get()

    c.execute(f"""SELECT p_text FROM paragraphs_list WHERE pl_id = '{p_edt_p_id}'""")
    p_edt_text_raw = c.fetchall()
    p_edt_text = ((p_edt_text_raw[0])[0])

    p_edt_paragraph_text_entry.insert(END, f'{p_edt_text}')

    conn.commit()


def p_edt_decode_id():
    p_edt_decode_id_variable.delete("1.0", "end")
    p_edt_decode_id_variable.insert(END, id.decoder_3(p_edt_p_id_variable.get()))


def p_del_delete():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()
    p_del_s_id = p_edt_s_id_variable.get()
    p_del_p_id = p_edt_p_id_variable.get()
    p_del_p_id_cut = id.decoder_2(p_del_p_id)[-1]

    p_del_warning = messagebox.askquestion('Confirm Deletion',
                                           f'Are you sure you want to delete Paragraph Number {id.id_int(p_del_p_id)}?',
                                           icon='warning')

    if p_del_warning == 'yes':
        c.execute(f"""DELETE FROM paragraphs_list WHERE pl_id LIKE '{p_del_p_id}%'""")
        c.execute(f"""DELETE FROM choices WHERE c_id LIKE '{p_del_p_id}%'""")

        # Remove Paragraph If it was assigned to a choice
        c.execute(f"""SELECT c_id FROM choices WHERE c_id LIKE '%{p_del_p_id_cut}'""")
        c_id_list_raw = c.fetchall()
        c_id_list = id.raw_conv(c_id_list_raw)

        for c_id in c_id_list:
            # Modify id
            c_del_c_id_new = id.p_del(c_id)

            # Update table
            c.execute(f"""UPDATE choices SET c_id = "{c_del_c_id_new}" WHERE c_id = '{c_id}'""")


        # Show Success pop-up
        messagebox.showinfo("Success",
                            f"Paragraph Number {id.id_int(p_del_p_id)} In Story Number {id.id_int(p_del_s_id)}\nhas been successfully deleted."
                            f"\nAll Paragraphs and Choices connected to Paragraph Number {id.id_int(p_del_p_id)} were also Deleted.")
        p_edt_paragraph_text_entry.delete("1.0", "end")
        p_edt_decode_id_variable.delete("1.0", "end")

    conn.commit()

    p_edt_p_id_opt_menu()


def p_edt_p_end():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()
    p_edt_p_id = p_edt_p_id_variable.get()
    p_edt_p_end_bool_raw = p_edt_p_end_variable.get()

    if p_edt_p_end_bool_raw == 'True':
        p_edt_p_end_bool = 1
    else:
        p_edt_p_end_bool = 0

    if p_edt_p_end_bool == 0:
        c.execute(f"""UPDATE paragraphs_list SET end_bool = '{p_edt_p_end_bool}' WHERE pl_id = '{p_edt_p_id}'""")

        messagebox.showinfo("Ending Paragraph", f"Paragraph Number {id.id_int(p_edt_p_id)} Has Been Unassigned From Being An Ending Paragraph")

    else:
        c.execute(f"""UPDATE paragraphs_list SET 
        end_bool = '{p_edt_p_end_bool}'
        
        WHERE pl_id = '{p_edt_p_id}'""")

        c.execute(f"""DELETE FROM choices WHERE c_id LIKE '{p_edt_p_id}%'""")

        messagebox.showinfo("Ending Paragraph", f"Paragraph Number {id.id_int(p_edt_p_id)} Has Been Set To An Ending Paragraph."
                                                f"\nThis Paragraph Can No Longer Have Choices Assigned to it.")
    conn.commit()


def p_edt_window():
    style_func()
    global p_edt_wd, database
    database = editor_settings.database_module.database
    p_edt_wd = Toplevel()
    path = os.path.dirname(__file__)
    p_edt_wd.iconbitmap(f'{path}/Illustrations/Icon/editor_icon_2.ico')
    p_edt_wd.grab_set()
    p_edt_wd.title("Edit Paragraphs")
    screen_x_2 = p_edt_wd.winfo_screenwidth()
    screen_y_2 = p_edt_wd.winfo_screenheight()
    window_x_2 = 990
    window_y_2 = 637
    p_edt_wd.minsize(window_x_2, window_y_2)
    p_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    p_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    p_edt_frame_height = 400
    p_edt_info_frame_height = 57

    # Top Frame
    p_edt_top_frame = Frame(p_edt_wd, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_top_frame.pack(fill="both", side=TOP)

    #

    # Select Info Frame
    p_edt_select_info_frame = LabelFrame(p_edt_top_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_select_info_frame.pack(fill="both", side=LEFT)

    # Info Frame 1
    p_edt_info_frame_1 = Frame(p_edt_select_info_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_info_frame_1.pack(fill="both", side=TOP)

    # Info Frame 3 (Button)
    p_edt_info_frame_3 = Frame(p_edt_select_info_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_info_frame_3.pack(fill="both", side=TOP)

    #

    # Select Spec Frame
    p_edt_select_spec_frame = Frame(p_edt_top_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_select_spec_frame.pack(fill="both", side=RIGHT)

    # Select NPC Frame
    p_edt_select_npc_frame = LabelFrame(p_edt_select_spec_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_select_npc_frame.pack(fill="both")

    # Spec Frame 1
    p_edt_spec_frame_1 = Frame(p_edt_select_npc_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_spec_frame_1.pack(fill="both")

    # Spec Frame 2 (Button)
    p_edt_spec_frame_2 = Frame(p_edt_select_npc_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_spec_frame_2.pack(fill="both")

    # Bottom Frame
    p_edt_bottom_frame = Frame(p_edt_wd, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_bottom_frame.pack(fill="both", side=BOTTOM, expand=True)

    #

    # Paragraph Edit Frame
    p_edt_p_edit_frame = LabelFrame(p_edt_bottom_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_p_edit_frame.pack(fill="y", side=LEFT)

    # Paragraph Edit Frame 1
    p_edt_p_edit_frame_1 = Frame(p_edt_p_edit_frame, height=p_edt_frame_height, width=window_x_2)
    p_edt_p_edit_frame_1.pack(fill="both")

    # Paragraph Edit Frame 2 (Button)
    p_edt_p_edit_frame_2 = Frame(p_edt_p_edit_frame, height=window_y_2 - p_edt_frame_height, width=window_x_2)
    p_edt_p_edit_frame_2.pack(fill="both")

    #

    # Paragraph Ending Frame
    p_edt_p_end_frame = Frame(p_edt_bottom_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_p_end_frame.pack(fill="both", side=RIGHT)

    # Paragraph Ending Frame_0
    p_edt_p_end_frame_0 = LabelFrame(p_edt_select_spec_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_p_end_frame_0.pack(fill="x", side=TOP)

    # Paragraph Ending Frame 1
    p_edt_p_end_frame_1 = Frame(p_edt_p_end_frame_0, height=p_edt_frame_height, width=window_x_2)
    p_edt_p_end_frame_1.pack(fill="both")

    # Paragraph Ending Frame 2 (Button)
    p_edt_p_end_frame_2 = Frame(p_edt_p_end_frame_0, height=window_y_2 - p_edt_frame_height, width=window_x_2)
    p_edt_p_end_frame_2.pack(fill="both")

    # Cancel Button Frame
    p_edt_cancel_frame = Frame(p_edt_p_end_frame, height=p_edt_info_frame_height, width=window_x_2)
    p_edt_cancel_frame.pack(fill="x", side=BOTTOM)

    p_edt_option_width = 39
    p_edt_entry_width = 37
    p_edt_width = 42
    p_edt_pad = 10

    # Labels
    p_edt_story_id_label = ttk.Label(p_edt_info_frame_1, text="Select Story ID:", width=int(p_edt_width / 2), anchor=W)
    p_edt_story_id_label.grid(row=0, column=0, padx=(p_edt_pad, p_edt_pad - 6), pady=p_edt_pad, stick="w")

    p_edt_choice_id_label = ttk.Label(p_edt_info_frame_1, text="Select Paragraph ID:", width=int(p_edt_width / 2), anchor=W)
    p_edt_choice_id_label.grid(row=1, column=0, padx=(p_edt_pad, p_edt_pad - 6), pady=p_edt_pad, stick="w")

    p_edt_npc_name_label = ttk.Label(p_edt_spec_frame_1, text="Select NPC Name:", width=int(p_edt_width / 2), anchor=W)
    p_edt_npc_name_label.grid(row=2, column=0, padx=(p_edt_pad, p_edt_pad - 6), pady=p_edt_pad, stick="w")

    p_edt_mst_name_label = ttk.Label(p_edt_spec_frame_1, text="Or Select Enemy Name:", width=int(p_edt_width / 2), anchor=W)
    p_edt_mst_name_label.grid(row=3, column=0, padx=(p_edt_pad, p_edt_pad - 6), pady=p_edt_pad, stick="w")

    p_edt_decode_id_label_text = ttk.Label(p_edt_info_frame_1, text="Decoded ID:", width=int(p_edt_width / 2), anchor=NW)
    p_edt_decode_id_label_text.grid(row=2, column=0, padx=(p_edt_pad, p_edt_pad - 5), pady=p_edt_pad, stick="nw")

    p_edt_paragraph_text_label = ttk.Label(p_edt_p_edit_frame_1, text="Edit Paragraph:", width=int(p_edt_width / 2) - 1,
                                       anchor=NW)
    p_edt_paragraph_text_label.grid(row=0, column=0, padx=p_edt_pad, pady=p_edt_pad, stick="nw")

    p_edt_paragraph_end_label = ttk.Label(p_edt_p_end_frame_1, text="Ending Paragraph:", width=int(p_edt_width / 2), anchor=W)
    p_edt_paragraph_end_label.grid(row=0, column=0, padx=(p_edt_pad, p_edt_pad - 6), pady=p_edt_pad, stick="w")

    # Message Box
    global p_edt_decode_id_variable
    p_edt_decode_id_variable = Text(p_edt_info_frame_1, width=p_edt_entry_width, height=5)
    p_edt_decode_id_variable.bind("<Key>", lambda a: "break")
    p_edt_decode_id_variable.grid(row=2, column=1, padx=p_edt_pad, pady=(p_edt_pad, p_edt_pad-3), stick="w")

    # Text
    global p_edt_paragraph_text_entry
    p_edt_paragraph_text_entry = Text(p_edt_p_edit_frame_1, width=p_edt_entry_width, height=20)
    p_edt_paragraph_text_entry.grid(row=0, column=1, padx=(p_edt_pad, p_edt_pad+5), pady=p_edt_pad, stick="w")

    # True Or False Option Menu For Ending Paragraph
    global p_edt_p_end_variable
    p_edt_p_end_variable = StringVar()
    p_edt_p_end_bool_list = [
        'True',
        'False'
    ]
    p_edt_p_id_opt_menu_var = ttk.OptionMenu(p_edt_p_end_frame_1, p_edt_p_end_variable, p_edt_p_end_bool_list[-1], *p_edt_p_end_bool_list)
    p_edt_p_id_opt_menu_var.config(width=p_edt_option_width)
    p_edt_p_id_opt_menu_var.grid(row=0, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

    # Buttons
    p_edt_submit_id_button = ttk.Button(p_edt_info_frame_3, text="Decode ID", width=int(p_edt_width / 2),
                                    command=p_edt_decode_id)
    p_edt_submit_id_button.grid(row=0, column=0, padx=p_edt_pad, pady=p_edt_pad, stick="w", ipadx=157)

    #

    p_edt_submit_enemy_button = ttk.Button(p_edt_spec_frame_2, text="Submit Enemy Changes", width=int(p_edt_width / 2),
                                    command=p_edt_save_enemy)
    p_edt_submit_enemy_button.grid(row=0, column=0, padx=p_edt_pad, pady=p_edt_pad, stick="w", ipadx=157)

    #

    p_edt_width_buttons = 19
    p_edt_save_story_button = ttk.Button(p_edt_p_edit_frame_2, text="Save Changes", width=p_edt_width_buttons,
                                     command=p_edt_save_edit)
    p_edt_save_story_button.grid(row=0, column=0, padx=(p_edt_pad + 1, p_edt_pad), pady=p_edt_pad, stick="w")

    p_edt_load_text_button = ttk.Button(p_edt_p_edit_frame_2, text="Load Paragraph", width=p_edt_width_buttons,
                                    command=p_edt_insert)
    p_edt_load_text_button.grid(row=0, column=1, padx=p_edt_pad, pady=p_edt_pad, stick="w")

    p_edt_delete_text_button = ttk.Button(p_edt_p_edit_frame_2, text="Delete Paragraph", width=p_edt_width_buttons,
                                      command=p_del_delete)
    p_edt_delete_text_button.grid(row=0, column=2, padx=(p_edt_pad, p_edt_pad + 1), pady=p_edt_pad, stick="w")

    #

    p_edt_cancel_button = ttk.Button(p_edt_cancel_frame, text="Cancel", width=int(p_edt_width / 2),
                                 command=p_edt_wd.destroy)
    p_edt_cancel_button.grid(row=0, column=0, padx=p_edt_pad, pady=(p_edt_pad, p_edt_pad+2), stick="w", ipadx=157)

    #

    p_edt_submit_enemy_button = ttk.Button(p_edt_p_end_frame_2, text="Submit Paragraph Changes", width=int(p_edt_width / 2),
                                       command=p_edt_p_end)
    p_edt_submit_enemy_button.grid(row=0, column=0, padx=p_edt_pad, pady=(p_edt_pad+5, p_edt_pad), stick="w", ipadx=157)


    global p_edt_s_id_opt_menu, p_edt_p_id_opt_menu, p_edt_npc_name_opt_menu, p_edt_mst_name_opt_menu

    def p_edt_s_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM paragraphs_list UNION SELECT s_id FROM paragraphs_list ORDER BY s_id""")
        p_edt_s_id_list_raw = c.fetchall()
        p_edt_s_id_list = id.raw_conv(p_edt_s_id_list_raw)

        if p_edt_s_id_list:
            global p_edt_s_id_variable
            p_edt_s_id_variable = StringVar()
            p_edt_s_id_variable.set(p_edt_s_id_list[0])
            p_edt_s_id_opt_menu_var = ttk.OptionMenu(p_edt_info_frame_1, p_edt_s_id_variable, *p_edt_s_id_list)
            p_edt_s_id_opt_menu_var.grid(row=0, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

        else:
            p_edt_wd.destroy()
            messagebox.showerror("Index Error", "No Existing Stories Found")

        conn.commit()

    def p_edt_p_id_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT pl_id FROM paragraphs_list ORDER BY pl_id""")
        p_edt_p_id_list_raw = c.fetchall()
        p_edt_p_id_list = id.raw_conv(p_edt_p_id_list_raw)

        if p_edt_p_id_list:
            global p_edt_p_id_variable
            p_edt_p_id_variable = StringVar()
            p_edt_p_id_opt_menu_var = ttk.OptionMenu(p_edt_info_frame_1, p_edt_p_id_variable, p_edt_p_id_list[0], *p_edt_p_id_list)
            p_edt_p_id_opt_menu_var.grid(row=1, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

            p_edt_npc_name_opt_menu()
            p_edt_mst_name_opt_menu()

        else:
            messagebox.showerror("Index Error", "No Existing Paragraphs Found")
            p_edt_wd.destroy()

        conn.commit()

    def p_edt_npc_name_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        # Get npc_id's that haven't been used
        c.execute(f"""SELECT npc_id FROM npcs""")
        p_edt_npc_id_list_raw = c.fetchall()
        p_edt_npc_id_list = id.raw_conv(p_edt_npc_id_list_raw)

        # Create a list for the names of each npc_id
        p_edt_npc_name_list = []

        for x_id in p_edt_npc_id_list:
            c.execute(f"""SELECT npc_name FROM npcs WHERE npc_id='{x_id}'""")
            p_edt_npc_name_raw = c.fetchall()
            p_edt_npc_name = id.raw_conv(p_edt_npc_name_raw)[0]
            p_edt_npc_name_list.append(p_edt_npc_name)

        global p_edt_npc_name_variable
        p_edt_npc_name_variable = StringVar()
        p_edt_npc_name_list.append('None')
        p_edt_npc_name_opt_menu_var = ttk.OptionMenu(p_edt_spec_frame_1, p_edt_npc_name_variable, p_edt_npc_name_list[-1], *p_edt_npc_name_list)
        p_edt_npc_name_opt_menu_var.configure(width=p_edt_option_width)
        p_edt_npc_name_opt_menu_var.grid(row=2, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

        if not p_edt_npc_name_list:
            messagebox.showerror("Index Error", "No Existing NPC's Found")

        conn.commit()

    def p_edt_mst_name_opt_menu():
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        # Get mst_id's that haven't been used
        c.execute(f"""SELECT mst_id FROM monsters""")
        p_edt_mst_id_list_raw = c.fetchall()
        p_edt_mst_id_list = id.raw_conv(p_edt_mst_id_list_raw)

        p_edt_mst_name_list = []

        # Create a list for the names of each mst_id
        for x_id in p_edt_mst_id_list:
            c.execute(f"""SELECT mst_name FROM monsters WHERE mst_id='{x_id}'""")
            p_edt_mst_name_raw = c.fetchall()
            p_edt_mst_name = id.raw_conv(p_edt_mst_name_raw)[0]
            p_edt_mst_name_list.append(p_edt_mst_name)

        global p_edt_mst_name_variable
        p_edt_mst_name_variable = StringVar()
        p_edt_mst_name_list.append('None')
        p_edt_mst_name_opt_menu_var = ttk.OptionMenu(p_edt_spec_frame_1, p_edt_mst_name_variable, p_edt_mst_name_list[-1], *p_edt_mst_name_list)
        p_edt_mst_name_opt_menu_var.configure(width=p_edt_option_width)
        p_edt_mst_name_opt_menu_var.grid(row=3, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

        if not p_edt_mst_name_list:
            messagebox.showerror("Index Error", "No Existing Enemies Found")

        conn.commit()

    p_edt_s_id_opt_menu()
    p_edt_p_id_opt_menu()

    test_buttons_func.error_update()

    p_edt_wd.mainloop()
