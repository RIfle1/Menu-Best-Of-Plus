def p_edt_save_object():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    p_edt_s_id = p_edt_s_id_variable.get()
    p_edt_p_id = p_edt_p_id_variable.get()

    p_edt_obj_name = p_edt_obj_name_variable.get()

    # Get obj_id with obj_name
    if p_edt_obj_name != 'None':
        c.execute(f"""SELECT obj_id FROM objects where obj_name = '{p_edt_obj_name}'""")
        p_edt_obj_id_raw = c.fetchall()
        p_edt_obj_id = id.raw_conv(p_edt_obj_id_raw)[0]
    else:
        p_edt_obj_id = 'None'

    c.execute(f"""SELECT end_bool FROM paragraphs_list WHERE pl_id = '{p_edt_p_id}'""")
    p_edt_end_bool_raw = c.fetchall()
    p_edt_end_bool = id.raw_conv(p_edt_end_bool_raw)[0]

    if p_edt_end_bool == 0:
        c.execute("""UPDATE paragraphs_list SET obj_id = :obj_id WHERE pl_id = :pl_id""",
                          {
                              "pl_id": f'{p_edt_p_id}',
                              "obj_id": f"{p_edt_obj_id}"
                          })

        # Show Success pop-up
        messagebox.showinfo("Success", f"Paragraph Number {id.id_int(p_edt_p_id)} in Story Number {id.id_int(p_edt_s_id)} has been assigned {p_edt_obj_name} as a drop item.")
    else:
        messagebox.showerror("Cannot Perform Action", f"Paragraph Number {id.id_int(p_edt_p_id)} is set to an ending "
                                                      f"paragraph, therefore it cannot have any drops assigned to "
                                                      f"it.\nYou can change that by setting 'Ending Paragraph' To "
                                                      f"'False'.")

    conn.commit()










def p_edt_obj_name_opt_menu():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get obj_name's
    c.execute(f"""SELECT obj_name FROM objects""")
    p_edt_obj_name_list_raw = c.fetchall()
    p_edt_obj_name_list = id.raw_conv(p_edt_obj_name_list_raw)

    global p_edt_obj_name_variable
    p_edt_obj_name_variable = StringVar()
    p_edt_obj_name_list.append('None')
    p_edt_mst_name_opt_menu_var = ttk.OptionMenu(p_edt_select_object_frame_1, p_edt_obj_name_variable,
                                                 p_edt_obj_name_list[-1], *p_edt_obj_name_list)
    p_edt_mst_name_opt_menu_var.configure(width=p_edt_option_width)
    p_edt_mst_name_opt_menu_var.grid(row=0, column=1, pady=p_edt_pad, padx=p_edt_pad, stick="ew")

    if not p_edt_obj_name_list:
        messagebox.showerror("Index Error", "No Existing Objects Found")

    conn.commit()



def c_edt_assign_object_save():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    # Get Object's Name
    c_edt_obj_name = c_edt_obj_name_variable.get()

    # Get c_id
    c_edt_c_id = c_edt_c_id_variable.get()

    c_edt_c_id_from = id.decoder_2(c_edt_c_id)[1]

    if c_edt_c_id_from != 'IP':
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
            messagebox.showinfo("Success", f"Choice Number {c_ed_c_id_num} In Paragraph Number {c_ed_p_id_num} Has Been Assigned Object '{c_edt_obj_name}' As A Condition.")

        else:
            c.execute(f"""UPDATE choices SET obj_id = 'None' WHERE c_id = '{c_edt_c_id}'""")
            messagebox.showinfo("Success",
                                f"Choice Number {c_ed_c_id_num} Condition In Paragraph Number {c_ed_p_id_num} Has Been Removed.")
    else:
        messagebox.showerror("Error", f"Initial Paragraph Choices Cannot Have Conditions.")

    conn.commit()