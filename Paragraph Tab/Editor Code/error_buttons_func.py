# Imports
import sqlite3
from tkinter import *
from tkinter import messagebox

import editor_settings
import id


def p_end_check():
    global database
    database = 'Editor.db'
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()
    # Get s_id list
    c.execute(f"""SELECT s_id from stories""")
    s_id_list_stories_raw = c.fetchall()
    s_id_list_stories = id.raw_conv(s_id_list_stories_raw)

    c.execute(f"""SELECT s_id from paragraphs_list""")
    s_id_list_paragraphs_raw = c.fetchall()
    s_id_list_paragraphs = id.raw_conv(s_id_list_paragraphs_raw)

    warning_list = []

    s_id_with_no_paragraphs = []
    for s_id in s_id_list_stories:
        if s_id not in s_id_list_paragraphs:
            s_id_with_no_paragraphs.append(s_id)

    for s_id in s_id_with_no_paragraphs:
        warning_list.append(f"Story Number {id.id_int(s_id)} Has No Paragraphs Assigned")

    c.execute(f"""SELECT s_id, end_bool FROM paragraphs_list""")
    info_list_raw = c.fetchall()

    s_id_end_count_list = []
    story_list = []
    for x_list in info_list_raw:
        if x_list[0] not in story_list:
            story_list.append(x_list[0])

    for s_id in story_list:
        counter = 0
        for x_list in info_list_raw:
            if s_id in x_list:
                if x_list[1] == 1:
                    counter += 1
        s_id_end_count_list.append([s_id, counter])

    warning_list = []
    for x_list in s_id_end_count_list:
        if x_list[1] == 0:
            warning_list.append(x_list)

    for x_list in warning_list:
        warning_list.append(f"Story Number {id.id_int(x_list[0])} Has No Ending Paragraphs Assigned")
    print(warning_list)

    messagebox.showerror("Error", f"{warning_list}", icon='warning')


p_end_check()


def function_runner():
    p_end_check()
