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


class ChoiceWindow:
    import sqlite3

    def __init__(self):
        # Create New Window
        self.new_choice = Toplevel()
        self.new_choice.title("Create A new Choice")
        self.screen_x_2 = self.new_choice.winfo_screenwidth()
        self.screen_y_2 = self.new_choice.winfo_screenheight()
        self.window_x_2 = 505
        self.window_y_2 = 800
        self.new_choice.minsize(self.window_x_2, self.window_y_2)
        self.new_choice.maxsize(self.window_x_2, self.window_y_2)
        self.pos_x_2 = int((self.screen_x_2 - self.window_x_2) / 2)
        self.pos_y_2 = int((self.screen_y_2 - self.window_y_2) / 2)
        self.new_choice.geometry(f"{self.window_x_2}x{self.window_y_2}+{self.pos_x_2}+{self.pos_y_2}")

        self.frame_height = 200
        self.rest = self.window_y_2 - self.frame_height*2
        # Info Frame 1
        self.info_frame_1 = LabelFrame(self.new_choice, width=self.window_x_2, height=self.frame_height)
        self.info_frame_1.pack(fill="both", side=TOP)

        # Info Frame 2
        self.info_frame_2 = LabelFrame(self.new_choice, width=self.window_x_2, height=self.frame_height)
        self.info_frame_2.pack(fill="both", side=TOP, expand=True)

        # Top Button Frame
        self.button_frame_1 = LabelFrame(self.new_choice, height=self.rest / 2, width=self.window_x_2)
        self.button_frame_1.pack(fill="both")

        # Choice Frame
        self.choice_frame = LabelFrame(self.new_choice, width=self.window_x_2, height=self.frame_height)
        self.choice_frame.pack(fill="both")

        # Bottom Buttons Frame
        self.button_frame_2 = LabelFrame(self.new_choice, height=self.rest / 2, width=self.window_x_2)
        self.button_frame_2.pack(fill="both", side=BOTTOM)

        self.width = 42
        self.pad = 10
        # Labels
        self.get_story_id_label = Label(self.info_frame_1, text="Select Story ID:", width=int(self.width / 2), anchor=NW)
        self.get_story_id_label.grid(row=0, column=0, padx=self.pad, pady=self.pad, stick="nw")

        self.get_pg_id_label = Label(self.info_frame_1, text="Select Paragraph ID:", width=int(self.width / 2), anchor=NW)
        self.get_pg_id_label.grid(row=1, column=0, padx=self.pad, pady=self.pad, stick="nw")

        self.paragraph_text_label = Label(self.info_frame_2, text="Paragraph Text:", width=int(self.width / 2), anchor=NW)
        self.paragraph_text_label.grid(row=2, column=0, padx=self.pad, pady=self.pad, stick="nw")

        self.get_choice_id_label = Label(self.choice_frame, text="Enter Choice Number:", width=int(self.width / 2), anchor=NW)
        self.get_choice_id_label.grid(row=0, column=0, padx=self.pad, pady=self.pad, stick="nw")

        self.choice_text_label = Label(self.choice_frame, text="Choice Text:", width=int(self.width / 2), anchor=NW)
        self.choice_text_label.grid(row=1, column=0, padx=self.pad, pady=self.pad, stick="nw")

        # Entries
        self.get_choice_id_entry = Entry(self.choice_frame, width=48)
        self.get_choice_id_entry.grid(row=0, column=1, padx=self.pad, pady=self.pad)

        self.choice_text_entry = Text(self.choice_frame, width=37, height=20)
        self.choice_text_entry.grid(row=1, column=1, padx=self.pad, pady=self.pad)

        # Message Box
        self.old_text = StringVar()
        self.show_paragraph_message = Message(self.info_frame_2, textvariable=self.old_text, width=280, anchor=NW)
        self.show_paragraph_message.grid(row=2, column=1, padx=self.pad, pady=self.pad, stick="nw")

        # Buttons
        self.submit_button = Button(self.button_frame_1, text="Submit", width=int(self.width / 2), command=self.insert_paragraph)
        self.submit_button.grid(row=0, column=0, padx=self.pad, pady=self.pad, ipadx=160)

        self.save_choice_button = Button(self.button_frame_2, text="Save Initial Paragraph", width=int(self.width / 2), command=self.save_choice)
        self.save_choice_button.grid(row=2, column=0, padx=self.pad, pady=self.pad, stick="w")

        self.cancel_button = Button(self.button_frame_2, text="Cancel", width=self.width, command=self.new_choice.destroy)
        self.cancel_button.grid(row=2, column=1, padx=self.pad, pady=self.pad, stick="w")

        self.new_choice.mainloop()

    def option_s_id_menu(self):
        # Options Menu For all existing stories
        self.conn = sqlite3.connect("EditorDataV3.db")
        self.c = self.conn.cursor()

        self.c.execute("""SELECT s_id FROM paragraphs UNION SELECT s_id FROM first_paragraphs""")
        self.s_id_list_paragraphs_raw = self.c.fetchall()

        self.s_id_paragraphs_list = []
        for self.tp in self.s_id_list_paragraphs_raw:
            for self.item in self.tp:
                self.s_id_paragraphs_list.append(self.item)

        self.s_id_list = self.s_id_paragraphs_list

        if self.s_id_list:
            global s_id_variable
            self.s_id_variable = StringVar()
            self.s_id_variable.set(self.s_id_list[0])
            self.s_id_opmenu = OptionMenu(self.info_frame_1, self.s_id_variable, *self.s_id_list,
                                              command=self.option_p_id_menu)
            self.s_id_opmenu.config(width=self.width)
            self.s_id_opmenu.grid(row=0, column=1, pady=self.pad, padx=self.pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            self.new_choice.destroy()

        self.conn.commit()
        self.conn.close()

    def option_p_id_menu(self):
        # Options Menu For all existing paragraphs
        self.conn = sqlite3.connect("EditorDataV3.db")
        self.c = self.conn.cursor()

        self.c.execute(f"""SELECT fp_id FROM first_paragraphs WHERE s_id = '{self.s_id_variable.get()}'
            UNION SELECT p_id FROM paragraphs WHERE s_id = '{self.s_id_variable.get()}'
            UNION SELECT fp_id FROM choices WHERE s_id = '{self.s_id_variable.get()}'""")
        self.p_id_list_paragraphs_raw = self.c.fetchall()

        self.p_id_paragraphs_list = []
        for self.tp in self.p_id_list_paragraphs_raw:
            for self.item in self.tp:
                self.p_id_paragraphs_list.append(self.item)

        self.p_id_list = self.p_id_paragraphs_list

        if self.p_id_list:
            global p_id_variable
            self.p_id_variable = StringVar()
            self.p_id_variable.set(self.p_id_list[0])
            self.p_id_opmenu = OptionMenu(self.info_frame_1, self.p_id_variable, *self.p_id_list)
            self.p_id_opmenu.config(width=self.width)
            self.p_id_opmenu.grid(row=1, column=1, pady=self.pad, padx=self.pad, stick="ew")

        else:
            messagebox.showerror("Index Error", "No Existing Stories Found")
            self.new_choice.destroy()

        self.conn.commit()
        self.conn.close()

    def save_choice(self):
        # Create a connection to the database
        self.conn = sqlite3.connect("EditorDataV3.db")
        self.c = self.conn.cursor()

        # Create Table
        self.c.execute("""CREATE TABLE IF NOT EXISTS choices
        (s_id text,
        fp_id text,
        p_id text,
        c_id text,
        c_text text)""")

        # im not gonna explain this stuff 0_o
        self.s_id = self.s_id_variable.get()
        self.fp_id = self.id.fp_id(self.s_id)
        self.p_id = self.p_id_variable.get()
        self.c_id = self.get_choice_id_entry.get()
        self.text_length = len(self.choice_text_entry.get("1.0", "end"))
        self.c.execute(f"""SELECT c_id FROM choices WHERE c_id = '{self.p_id}_{id.c_id(self.c_id)}'""")
        self.c_id_raw = self.c.fetchall()
        self.d_p_id = id.decoder_2(self.p_id)[0]

        # I ran out of brain cells for this
        if f'{self.s_id}' == f'{self.d_p_id}':
            try:
                self.c_id = int(self.c_id)
                if self.text_length != 1:
                    if len(self.c_id_raw) == 0:
                        if self.c_id > 0:
                            # Insert into table if that id does not exist
                            self.c.execute("INSERT INTO choices VALUES (:s_id, :fp_id, :p_id, :c_id, :c_text)",
                                            {
                                                "s_id": f"{self.s_id}",
                                                "fp_id": f"{self.fp_id}",
                                                "p_id": f"{self.p_id}",
                                                "c_id": f"{self.p_id}_{id.id_conv('c_id', self.c_id)}",
                                                "c_text": str(self.choice_text_entry.get("1.0", "end"))
                                            })
                            # Show Success pop-up
                            messagebox.showinfo("Success",
                                                f"Choice Number {self.c_id}\nIn Story Number {self.id.id_int(self.s_id)}\nhas been successfully created.")
                        else:
                            messagebox.showerror("Syntax Error", "Choice ID Must Be Positive")
                    else:
                        messagebox.showerror("Duplication Error", f"Choice Number {self.c_id} Already Exists")
                else:
                    messagebox.showerror("Input Error", "Choice Text Is Empty")

            except ValueError:
                messagebox.showerror("Syntax Error", "Story ID Must Be A Number")
        else:
            messagebox.showerror("ID Error", f"Paragraph's Story ID is {self.d_p_id} but Story ID is {self.s_id}")

        # End Connection
        self.conn.commit()
        self.conn.close()

        # Clear the Text Boxes
        self.get_choice_id_entry.delete(0, END)
        self.choice_text_entry.delete("1.0", "end")

    option_p_id_menu()

    def insert_paragraph(self):
        # Create a connection to the database
        self.conn = self.sqlite3.connect("EditorDataV3.db")
        self.c = self.conn.cursor()

        self.p_id = p_id_variable.get()

        # Fetch Information
        self.c.execute(
            f"""SELECT fp_text FROM first_paragraphs WHERE fp_id='{self.p_id}' UNION SELECT p_text FROM paragraphs WHERE p_id='{self.p_id}'""")
        self.text_raw = self.c.fetchall()
        text_1 = ((self.text_raw[0])[0])

        # Input data into text box
        self.old_text.set(str(text_1))

        # End Connection
        self.conn.commit()
        self.conn.close()


ChoiceWindow.__call__()
