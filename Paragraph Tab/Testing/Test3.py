def p_edt_edit():
    conn = sqlite3.connect(database, uri=True)
    c = conn.cursor()

    p_edt_s_id = p_edt_s_id_variable.get()
    p_edt_p_id = p_edt_p_id_variable.get()

    p_edt_npc_name = p_edt_npc_name_variable.get()
    p_edt_mst_name = p_edt_mst_name_variable.get()

    p_edt_obj_name = p_edt_obj_name_variable.get()

    # Get obj_id with obj_name
    if p_edt_obj_name != 'None' and p_edt_obj_name != 'Previous':
        c.execute(f"""SELECT obj_id FROM objects where obj_name = '{p_edt_obj_name}'""")
        p_edt_obj_id_raw = c.fetchall()
        p_edt_obj_id = id.raw_conv(p_edt_obj_id_raw)[0]
    elif p_edt_obj_name == 'Previous':
        c.execute(f"""SELECT obj_id FROM paragraphs_list where pl_id = '{p_edt_p_id}'""")
        p_edt_obj_id_raw = c.fetchall()
        p_edt_obj_id = id.raw_conv(p_edt_obj_id_raw)[0]
        if not p_edt_obj_id:
            p_edt_obj_id = 'None'
    else:
        p_edt_obj_id = 'None'

    # Check to see if an npc or mst has been assigned
    if p_edt_npc_name == p_edt_mst_name == 'None' or p_edt_npc_name == p_edt_mst_name == 'Previous':
        messagebox.showerror("Input Error", f'You Must Assign An NPC or Enemy To This Paragraph', icon='warning')
    else:
        if p_edt_npc_name != 'None' and p_edt_mst_name == 'None':
            # Save Paragraph to NPC ID
            if p_edt_npc_name != 'Previous':
                # Get npc_id with npc_name
                c.execute(f"""SELECT npc_id FROM npcs WHERE npc_name = '{p_edt_npc_name}'""")
                p_edt_npc_id_raw = c.fetchall()
                p_edt_npc_id = id.raw_conv(p_edt_npc_id_raw)[0]
            else:
                # Get previous npc_id with p_id
                c.execute(f"""SELECT npc_id FROM paragraphs_list WHERE pl_id = '{p_edt_p_id}'""")
                p_edt_npc_id_raw = c.fetchall()
                p_edt_npc_id = id.raw_conv(p_edt_npc_id_raw)[0]

            if len(p_edt_paragraph_text_entry.get("1.0", "end")) != 1:
                c.execute("""UPDATE paragraphs_list SET 
                p_text = :p_text,
                npc_id = :npc_id,
                npc_bool = :npc_bool,
                mst_id = :mst_id,
                mst_bool = :mst_bool,
                obj_id = :obj_id 
                WHERE pl_id = :pl_id""",
                          {
                              "p_text": p_edt_paragraph_text_entry.get("1.0", "end"),
                              "pl_id": f'{p_edt_p_id}',
                              "npc_id": f'{p_edt_npc_id}',
                              "npc_bool": 1,
                              "mst_id": 'None',
                              "mst_bool": 0,
                              "obj_id": f"{p_edt_obj_id}"
                          })

                # Show Success pop-up
                messagebox.showinfo("Success",
                                    f"Paragraph Number {id.id_int(p_edt_p_id)} in Story Number {id.id_int(p_edt_s_id)} has been successfully modified.")
            else:
                messagebox.showerror("Input Error", f'Paragraph Text is Empty', icon='warning')

        elif p_edt_mst_name != 'None' and p_edt_npc_name == 'None':
            # Save paragraph to mst_id
            if p_edt_mst_name != 'Previous':
                # Get mst_id with mst_name
                c.execute(f"""SELECT mst_id FROM monsters WHERE mst_name = '{p_edt_mst_name}'""")
                p_edt_mst_id_raw = c.fetchall()
                p_edt_mst_id = id.raw_conv(p_edt_mst_id_raw)[0]
            else:
                # Get previous mst_id with p_id
                c.execute(f"""SELECT mst_id FROM paragraphs_list WHERE pl_id = '{p_edt_p_id}'""")
                p_edt_mst_id_raw = c.fetchall()
                p_edt_mst_id = id.raw_conv(p_edt_mst_id_raw)[0]

            if len(p_edt_paragraph_text_entry.get("1.0", "end")) != 1:
                c.execute("""UPDATE paragraphs_list SET 
                p_text = :p_text,
                mst_id = :mst_id,
                mst_bool = :mst_bool,
                npc_id = :npc_id,
                npc_bool = :npc_bool,
                obj_id = :obj_id 
                WHERE pl_id = :pl_id""",
                          {
                              "p_text": p_edt_paragraph_text_entry.get("1.0", "end"),
                              "pl_id": f'{p_edt_p_id}',
                              "mst_id": f'{p_edt_mst_id}',
                              "mst_bool": 1,
                              "npc_id": 'None',
                              "npc_bool": 0,
                              "obj_id": f"{p_edt_obj_id}"
                          })

                # Show Success pop-up
                messagebox.showinfo("Success",
                                    f"Paragraph Number {id.id_int(p_edt_p_id)} in Story Number {id.id_int(p_edt_s_id)} has been successfully modified.")
            else:
                messagebox.showerror("Input Error", f'Paragraph Text is Empty', icon='warning')
        else:
            messagebox.showerror("Input Error", f'You Cannot Assign An Enemy And An NPC To A Paragraph', icon='warning')

        # Clear the Text Boxes
        p_edt_paragraph_text_entry.delete("1.0", "end")

    conn.commit()

    p_edt_s_id_opt_menu()
    p_edt_p_id_opt_menu()
    p_edt_npc_name_opt_menu()
    p_edt_mst_name_opt_menu()