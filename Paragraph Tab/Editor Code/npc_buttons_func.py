# All necessary imports
import time
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as font
import sqlite3
import id

database = 'EditorDataV3.db'


def npc_new_save():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS npcs
                 (npc_id text,
                 npc_name text)""")

    # Create a new ch_id
    c.execute(f"""SELECT npc_id from npcs""")
    npc_new_npc_id_list_raw = c.fetchall()
    npc_new_npc_id_list = id.raw_conv(npc_new_npc_id_list_raw)

    if not npc_new_npc_id_list:
        npc_new_npc_id = 1
    else:
        npc_new_npc_id = int(id.max_num(id.int_list(npc_new_npc_id_list))) + 1

    npc_new_npc_name = npc_new_name_entry_var.get()

    c.execute(f"""SELECT npc_name FROM npcs WHERE npc_name = '{npc_new_npc_name}'""")
    npc_new_name_list_raw = c.fetchall()
    npc_new_name_list = id.raw_conv(npc_new_name_list_raw)

    if not npc_new_npc_name == '':
        if not npc_new_name_list:
            c.execute("""INSERT INTO npcs VALUES (
                       :npc_id, 
                       :npc_name)""",
                      {
                          'npc_id': str(id.npc_id(npc_new_npc_id)),
                          'npc_name': str(npc_new_npc_name),
                      })

            messagebox.showinfo("Success", f'NPC {npc_new_npc_name} Has Been Successfully Created.')
            # Clear the Text Boxes
            npc_new_name_entry.delete(0, END)
        else:
            messagebox.showerror("Duplication Error", f"NPC Called '{npc_new_npc_name}' Already Exists.", icon='warning')
    else:
        messagebox.showerror("Input Error", f"NPC Has To Be Named.", icon='warning')
    conn.commit()
    conn.close()


def npc_new_window():
    global npc_new_wd
    # Create New Window
    npc_new_wd = Toplevel()
    npc_new_wd.title("Create A New NPC")
    screen_x_2 = npc_new_wd.winfo_screenwidth()
    screen_y_2 = npc_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 95
    npc_new_wd.minsize(window_x_2, window_y_2)
    npc_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    npc_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    npc_new_frame_height = 200
    npc_new_rest = window_y_2 - npc_new_frame_height * 2
    # Info Frame 1
    npc_new_info_frame_1 = LabelFrame(npc_new_wd, width=window_x_2, height=npc_new_frame_height)
    npc_new_info_frame_1.pack(fill="both", side=TOP)

    # Top Button Frame
    npc_new_button_frame = LabelFrame(npc_new_wd, height=npc_new_rest / 2, width=window_x_2)
    npc_new_button_frame.pack(fill="both")

    npc_new_width = 42
    npc_new_pad = 10
    npc_new_entry_width = 49
    npc_new_text_width = 37

    # Labels
    npc_new_name_label = Label(npc_new_info_frame_1, text="Name:", width=int(npc_new_width / 2), anchor=W)
    npc_new_name_label.grid(row=0, column=0, padx=(npc_new_pad, npc_new_pad+4), pady=npc_new_pad, stick="w")

    # Short Entries
    global npc_new_name_entry_var, npc_new_name_entry
    npc_new_name_entry_var = StringVar()
    npc_new_name_entry = Entry(npc_new_info_frame_1, textvariable=npc_new_name_entry_var, width=npc_new_entry_width)
    npc_new_name_entry.grid(row=0, column=1, padx=npc_new_pad, pady=npc_new_pad, stick="nw")

    # Buttons
    npc_new_save_npc_button = Button(npc_new_button_frame, text="Save NPC", width=int(npc_new_width / 2),
                                          command=npc_new_save)
    npc_new_save_npc_button.grid(row=0, column=0, padx=npc_new_pad, pady=npc_new_pad, stick="w")

    npc_new_cancel_button = Button(npc_new_button_frame, text="Cancel", width=npc_new_width-1, command=npc_new_wd.destroy)
    npc_new_cancel_button.grid(row=0, column=1, padx=npc_new_pad, pady=npc_new_pad, stick="w")

    npc_new_wd.mainloop()


def npc_edt_delete():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    npc_edt_npc_name = npc_edt_npc_name_var.get()

    # Get npc_id with npc_name
    c.execute(f"""SELECT npc_id FROM npcs WHERE npc_name = '{npc_edt_npc_name}'""")
    npc_edt_npc_id_raw = c.fetchall()
    npc_edt_npc_id = str(id.raw_conv(npc_edt_npc_id_raw)[0])

    # Get pl_id with npc_id
    c.execute(f"""SELECT pl_id FROM paragraphs_list WHERE npc_id = '{npc_edt_npc_id}'""")
    npc_edt_pl_id_raw = c.fetchall()
    npc_edt_pl_id = id.raw_conv(npc_edt_pl_id_raw)

    # Make a string of it only if an actual pl_id connected to this character exists
    if npc_edt_pl_id:
        npc_edt_pl_id = str(id.raw_conv(npc_edt_pl_id_raw)[0])
    else:
        npc_edt_pl_id = '/'

    s_del_warning = messagebox.askquestion('Confirm Deletion',
                                           f"Are you sure you want to delete NPC called '{npc_edt_npc_name}'?",
                                           icon='warning')

    if s_del_warning == 'yes':
        if npc_edt_pl_id == '/':
            c.execute(f"""DELETE FROM npcs WHERE npc_id = '{npc_edt_npc_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success", f"NPC Called {npc_edt_npc_name} has been successfully deleted.")
        else:
            c.execute(f"""DELETE FROM npcs WHERE npc_id = '{npc_edt_npc_id}'""")
            c.execute(f"""UPDATE paragraphs_list SET 
            npc_id = 'None'
            npc_bool = f{0} 
            WHERE npc_id = '{npc_edt_npc_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Character Number '{npc_edt_npc_name}' has been successfully deleted.")

        conn.commit()
        conn.close()

        # Delete Previous Input
        npc_edt_name_entry.delete(0, END)

        npc_edt_npc_name_opt_menu()

    else:
        conn.commit()
        conn.close()


def npc_edt_insert():
    # Delete Previous Input
    npc_edt_name_entry.delete(0, END)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    npc_edt_npc_name = npc_edt_npc_name_var.get()

    c.execute(f"""SELECT npc_name FROM npcs WHERE npc_name = '{npc_edt_npc_name}'""")
    npc_edt_name_list_raw = c.fetchall()
    npc_edt_name_list = id.raw_conv(npc_edt_name_list_raw)

    # Input data into text box
    npc_edt_name_entry.insert(END, f'{npc_edt_name_list[0]}')

    conn.commit()
    conn.close()


def npc_edt_edit():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    npc_edt_npc_name_old = npc_edt_npc_name_var.get()

    npc_edt_npc_name = npc_edt_name_entry.get()
    if npc_edt_npc_name != '':
        c.execute(f"""UPDATE npcs SET npc_name = '{npc_edt_npc_name}' WHERE npc_name = '{npc_edt_npc_name_old}'""")

        messagebox.showinfo("Success", f"NPC '{npc_edt_npc_name_old}' has been successfully Renamed.")

        # Clear the Text Boxes
        npc_edt_name_entry.delete(0, END)

    else:
        messagebox.showerror("Input Error", f'Input a Name', icon='warning')

    conn.commit()
    conn.close()

    npc_edt_npc_name_opt_menu()


def npc_edt_window():
    global npc_edt_wd
    # Create New Window
    npc_edt_wd = Toplevel()
    npc_edt_wd.title("Edit A Character")
    screen_x_2 = npc_edt_wd.winfo_screenwidth()
    screen_y_2 = npc_edt_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 150
    npc_edt_wd.minsize(window_x_2, window_y_2)
    npc_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    npc_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    npc_edt_frame_height = 200
    npc_edt_rest = window_y_2 - npc_edt_frame_height * 2
    # Info Frame 0
    npc_edt_info_frame_0 = LabelFrame(npc_edt_wd, width=window_x_2, height=npc_edt_frame_height)
    npc_edt_info_frame_0.pack(fill="both", side=TOP)

    # Info Frame 1
    npc_edt_info_frame_1 = LabelFrame(npc_edt_wd, width=window_x_2, height=npc_edt_frame_height)
    npc_edt_info_frame_1.pack(fill="both", side=TOP)

    # Button Frame
    npc_edt_button_frame = LabelFrame(npc_edt_wd, height=npc_edt_rest / 2, width=window_x_2)
    npc_edt_button_frame.pack(fill="both")

    npc_edt_width = 42
    npc_edt_pad = 10
    npc_edt_entry_width = 49
    npc_edt_text_width = 37

    # Labels
    npc_edt_select_npc_label = Label(npc_edt_info_frame_0, text="Select NPC:", width=int(npc_edt_width / 2), anchor=W)
    npc_edt_select_npc_label.grid(row=0, column=0, padx=(npc_edt_pad, npc_edt_pad - 3), pady=npc_edt_pad, stick="w")

    npc_edt_name_label = Label(npc_edt_info_frame_1, text="Rename:", width=int(npc_edt_width / 2), anchor=W)
    npc_edt_name_label.grid(row=0, column=0, padx=npc_edt_pad, pady=npc_edt_pad, stick="w")

    # Short Entries
    global npc_edt_name_entry_var, npc_edt_name_entry
    npc_edt_name_entry_var = StringVar()
    npc_edt_name_entry = Entry(npc_edt_info_frame_1, textvariable=npc_edt_name_entry_var, width=npc_edt_entry_width)
    npc_edt_name_entry.grid(row=0, column=1, padx=npc_edt_pad, pady=npc_edt_pad, stick="nw")

    # Buttons
    npc_edt_width_buttons = 13
    npc_edt_save_changes_button = Button(npc_edt_button_frame, text="Save Changes", width=npc_edt_width_buttons,
                                        command=npc_edt_edit)
    npc_edt_save_changes_button.grid(row=0, column=0, padx=(npc_edt_pad + 9, npc_edt_pad), pady=npc_edt_pad, stick="w")

    npc_edt_load_npc_button = Button(npc_edt_button_frame, text="Load NPC", width=npc_edt_width_buttons,
                                          command=npc_edt_insert)
    npc_edt_load_npc_button.grid(row=0, column=1, padx=npc_edt_pad, pady=npc_edt_pad, stick="w")

    npc_edt_delete_npc_button = Button(npc_edt_button_frame, text="Delete NPC", width=npc_edt_width_buttons,
                                            command=npc_edt_delete)
    npc_edt_delete_npc_button.grid(row=0, column=2, padx=npc_edt_pad, pady=npc_edt_pad, stick="w")

    npc_edt_cancel_button = Button(npc_edt_button_frame, text="Cancel", width=npc_edt_width_buttons,
                                  command=npc_edt_wd.destroy)
    npc_edt_cancel_button.grid(row=0, column=3, padx=npc_edt_pad, pady=npc_edt_pad, stick="w")

    global npc_edt_npc_name_opt_menu

    def npc_edt_npc_name_opt_menu():
        # Options Menu For all existing NPC Names
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT npc_name FROM npcs""")
        npc_new_npc_name_list_raw = c.fetchall()
        npc_new_npc_name_list = id.raw_conv(npc_new_npc_name_list_raw)

        if npc_new_npc_name_list:
            global npc_edt_npc_name_var
            npc_edt_npc_name_var = StringVar()
            npc_edt_npc_name_var.set(npc_new_npc_name_list[0])
            npc_edt_npc_name_opt_menu_var = OptionMenu(npc_edt_info_frame_0, npc_edt_npc_name_var,
                                                          *npc_new_npc_name_list)
            npc_edt_npc_name_opt_menu_var.config(width=npc_edt_width + 1)
            npc_edt_npc_name_opt_menu_var.grid(row=0, column=1, pady=npc_edt_pad, padx=npc_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing NPC's were Found")
            npc_edt_wd.destroy()

        conn.commit()
        conn.close()

    npc_edt_npc_name_opt_menu()

    npc_edt_wd.mainloop()


