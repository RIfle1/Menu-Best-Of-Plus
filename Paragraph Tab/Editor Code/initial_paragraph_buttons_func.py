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


def style_func():
    ip_font_size = 11
    ip_style = ttk.Style()
    ip_style.configure("TMenubutton", background="#c2c2c2", font=('Times New Roman', ip_font_size))
    ip_style.configure("TButton", font=('Times New Roman', ip_font_size))
    ip_style.configure("TLabel", font=('Times New Roman', ip_font_size))


def ip_new_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS initial_paragraphs
    (s_id text, 
    ip_id text,
    ip_text text)""")

    ip_new_s_id = ip_new_ip_id_variable.get()
    ip_new_ip_id = 'IP'
    ip_new_text_length = len(ip_new_paragraph_text_entry.get("1.0", "end"))

    if ip_new_text_length != 1:
        c.execute("INSERT INTO initial_paragraphs VALUES (:s_id, :ip_id, :ip_text)",
                  {
                      "s_id": f"{ip_new_s_id}",
                      "ip_id": f"{ip_new_s_id}_{ip_new_ip_id}",
                      "ip_text": str(ip_new_paragraph_text_entry.get("1.0", "end"))
                  })
        messagebox.showinfo("Success", f"Initial Paragraph of Story {id.id_int(ip_new_s_id)} has been successfully created.")
    else:
        messagebox.showerror("Input Error", "Story Text Is Empty")

    conn.commit()

    ip_new_paragraph_text_entry.delete("1.0", "end")
    ip_new_show_story_message.delete("1.0", "end")
    ip_new_s_id_opt_menu()


def ip_new_insert():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ip_new_s_id = ip_new_ip_id_variable.get()

    c.execute(f"""SELECT s_text FROM stories WHERE s_id='{ip_new_s_id}'""")
    ip_new_text_raw = c.fetchall()
    ip_new_text = ((ip_new_text_raw[0])[0])

    ip_new_show_story_message.delete("1.0", "end")
    ip_new_show_story_message.insert(END, str(ip_new_text))

    conn.commit()


def ip_new_window():
    global ip_new_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    ip_new_wd = Toplevel()
    ip_new_wd.title("Create An Initial Paragraph")
    screen_x_2 = ip_new_wd.winfo_screenwidth()
    screen_y_2 = ip_new_wd.winfo_screenheight()
    window_x_2 = 505
    window_y_2 = 850
    ip_new_wd.minsize(window_x_2, window_y_2)
    ip_new_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    ip_new_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    ip_new_frame_height = 200
    ip_new_rest = window_y_2 - ip_new_frame_height*2
    # Info Frame 1
    ip_new_info_frame_1 = LabelFrame(ip_new_wd, width=window_x_2, height=ip_new_frame_height)
    ip_new_info_frame_1.pack(fill="both", side=TOP)

    # Top Button Frame
    ip_new_button_frame_1 = LabelFrame(ip_new_wd, height=ip_new_rest / 2, width=window_x_2)
    ip_new_button_frame_1.pack(fill="both")

    # Entry Frame
    ip_new_entry_frame = LabelFrame(ip_new_wd, width=window_x_2, height=ip_new_frame_height)
    ip_new_entry_frame.pack(fill="both")

    # Bottom Buttons Frame
    ip_new_button_frame_2 = LabelFrame(ip_new_wd, height=ip_new_rest / 2, width=window_x_2)
    ip_new_button_frame_2.pack(fill="both", side=BOTTOM)

    ip_new_width = 42
    ip_new_pad = 10

    # Labels
    ip_new_get_story_id_label = ttk.Label(ip_new_info_frame_1, text="Story Number ID:", width=int(ip_new_width / 2), anchor=W)
    ip_new_get_story_id_label.grid(row=0, column=0, padx=(ip_new_pad, 11), pady=ip_new_pad, stick="w")

    ip_new_story_text_label = ttk.Label(ip_new_info_frame_1, text="Story Text:", width=int(ip_new_width / 2), anchor=NW)
    ip_new_story_text_label.grid(row=1, column=0, padx=(ip_new_pad, 13), pady=ip_new_pad, stick="nw")

    ip_new_paragraph_text_label = ttk.Label(ip_new_entry_frame, text="Initial Paragraph Text:", width=int(ip_new_width / 2), anchor=NW)
    ip_new_paragraph_text_label.grid(row=0, column=0, padx=(ip_new_pad, 13), pady=ip_new_pad, stick="nw")

    # Entries
    global ip_new_paragraph_text_entry, ip_new_show_story_message
    ip_new_paragraph_text_entry = Text(ip_new_entry_frame, width=37, height=20)
    ip_new_paragraph_text_entry.grid(row=0, column=1, padx=ip_new_pad, pady=ip_new_pad)

    # Message Box
    global ip_new_show_story_message
    ip_new_show_story_message = Text(ip_new_info_frame_1, width=37, height=20)
    ip_new_show_story_message.bind("<Key>", lambda a: "break")
    ip_new_show_story_message.grid(row=1, column=1, padx=ip_new_pad, pady=ip_new_pad, stick="w")

    # Buttons
    ip_new_submit_button = ttk.Button(ip_new_button_frame_1, text="Submit", width=int(ip_new_width / 2), command=ip_new_insert)
    ip_new_submit_button.grid(row=0, column=0, padx=ip_new_pad, pady=ip_new_pad, ipadx=160)

    ip_new_save_story_button = ttk.Button(ip_new_button_frame_2, text="Save Initial Paragraph", width=int(ip_new_width / 2), command=ip_new_save)
    ip_new_save_story_button.grid(row=2, column=0, padx=ip_new_pad, pady=ip_new_pad, stick="w")

    ip_new_cancel_button = ttk.Button(ip_new_button_frame_2, text="Cancel", width=ip_new_width, command=ip_new_wd.destroy)
    ip_new_cancel_button.grid(row=2, column=1, padx=ip_new_pad, pady=ip_new_pad, stick="w")
    global ip_new_s_id_opt_menu

    def ip_new_s_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT s_id FROM stories ORDER BY s_id""")
        ip_new_s_id_list_stories_raw = c.fetchall()
        ip_new_s_id_stories_list = []
        for tp in ip_new_s_id_list_stories_raw:
            for item in tp:
                ip_new_s_id_stories_list.append(item)

        c.execute("""SELECT s_id FROM initial_paragraphs ORDER BY s_id""")
        s_id_list_int_pg_raw = c.fetchall()
        s_id_int_pg_list = []
        for tp in s_id_list_int_pg_raw:
            for item in tp:
                s_id_int_pg_list.append(item)

        for item in s_id_int_pg_list:
            ip_new_s_id_stories_list.remove(item)

        s_id_list = ip_new_s_id_stories_list

        if s_id_list:
            global ip_new_ip_id_variable
            ip_new_ip_id_variable = StringVar()
            ip_new_s_id_opt_menu_var = ttk.OptionMenu(ip_new_info_frame_1, ip_new_ip_id_variable, s_id_list[0], *s_id_list)
            ip_new_s_id_opt_menu_var.grid(row=0, column=1, pady=ip_new_pad, padx=ip_new_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            ip_new_wd.destroy()

        conn.commit()

    ip_new_s_id_opt_menu()

    style_func()

    ip_new_wd.mainloop()


# Function to edit stories
def ip_edt_edit():
    # Create a connection to the database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get id's
    ip_edt_ip_id = ip_edt_ip_id_variable.get()
    ip_edt_s_id = id.id_int(id.decoder_2(ip_edt_ip_id)[-2])

    ip_edt_text_length = len(ip_edt_ip_text_entry.get("1.0", "end"))

    # Update Table
    if ip_edt_text_length != 1:
        c.execute("""UPDATE initial_paragraphs SET ip_text = :ip_text WHERE ip_id = :ip_id""",
                  {
                      "ip_text": ip_edt_ip_text_entry.get("1.0", "end"),
                      "ip_id": f'{ip_edt_ip_id}'
                  })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Initial Paragraph in Story Number {ip_edt_s_id} has been successfully modified.")
    else:
        messagebox.showerror("Input Error", f'Initial Paragraph Text is Empty', icon='warning')

    # Clear the Text Boxes
    ip_edt_ip_text_entry.delete("1.0", "end")

    conn.commit()

    ip_edt_ip_id_opt_menu()


# Function to insert already written text
def ip_edt_insert():
    # Delete Previous Input
    ip_edt_ip_text_entry.delete("1.0", "end")

    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    ip_edt_ip_id = ip_edt_ip_id_variable.get()

    c.execute(f"""SELECT ip_text FROM initial_paragraphs WHERE ip_id = '{ip_edt_ip_id}'""")
    ip_edt_text_raw = c.fetchall()
    ip_edt_text = ((ip_edt_text_raw[0])[0])

    # Input data into text box
    ip_edt_ip_text_entry.insert(END, f'{ip_edt_text}')

    conn.commit()


# Function to insert decoded id
def ip_edt_decode_id():
    ip_edt_decode_id_text.delete("1.0", "end")
    ip_edt_decode_id_text.insert(END, id.decoder_3(ip_edt_ip_id_variable.get()))


# Function to delete a story from the delete window
def ip_del_delete():
    # Create connection to retrieve data
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()
    ip_del_ip_id = ip_edt_ip_id_variable.get()
    ip_del_s_id = id.id_int(id.decoder_2(ip_del_ip_id)[-2])

    ip_del_warning = messagebox.askquestion('Confirm Deletion', f'Are you sure you want to delete the Initial Paragraph In Story Number {ip_del_s_id}?', icon='warning')

    if ip_del_warning == 'yes':
        c.execute(f"""DELETE FROM initial_paragraphs WHERE ip_id = '{ip_del_ip_id}'""")
        c.execute(f"""DELETE FROM paragraphs_list WHERE s_id = '{id.conv('s_id', id.id_int(ip_del_ip_id))}'""")
        c.execute(f"""DELETE FROM choices WHERE s_id = '{id.conv('s_id', id.id_int(ip_del_ip_id))}'""")

        # Show Success pop-up
        messagebox.showinfo("Success", f"The Initial Paragraph Number In Story Number {ip_del_s_id}\nhas been successfully deleted."
                                       f"\nAll Paragraphs And Choices Were Also Deleted From Story Number {ip_del_s_id}.")
        ip_edt_ip_text_entry.delete("1.0", "end")
        ip_edt_decode_id_text.delete("1.0", "end")

    conn.commit()

    ip_edt_ip_id_opt_menu()


# Function to open edit window
def ip_edt_window():
    global ip_edt_wd, database
    database = editor_settings.database_module.database
    # Create New Window
    ip_edt_wd = Toplevel()
    ip_edt_wd.title("Edit Initial Paragraph")
    screen_x_2 = ip_edt_wd.winfo_screenwidth()
    screen_y_2 = ip_edt_wd.winfo_screenheight()
    window_x_2 = 510
    window_y_2 = 641
    ip_edt_wd.minsize(window_x_2, window_y_2)
    ip_edt_wd.maxsize(window_x_2, window_y_2)
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    ip_edt_wd.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    ip_edt_frame_height = 400
    ip_edt_info_frame_height = 57

    # Top Frame
    ip_edt_top_frame = LabelFrame(ip_edt_wd, height=ip_edt_info_frame_height, width=window_x_2)
    ip_edt_top_frame.pack(fill="both")

    # Info Frame 1
    ip_edt_info_frame_1 = Frame(ip_edt_top_frame, height=ip_edt_info_frame_height, width=window_x_2)
    ip_edt_info_frame_1.pack(fill="both")

    # Info Frame 2
    ip_edt_info_frame_2 = Frame(ip_edt_top_frame, height=ip_edt_info_frame_height, width=window_x_2)
    ip_edt_info_frame_2.pack(fill="both")

    # Bottom Frame
    ip_edt_bottom_frame = LabelFrame(ip_edt_wd, height=ip_edt_info_frame_height, width=window_x_2)
    ip_edt_bottom_frame.pack(fill="both")

    # Info Frame 3
    ip_edt_info_frame_3 = Frame(ip_edt_bottom_frame, height=ip_edt_frame_height, width=window_x_2)
    ip_edt_info_frame_3.pack(fill="both")

    # Buttons Frame 1
    ip_edt_button_frame_1 = Frame(ip_edt_bottom_frame, height=window_y_2 - ip_edt_frame_height, width=window_x_2)
    ip_edt_button_frame_1.pack(fill="both")

    # Buttons Frame 2
    ip_edt_button_frame_2 = Frame(ip_edt_bottom_frame, height=window_y_2 - ip_edt_frame_height, width=window_x_2)
    ip_edt_button_frame_2.pack(fill="both")

    ip_edt_entry_width = 37
    ip_edt_width = 23
    ip_edt_pad = 10

    # Labels
    ip_edt_ip_id_label = ttk.Label(ip_edt_info_frame_1, text="Select Initial Paragraph ID:", width=ip_edt_width, anchor=W)
    ip_edt_ip_id_label.grid(row=0, column=0, padx=ip_edt_pad, pady=ip_edt_pad, stick="w")

    ip_edt_decode_id_label_text = ttk.Label(ip_edt_info_frame_1, text="Decoded ID:", width=ip_edt_width, anchor=NW)
    ip_edt_decode_id_label_text.grid(row=1, column=0, padx=ip_edt_pad, pady=ip_edt_pad, stick="nw")

    ip_edt_edit_ip_label = ttk.Label(ip_edt_info_frame_3, text="Edit Initial Paragraph:", width=ip_edt_width, anchor=NW)
    ip_edt_edit_ip_label.grid(row=0, column=0, padx=ip_edt_pad, pady=ip_edt_pad, stick="nw")

    # Decode ID Message
    global ip_edt_decode_id_text
    ip_edt_decode_id_text = Text(ip_edt_info_frame_1, width=ip_edt_entry_width, height=5)
    ip_edt_decode_id_text.bind("<Key>", lambda a: "break")
    ip_edt_decode_id_text.grid(row=1, column=1, padx=ip_edt_pad, pady=ip_edt_pad, stick="w")

    # Text Entry
    global ip_edt_ip_text_entry
    ip_edt_ip_text_entry = Text(ip_edt_info_frame_3, width=ip_edt_entry_width, height=20)
    ip_edt_ip_text_entry.grid(row=0, column=1, padx=ip_edt_pad, pady=ip_edt_pad, stick="w")

    # Buttons
    ip_edt_submit_id_button = ttk.Button(ip_edt_info_frame_2, text="Decode ID", width=ip_edt_width, command=ip_edt_decode_id)
    ip_edt_submit_id_button.grid(row=0, column=0, padx=ip_edt_pad, pady=ip_edt_pad, stick="w", ipadx=157)

    ip_edt_width_buttons = 19
    ip_edt_save_story_button = ttk.Button(ip_edt_button_frame_1, text="Save Changes", width=ip_edt_width_buttons,
                                     command=ip_edt_edit)
    ip_edt_save_story_button.grid(row=0, column=0, padx=(ip_edt_pad, ip_edt_pad+8), pady=ip_edt_pad, stick="w")

    ip_edt_load_text_button = ttk.Button(ip_edt_button_frame_1, text="Load Paragraph", width=ip_edt_width_buttons,
                                    command=ip_edt_insert)
    ip_edt_load_text_button.grid(row=0, column=1, padx=(ip_edt_pad, ip_edt_pad+7), pady=ip_edt_pad, stick="w")

    ip_edt_delete_text_button = ttk.Button(ip_edt_button_frame_1, text="Delete Paragraph", width=ip_edt_width_buttons,
                                      command=ip_del_delete)
    ip_edt_delete_text_button.grid(row=0, column=2, padx=ip_edt_pad, pady=ip_edt_pad, stick="w")

    ip_edt_cancel_button = ttk.Button(ip_edt_button_frame_2, text="Cancel", width=ip_edt_width,
                                 command=ip_edt_wd.destroy)
    ip_edt_cancel_button.grid(row=0, column=3, padx=ip_edt_pad, pady=ip_edt_pad, stick="w", ipadx=157)

    global ip_edt_ip_id_opt_menu

    def ip_edt_ip_id_opt_menu():
        # Options Menu For all existing stories
        conn = sqlite3.connect(database, uri=True)
        c = conn.cursor()

        c.execute("""SELECT ip_id FROM initial_paragraphs ORDER BY ip_id""")
        ip_new_ip_id_list_raw = c.fetchall()
        ip_new_ip_id_list = []
        for tp in ip_new_ip_id_list_raw:
            for item in tp:
                ip_new_ip_id_list.append(item)

        if ip_new_ip_id_list:
            global ip_edt_ip_id_variable
            ip_edt_ip_id_variable = StringVar()
            ip_edt_ip_id_opt_menu_var = ttk.OptionMenu(ip_edt_info_frame_1, ip_edt_ip_id_variable, ip_new_ip_id_list[0], *ip_new_ip_id_list)
            ip_edt_ip_id_opt_menu_var.grid(row=0, column=1, padx=ip_edt_pad, pady=ip_edt_pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Initial Paragraphs Found")
            ip_edt_wd.destroy()

        conn.commit()

    ip_edt_ip_id_opt_menu()

    style_func()

    ip_edt_wd.mainloop()
