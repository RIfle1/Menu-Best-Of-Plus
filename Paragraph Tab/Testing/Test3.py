# Scroll Bar stuff
obj_main_error_frame_1 = Frame(test_main_error_frame, height=window_x - test_main_frame_height)
obj_main_error_frame_1.pack(fill="both", expand=True)

# Create Canvas
obj_canvas = Canvas(obj_main_error_frame_1)

# Create ScrollBar
obj_scrollbar = Scrollbar(obj_main_error_frame_1, orient="vertical", command=obj_canvas.yview)
obj_scrollbar.pack(side="right", fill="y")

# Frame To Put Objects in
obj_main_error_frame_2 = Frame(obj_canvas, height=window_x - test_main_frame_height)
obj_main_error_frame_2.bind("<Configure>", lambda e: obj_canvas.configure(scrollregion=obj_canvas.bbox("all")))

# Canvas Config
obj_canvas.create_window((0, 0), window=obj_main_error_frame_2, anchor="nw")
obj_canvas.configure(yscrollcommand=obj_scrollbar.set)
obj_canvas.pack(side="left", fill="both", expand=True)