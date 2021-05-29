from tkinter import *
from tkinter import ttk

# Scroll Bar stuff
button_main_frame_1 = Frame(tab_id)
button_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
button_canvas = Canvas(button_main_frame_1)

# Create ScrollBar
button_y_scrollbar = Scrollbar(button_main_frame_1, orient="vertical", command=button_canvas.yview)
button_y_scrollbar.pack(side="right", fill="y")
button_x_scrollbar = Scrollbar(button_main_frame_1, orient="horizontal", command=button_canvas.xview)
button_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
button_main_frame_2 = Frame(button_canvas)
button_main_frame_2.bind("<Configure>", lambda e: button_canvas.configure(scrollregion=button_canvas.bbox("all")))

# Canvas Config
button_canvas.create_window((0, 0), window=button_main_frame_2, anchor="nw")
button_canvas.configure(yscrollcommand=button_y_scrollbar.set)
button_canvas.configure(xscrollcommand=button_x_scrollbar.set)
button_canvas.pack(side="left", fill="both", expand=True)
