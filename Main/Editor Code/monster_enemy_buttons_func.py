# All necessary imports
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import id
import os
import editor_settings
import test_buttons_func


def style_func():
    mst_font_size = 11
    mst_style = ttk.Style()
    mst_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', mst_font_size))
    mst_style.configure("TButton", font=('Times New Roman', mst_font_size))
    mst_style.configure("TLabel", font=('Times New Roman', mst_font_size))


def mst_new_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS monsters
                 (mst_id text,
                 mst_name text,
                 mst_type text)""")

    # Create a new mst_id
    c.execute(f"""SELECT mst_id from monsters""")
    mst_new_mst_id_list_raw = c.fetchall()
    mst_new_mst_id_list = id.raw_conv(mst_new_mst_id_list_raw)

    if not mst_new_mst_id_list:
        mst_new_mst_id = 1
    else:
        mst_new_mst_id = int(id.max_num(id.int_list(mst_new_mst_id_list))) + 1

    mst_new_mst_name = mst_new_name_entry_var.get()

    try:
        c.execute(f"""SELECT mst_name FROM monsters WHERE mst_name = '{mst_new_mst_name}'""")
        mst_new_name_list_raw = c.fetchall()
        mst_new_name_list = id.raw_conv(mst_new_name_list_raw)

        if not mst_new_mst_name == '':
            if not mst_new_name_list:
                c.execute("""INSERT INTO monsters VALUES (
                           :mst_id, 
                           :mst_name,
                           :mst_type)""",
                          {
                              'mst_id': str(id.mst_id(mst_new_mst_id)),
                              'mst_name': str(mst_new_name_entry_var.get()),
                              'mst_type': str(mst_new_mst_type_var.get())

                          })

                messagebox.showinfo("Success", f'{mst_new_mst_type_var.get()} Number {mst_new_mst_id} Has Been Successfully Created.')
                # Clear the Text Boxes
                mst_new_name_entry.delete(0, END)
            else:
                messagebox.showerror("Duplication Error", f"{mst_new_mst_type_var.get()} Called '{mst_new_mst_name}' Already Exists.")
        else:
            messagebox.showerror("Input Error", f"Enemy Has To Be Named.", icon='warning')
    except sqlite3.OperationalError:
        messagebox.showerror("Input Error", "No Weird Symbols In Enemy Name Please")

    conn.commit()


def mst_new_window():
    style_func()
    global mst_new_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    mst_new_wd = Toplevel()
    path = os.path.dirname(__file__)
    mst_new_wd.iconbitmap(f'{path}/Illustrations/Icon/editor_icon_2.ico')
    mst_new_wd.grab_set()
    mst_new_wd.title("Create An Enemy")
    screen_x_2 = mst_new_wd.winfo_screenwidth()
    screen_y_2 = mst_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 141
    mst_new_wd.minsize(window_x_2, window_y_2)
    mst_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    mst_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    mst_new_frame_height = 200
    mst_new_rest = window_y_2 - mst_new_frame_height * 2
    # Info Frame 1
    mst_new_info_frame_1 = LabelFrame(mst_new_wd, width=window_x_2, height=mst_new_frame_height)
    mst_new_info_frame_1.pack(fill="both", side=TOP)

    # Top Button Frame
    mst_new_button_frame = LabelFrame(mst_new_wd, height=mst_new_rest / 2, width=window_x_2)
    mst_new_button_frame.pack(fill="both")

    mst_new_width = 42
    mst_new_pad = 10
    mst_new_entry_width = 49

    # Labels
    npc_new_type_label = ttk.Label(mst_new_info_frame_1, text="Select Enemy Type:", width=int(mst_new_width / 2), anchor=W)
    npc_new_type_label.grid(row=0, column=0, padx=(mst_new_pad, mst_new_pad + 4), pady=mst_new_pad, stick="w")
    
    npc_new_name_label = ttk.Label(mst_new_info_frame_1, text="Enemy Name:", width=int(mst_new_width / 2), anchor=W)
    npc_new_name_label.grid(row=1, column=0, padx=(mst_new_pad, mst_new_pad+4), pady=mst_new_pad, stick="w")

    # Short Entries
    global mst_new_name_entry_var, mst_new_name_entry
    mst_new_name_entry_var = StringVar()
    mst_new_name_entry = ttk.Entry(mst_new_info_frame_1, textvariable=mst_new_name_entry_var, width=mst_new_entry_width)
    mst_new_name_entry.grid(row=1, column=1, padx=mst_new_pad, pady=mst_new_pad, stick="nw")
    
    # Option Enemy Type Menu
    mst_new_mst_type_list = ['Human', 'Monster']
    global mst_new_mst_type_var
    mst_new_mst_type_var = StringVar()
    mst_new_mst_type_opt_menu_var = ttk.OptionMenu(mst_new_info_frame_1, mst_new_mst_type_var, mst_new_mst_type_list[0], *mst_new_mst_type_list)
    mst_new_mst_type_opt_menu_var.grid(row=0, column=1, pady=mst_new_pad, padx=mst_new_pad, stick="ew")

    # Buttons
    npc_new_save_npc_button = ttk.Button(mst_new_button_frame, text="Save Enemy", width=int(mst_new_width / 2),
                                          command=mst_new_save)
    npc_new_save_npc_button.grid(row=0, column=0, padx=mst_new_pad, pady=mst_new_pad, stick="w")

    npc_new_cancel_button = ttk.Button(mst_new_button_frame, text="Cancel", width=mst_new_width-1, command=mst_new_wd.destroy)
    npc_new_cancel_button.grid(row=0, column=1, padx=mst_new_pad, pady=mst_new_pad, stick="w")

    test_buttons_func.error_update()

    mst_new_wd.mainloop()


def mst_edt_delete():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    mst_edt_ch_name = mst_new_mst_name_id_var.get()

    # Get mst_id with mst_name
    c.execute(f"""SELECT mst_id FROM monsters WHERE mst_name = '{mst_edt_ch_name}'""")
    mst_edt_mst_id_raw = c.fetchall()
    mst_edt_mst_id = str(id.raw_conv(mst_edt_mst_id_raw)[0])

    # Get pl_id with mst_id
    c.execute(f"""SELECT pl_id FROM paragraphs_list WHERE mst_id = '{mst_edt_mst_id}'""")
    npc_edt_s_id_raw = c.fetchall()
    mst_edt_s_id = id.raw_conv(npc_edt_s_id_raw)

    # Make a string of it only if an actual pl_id connected to this character exists
    if mst_edt_s_id:
        mst_edt_s_id = str(id.raw_conv(npc_edt_s_id_raw)[0])
    else:
        mst_edt_s_id = '/'

    s_del_warning = messagebox.askquestion('Confirm Deletion',
                                           f"Are you sure you want to delete NPC called '{mst_edt_ch_name}'?",
                                           icon='warning')

    if s_del_warning == 'yes':
        if mst_edt_s_id == '/':
            c.execute(f"""DELETE FROM monsters WHERE mst_id = '{mst_edt_mst_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success", f"Enemy '{mst_edt_ch_name}' has been successfully deleted.")
        else:
            c.execute(f"""DELETE FROM monsters WHERE mst_id = '{mst_edt_mst_id}'""")
            c.execute(f"""UPDATE paragraphs_list SET mst_id = 'None' WHERE mst_id = '{mst_edt_mst_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Enemy '{mst_edt_ch_name}' has been successfully deleted.")

        # Delete Previous Input
        mst_edt_name_entry.delete(0, END)

        conn.commit()

        mst_edt_mst_name_opt_menu()

    conn.commit()


def mst_edt_insert():
    # Delete Previous Input
    mst_edt_name_entry.delete(0, END)

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    mst_edt_mst_name = mst_new_mst_name_id_var.get()

    c.execute(f"""SELECT mst_name FROM monsters WHERE mst_name = '{mst_edt_mst_name}'""")
    mst_edt_name_list_raw = c.fetchall()
    mst_edt_name_list = id.raw_conv(mst_edt_name_list_raw)

    # Input data into text box
    mst_edt_name_entry.insert(END, f'{mst_edt_name_list[0]}')

    conn.commit()


def mst_edt_edit():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    mst_edt_mst_name_var = mst_new_mst_name_id_var.get()

    mst_edt_mst_name = mst_edt_name_entry.get()
    try:
        if mst_edt_mst_name != '':
            c.execute(f"""UPDATE monsters SET mst_name = '{mst_edt_mst_name}' WHERE mst_name = '{mst_edt_mst_name_var}'""")

            messagebox.showinfo("Success", f"Enemy '{mst_edt_mst_name_var}' has been successfully Renamed.")

            # Clear the Text Boxes
            mst_edt_name_entry.delete(0, END)

        else:
            messagebox.showerror("Input Error", f'Input a Name', icon='warning')
    except sqlite3.OperationalError:
        messagebox.showerror("Input Error", "No Weird Symbols In Enemy Name Please")

    conn.commit()

    mst_edt_mst_name_opt_menu()


def mst_edt_window():
    style_func()
    global mst_edt_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    mst_edt_wd = Toplevel()
    mst_edt_wd.grab_set()
    mst_edt_wd.title("Edit An Enemy")
    screen_x_2 = mst_edt_wd.winfo_screenwidth()
    screen_y_2 = mst_edt_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 141
    mst_edt_wd.minsize(window_x_2, window_y_2)
    mst_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    mst_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    mst_edt_frame_height = 200
    mst_edt_rest = window_y_2 - mst_edt_frame_height * 2
    # Info Frame 0
    mst_edt_info_frame_0 = Frame(mst_edt_wd, width=window_x_2, height=mst_edt_frame_height)
    mst_edt_info_frame_0.pack(fill="both", side=TOP)

    # Button Frame
    mst_edt_button_frame = Frame(mst_edt_wd, height=mst_edt_rest / 2, width=window_x_2)
    mst_edt_button_frame.pack(fill="both")

    mst_edt_width = 42
    mst_edt_pad = 10
    mst_edt_entry_width = 49

    # Labels
    mst_edt_select_mst_label = ttk.Label(mst_edt_info_frame_0, text="Select Enemy:", width=int(mst_edt_width / 2), anchor=W)
    mst_edt_select_mst_label.grid(row=0, column=0, padx=(mst_edt_pad, mst_edt_pad - 3), pady=mst_edt_pad, stick="w")

    mst_edt_name_label = ttk.Label(mst_edt_info_frame_0, text="Name:", width=int(mst_edt_width / 2), anchor=W)
    mst_edt_name_label.grid(row=1, column=0, padx=mst_edt_pad, pady=mst_edt_pad, stick="w")

    # Short Entries
    global mst_edt_name_entry_var, mst_edt_name_entry
    mst_edt_name_entry_var = StringVar()
    mst_edt_name_entry = ttk.Entry(mst_edt_info_frame_0, textvariable=mst_edt_name_entry_var, width=mst_edt_entry_width)
    mst_edt_name_entry.grid(row=1, column=1, padx=mst_edt_pad, pady=mst_edt_pad, stick="nw")

    # Buttons
    mst_edt_width_buttons = 13
    mst_edt_save_changes_button = ttk.Button(mst_edt_button_frame, text="Save Changes", width=mst_edt_width_buttons,
                                         command=mst_edt_edit)
    mst_edt_save_changes_button.grid(row=0, column=0, padx=(mst_edt_pad + 9, mst_edt_pad), pady=mst_edt_pad, stick="w")

    mst_edt_load_mst_button = ttk.Button(mst_edt_button_frame, text="Load Enemy", width=mst_edt_width_buttons,
                                     command=mst_edt_insert)
    mst_edt_load_mst_button.grid(row=0, column=1, padx=mst_edt_pad, pady=mst_edt_pad, stick="w")

    mst_edt_delete_mst_button = ttk.Button(mst_edt_button_frame, text="Delete Enemy", width=mst_edt_width_buttons,
                                      command=mst_edt_delete)
    mst_edt_delete_mst_button.grid(row=0, column=2, padx=mst_edt_pad, pady=mst_edt_pad, stick="w")

    mst_edt_cancel_button = ttk.Button(mst_edt_button_frame, text="Cancel", width=mst_edt_width_buttons,
                                   command=mst_edt_wd.destroy)
    mst_edt_cancel_button.grid(row=0, column=3, padx=mst_edt_pad, pady=mst_edt_pad, stick="w")

    global mst_edt_mst_name_opt_menu

    def mst_edt_mst_name_opt_menu():
        # Options Menu For all existing Enemies Names
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute(f"""SELECT mst_name FROM monsters""")
        mst_new_mst_name_id_ist_raw = c.fetchall()
        mst_new_mst_name_id_list = id.raw_conv(mst_new_mst_name_id_ist_raw)

        if mst_new_mst_name_id_list:
            global mst_new_mst_name_id_var
            mst_new_mst_name_id_var = StringVar()
            mst_edt_mst_name_id_opt_menu_var = ttk.OptionMenu(mst_edt_info_frame_0, mst_new_mst_name_id_var, mst_new_mst_name_id_list[0], *mst_new_mst_name_id_list)
            mst_edt_mst_name_id_opt_menu_var.grid(row=0, column=1, pady=mst_edt_pad, padx=mst_edt_pad, stick="ew")

        else:
            mst_edt_wd.destroy()
            messagebox.showerror("Index Error", "No Existing Enemies were Found")

        conn.commit()

    mst_edt_mst_name_opt_menu()

    test_buttons_func.error_update()

    mst_edt_wd.mainloop()

