# Imports
import sqlite3
from tkinter import *
from tkinter import messagebox
import editor_settings
import id
import sys

error_counter = sys.modules[__name__]

error_counter.errors = 0


def paragraphs_checker():
    global database
    database = editor_settings.database_module.database
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
        warning_list.append(f"Story Number {id.id_int(s_id)} Has No Paragraphs And No Ending Paragraphs Assigned\n")
        error_counter.errors += 1

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

    warning_s_id_list = []
    for x_list in s_id_end_count_list:
        if x_list[1] == 0:
            warning_s_id_list.append(x_list)

    for x_list in warning_s_id_list:
        warning_list.append(f"Story Number {id.id_int(x_list[0])} Has No Ending Paragraphs Assigned\n")
        error_counter.errors += 1

    c.execute(f"""SELECT pl_id, npc_bool, mst_bool FROM paragraphs_list""")
    p_info_list_raw = c.fetchall()

    p_errors_list = []
    for info in p_info_list_raw:
        if info[1] == 0 and info[2] == 0:
            p_errors_list.append(info[0])

    for p_id in p_errors_list:
        warning_list.append(f"{id.decoder_3(p_id)} Has No NPC or Enemy Assigned\n")
        error_counter.errors += 1

    warning_text = ''

    for text in warning_list:
        warning_text += f'{text}\n'
    warning_text += '###'

    errors_file = open("errors.txt", "a")
    errors_file.write(warning_text)
    errors_file.close()

    conn.commit()


def npc_enemy_checker():
    global database
    database = editor_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    warning_list = []

    c.execute(f"""SELECT npc_id FROM npcs EXCEPT SELECT npc_id FROM paragraphs_list""")
    npc_id_list_raw = c.fetchall()
    npc_id_list = id.raw_conv(npc_id_list_raw)

    npc_name_list = []
    for npc_id in npc_id_list:
        c.execute(f"""SELECT npc_name FROM npcs WHERE npc_id = '{npc_id}'""")
        npc_name_raw = c.fetchall()
        npc_name = id.raw_conv(npc_name_raw)[0]
        npc_name_list.append(npc_name)

    for npc_name in npc_name_list:
        warning_list.append(f"NPC '{npc_name}' Has No Assigned Paragraph\n")
        error_counter.errors += 1

    c.execute(f"""SELECT mst_id FROM monsters EXCEPT SELECT mst_id FROM paragraphs_list""")
    mst_id_list_raw = c.fetchall()
    mst_id_list = id.raw_conv(mst_id_list_raw)

    mst_name_list = []
    for mst_id in mst_id_list:
        c.execute(f"""SELECT mst_name FROM monsters WHERE mst_id = '{mst_id}'""")
        mst_name_raw = c.fetchall()
        mst_name = id.raw_conv(mst_name_raw)[0]
        mst_name_list.append(mst_name)

    for mst_name in mst_name_list:
        warning_list.append(f"Enemy '{mst_name}' Has No Assigned Paragraph\n")
        error_counter.errors += 1

    warning_text = ''

    for text in warning_list:
        warning_text += f'{text}\n'
    warning_text += '###'

    errors_file = open("errors.txt", "a")
    errors_file.write(warning_text)
    errors_file.close()

    conn.commit()


def objects_checker():
    global database
    database = editor_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    warning_list = []

    c.execute(f"""SELECT obj_id from objects EXCEPT SELECT obj_id FROM paragraphs_list""")
    obj_id_list_raw = c.fetchall()
    obj_id_list = id.raw_conv(obj_id_list_raw)

    obj_name_list = []
    for obj_id in obj_id_list:
        c.execute(f"""SELECT obj_name from objects WHERE obj_id = '{obj_id}'""")
        obj_name_raw = c.fetchall()
        obj_name = id.raw_conv(obj_name_raw)[0]
        obj_name_list.append(obj_name)

    for obj_name in obj_name_list:
        warning_list.append(f"Object '{obj_name}' Has No Assigned Paragraph\n")
        error_counter.errors += 1

    warning_text = ''

    for text in warning_list:
        warning_text += f'{text}\n'
    warning_text += '###'

    errors_file = open("errors.txt", "a")
    errors_file.write(warning_text)
    errors_file.close()

    conn.commit()


def choice_checker():
    global database
    database = editor_settings.database_module.database
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    warning_list = []

    c.execute(f"""SELECT c_id FROM choices""")
    c_id_list_raw = c.fetchall()
    c_id_list = id.raw_conv(c_id_list_raw)

    c_id_error_list = []
    for c_id in c_id_list:
        ending = id.id_str(id.decoder_2(c_id)[-1])
        if ending == 'C':
            c_id_error_list.append(c_id)

    for c_id in c_id_error_list:
        warning_list.append(f"{id.decoder_3(c_id)} Has No Assigned Paragraph\n")
        error_counter.errors += 1

    warning_text = ''

    for text in warning_list:
        warning_text += f'{text}\n'
    warning_text += '###'

    errors_file = open("errors.txt", "a")
    errors_file.write(warning_text)
    errors_file.close()

    conn.commit()


def update():
    return error_counter.errors


def function_runner():
    # Delete Previous Errors in file
    errors_file = open("errors.txt", "w")
    errors_file.truncate(0)
    errors_file.close()
    # Call Error Checking Functions
    paragraphs_checker()
    npc_enemy_checker()
    objects_checker()
    choice_checker()

    # Update the number of errors
    update()

    # Show Message With Number of Errors
    messagebox.showinfo("Errors", f"Your Game Editor Has {error_counter.errors} Errors.\nRefresh In Options To View Errors")

    # Reset Number of errors
    error_counter.errors = 0


