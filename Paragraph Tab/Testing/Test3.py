# ALL MAIN FRAMES
# MAIN Frame
mst_main_frame_width = int(0.75 * window_x)
mst_main_frame = LabelFrame(monster_tab, width=mst_main_frame_width, height=window_y)
mst_main_frame.pack(fill="both", expand=True)

# Main Buttons Frame
mst_main_frame_height = int(window_y / 4.8)
mst_main_buttons_frame = LabelFrame(mst_main_frame, height=mst_main_frame_height, width=mst_main_frame_width)
mst_main_buttons_frame.pack(fill="both")

# NPC Frame
mst_main_mst_frame = LabelFrame(mst_main_frame, height=window_x - mst_main_frame_height)
mst_main_mst_frame.pack(fill="both", expand=True)

mst_button_width = 22
mst_buttons_width = 30
mst_buttons_height = 1
mst_button_x_space = 2
mst_button_y_space = 4
mst_font_size = 18
# NEW NPC Button
mst_new_mst_button = Button(mst_main_buttons_frame, text="New Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                            pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                            command=character_buttons_func.ch_new_window)
mst_new_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)

# EDIT NPC Button
mst_edit_mst_button = Button(mst_main_buttons_frame, text="Edit Monster Or Enemy", bg="#5fafde", fg="White", padx=mst_buttons_width,
                             pady=mst_buttons_height, font=("Times New Roman", mst_font_size), relief=FLAT, width=mst_button_width,
                             command=character_buttons_func.ch_edt_window)
mst_edit_mst_button.pack(padx=mst_button_x_space, pady=mst_button_y_space)
