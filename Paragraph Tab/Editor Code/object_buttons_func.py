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


def obj_new_save():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS objects
                 (obj_id text,
                 obj_name text)""")

    # Create a new obj_id
    c.execute(f"""SELECT obj_id from objects""")
    obj_new_obj_id_list_raw = c.fetchall()
    obj_new_obj_id_list = id.raw_conv(obj_new_obj_id_list_raw)

    if not obj_new_obj_id_list:
        obj_new_obj_id = 1
    else:
        obj_new_obj_id = int(id.max_num(id.int_list(obj_new_obj_id_list))) + 1

    obj_new_obj_name = obj_new_name_entry_var.get()

    c.execute(f"""SELECT obj_name FROM objects WHERE obj_name = '{obj_new_obj_name}'""")
    obj_new_name_list_raw = c.fetchall()
    obj_new_name_list = id.raw_conv(obj_new_name_list_raw)

    if not obj_new_obj_name == '':
        if not obj_new_name_list:
            c.execute("""INSERT INTO objects VALUES (
                       :obj_id, 
                       :obj_name)""",
                      {
                          'obj_id': str(id.obj_id(obj_new_obj_id)),
                          'obj_name': str(obj_new_obj_name),
                      })

            messagebox.showinfo("Success", f'Object {obj_new_obj_name} Has Been Successfully Created.')
            # Clear the Text Boxes
            obj_new_name_entry.delete(0, END)
        else:
            messagebox.showerror("Duplication Error", f"Object Called '{obj_new_obj_name}' Already Exists.", icon='warning')
    else:
        messagebox.showerror("Input Error", f"Object Has to be named", icon='warning')

    conn.commit()
    conn.close()


def obj_new_window():
    global obj_new_wd
    # Create New Window
    obj_new_wd = Toplevel()
    obj_new_wd.title("Create A New Object")
    screen_x_2 = obj_new_wd.winfo_screenwidth()
    screen_y_2 = obj_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 95
    obj_new_wd.minsize(window_x_2, window_y_2)
    obj_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    obj_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    obj_new_frame_height = 200
    obj_new_rest = window_y_2 - obj_new_frame_height * 2
    # Info Frame 1
    obj_new_info_frame_1 = LabelFrame(obj_new_wd, width=window_x_2, height=obj_new_frame_height)
    obj_new_info_frame_1.pack(fill="both", side=TOP)

    # Top Button Frame
    obj_new_button_frame = LabelFrame(obj_new_wd, height=obj_new_rest / 2, width=window_x_2)
    obj_new_button_frame.pack(fill="both")

    obj_new_width = 42
    obj_new_pad = 10
    obj_new_entry_width = 49
    obj_new_text_width = 37

    # Labels
    obj_new_name_label = Label(obj_new_info_frame_1, text="Object Name:", width=int(obj_new_width / 2), anchor=W)
    obj_new_name_label.grid(row=0, column=0, padx=(obj_new_pad, obj_new_pad+4), pady=obj_new_pad, stick="w")

    # Short Entries
    global obj_new_name_entry_var, obj_new_name_entry
    obj_new_name_entry_var = StringVar()
    obj_new_name_entry = Entry(obj_new_info_frame_1, textvariable=obj_new_name_entry_var, width=obj_new_entry_width)
    obj_new_name_entry.grid(row=0, column=1, padx=obj_new_pad, pady=obj_new_pad, stick="nw")

    # Buttons
    obj_new_save_obj_button = Button(obj_new_button_frame, text="Save Object", width=int(obj_new_width / 2),
                                          command=obj_new_save)
    obj_new_save_obj_button.grid(row=0, column=0, padx=obj_new_pad, pady=obj_new_pad, stick="w")

    obj_new_cancel_button = Button(obj_new_button_frame, text="Cancel", width=obj_new_width-1, command=obj_new_wd.destroy)
    obj_new_cancel_button.grid(row=0, column=1, padx=obj_new_pad, pady=obj_new_pad, stick="w")

    obj_new_wd.mainloop()


def obj_edt_delete():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    obj_edt_obj_name = obj_edt_obj_name_var.get()

    # Get obj_id with obj_name
    c.execute(f"""SELECT obj_id FROM objects WHERE obj_name = '{obj_edt_obj_name}'""")
    obj_edt_obj_id_raw = c.fetchall()
    obj_edt_obj_id = str(id.raw_conv(obj_edt_obj_id_raw)[0])

    # Get c_id with obj_id
    c.execute(f"""SELECT c_id FROM choices WHERE obj_id = '{obj_edt_obj_id}'""")
    obj_edt_c_id_raw = c.fetchall()
    obj_edt_c_id = id.raw_conv(obj_edt_c_id_raw)

    # Make a string of it only if an actual c_id connected to this object exists
    if obj_edt_c_id:
        obj_edt_c_id = str(id.raw_conv(obj_edt_c_id_raw)[0])
    else:
        obj_edt_c_id = '/'

    s_del_warning = messagebox.askquestion('Confirm Deletion',
                                           f"Are you sure you want to delete Object called '{obj_edt_obj_name}'?",
                                           icon='warning')

    if s_del_warning == 'yes':
        if obj_edt_c_id == '/':
            c.execute(f"""DELETE FROM objects WHERE obj_id = '{obj_edt_obj_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success", f"Object Called '{obj_edt_obj_name}' has been successfully deleted.")
        else:
            c.execute(f"""DELETE FROM objects WHERE obj_id = '{obj_edt_obj_id}'""")
            c.execute(f"""UPDATE choices SET 
            obj_id = 'None'
            WHERE obj_id = '{obj_edt_obj_id}'""")

            # Show Success pop-up
            messagebox.showinfo("Success",
                                f"Object '{obj_edt_obj_name}' has been successfully deleted.")

        conn.commit()
        conn.close()

        # Delete Previous Input
        obj_edt_name_entry.delete(0, END)

        obj_edt_obj_name_opt_menu()

    else:
        conn.commit()
        conn.close()


def obj_edt_insert():
    # Delete Previous Input
    obj_edt_name_entry.delete(0, END)

    conn = sqlite3.connect(database)
    c = conn.cursor()

    obj_edt_obj_name = obj_edt_obj_name_var.get()

    c.execute(f"""SELECT obj_name FROM objects WHERE obj_name = '{obj_edt_obj_name}'""")
    obj_edt_name_list_raw = c.fetchall()
    obj_edt_name_list = id.raw_conv(obj_edt_name_list_raw)

    # Input data into text box
    obj_edt_name_entry.insert(END, f'{obj_edt_name_list[0]}')

    conn.commit()
    conn.close()


def obj_edt_edit():
    conn = sqlite3.connect(database)
    c = conn.cursor()

    obj_edt_obj_name_old = obj_edt_obj_name_var.get()

    obj_edt_obj_name = obj_edt_name_entry.get()
    if obj_edt_obj_name != '':
        c.execute(f"""UPDATE objects SET obj_name = '{obj_edt_obj_name}' WHERE obj_name = '{obj_edt_obj_name_old}'""")

        messagebox.showinfo("Success", f"Object '{obj_edt_obj_name_old}' has been successfully Renamed.")

        # Clear the Text Boxes
        obj_edt_name_entry.delete(0, END)

    else:
        messagebox.showerror("Input Error", f'Input a Name', icon='warning')

    conn.commit()
    conn.close()

    obj_edt_obj_name_opt_menu()


def obj_edt_window():
    global obj_edt_wd
    # Create New Window
    obj_edt_wd = Toplevel()
    obj_edt_wd.title("Edit An Object")
    screen_x_2 = obj_edt_wd.winfo_screenwidth()
    screen_y_2 = obj_edt_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 150
    obj_edt_wd.minsize(window_x_2, window_y_2)
    obj_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    obj_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    obj_edt_frame_height = 200
    obj_edt_rest = window_y_2 - obj_edt_frame_height * 2
    # Info Frame 0
    obj_edt_info_frame_0 = LabelFrame(obj_edt_wd, width=window_x_2, height=obj_edt_frame_height)
    obj_edt_info_frame_0.pack(fill="both", side=TOP)

    # Info Frame 1
    obj_edt_info_frame_1 = LabelFrame(obj_edt_wd, width=window_x_2, height=obj_edt_frame_height)
    obj_edt_info_frame_1.pack(fill="both", side=TOP)

    # Button Frame
    obj_edt_button_frame = LabelFrame(obj_edt_wd, height=obj_edt_rest / 2, width=window_x_2)
    obj_edt_button_frame.pack(fill="both")

    obj_edt_width = 42
    obj_edt_pad = 10
    obj_edt_entry_width = 49
    obj_edt_text_width = 37

    # Labels
    obj_edt_select_obj_label = Label(obj_edt_info_frame_0, text="Select Object:", width=int(obj_edt_width / 2), anchor=W)
    obj_edt_select_obj_label.grid(row=0, column=0, padx=(obj_edt_pad, obj_edt_pad - 3), pady=obj_edt_pad, stick="w")

    obj_edt_name_label = Label(obj_edt_info_frame_1, text="Rename:", width=int(obj_edt_width / 2), anchor=W)
    obj_edt_name_label.grid(row=0, column=0, padx=obj_edt_pad, pady=obj_edt_pad, stick="w")

    # Short Entries
    global obj_edt_name_entry_var, obj_edt_name_entry
    obj_edt_name_entry_var = StringVar()
    obj_edt_name_entry = Entry(obj_edt_info_frame_1, textvariable=obj_edt_name_entry_var, width=obj_edt_entry_width)
    obj_edt_name_entry.grid(row=0, column=1, padx=obj_edt_pad, pady=obj_edt_pad, stick="nw")

    # Buttons
    obj_edt_width_buttons = 13
    obj_edt_save_changes_button = Button(obj_edt_button_frame, text="Save Changes", width=obj_edt_width_buttons,
                                         command=obj_edt_edit)
    obj_edt_save_changes_button.grid(row=0, column=0, padx=(obj_edt_pad + 9, obj_edt_pad), pady=obj_edt_pad, stick="w")

    obj_edt_load_obj_button = Button(obj_edt_button_frame, text="Load Object", width=obj_edt_width_buttons,
                                     command=obj_edt_insert)
    obj_edt_load_obj_button.grid(row=0, column=1, padx=obj_edt_pad, pady=obj_edt_pad, stick="w")

    obj_edt_delete_obj_button = Button(obj_edt_button_frame, text="Delete Object", width=obj_edt_width_buttons,
                                            command=obj_edt_delete)
    obj_edt_delete_obj_button.grid(row=0, column=2, padx=obj_edt_pad, pady=obj_edt_pad, stick="w")

    obj_edt_cancel_button = Button(obj_edt_button_frame, text="Cancel", width=obj_edt_width_buttons,
                                   command=obj_edt_wd.destroy)
    obj_edt_cancel_button.grid(row=0, column=3, padx=obj_edt_pad, pady=obj_edt_pad, stick="w")

    global obj_edt_obj_name_opt_menu

    def obj_edt_obj_name_opt_menu():
        # Options Menu For all existing Objects
        conn = sqlite3.connect(database)
        c = conn.cursor()

        c.execute(f"""SELECT obj_name FROM objects""")
        obj_new_obj_name_list_raw = c.fetchall()
        obj_new_obj_name_list = id.raw_conv(obj_new_obj_name_list_raw)

        if obj_new_obj_name_list:
            global obj_edt_obj_name_var
            obj_edt_obj_name_var = StringVar()
            obj_edt_obj_name_var.set(obj_new_obj_name_list[0])
            obj_edt_obj_name_opt_menu_var = OptionMenu(obj_edt_info_frame_0, obj_edt_obj_name_var,
                                                       *obj_new_obj_name_list)
            obj_edt_obj_name_opt_menu_var.config(width=obj_edt_width + 1)
            obj_edt_obj_name_opt_menu_var.grid(row=0, column=1, pady=obj_edt_pad, padx=obj_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Objects were Found")
            obj_edt_wd.destroy()

        conn.commit()
        conn.close()

    obj_edt_obj_name_opt_menu()

    obj_edt_wd.mainloop()


