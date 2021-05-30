from tkinter import *
from tkinter import ttk

# Scroll Bar stuff
ch_scroll_bar_frame = Frame(tab_id)
ch_scroll_bar_frame.pack(fill="both", expand=True)

# Create Canvas
ch_canvas = Canvas(ch_scroll_bar_frame)

# Create ScrollBar
ch_button_y_scrollbar = Scrollbar(ch_scroll_bar_frame, orient="vertical", command=ch_canvas.yview)
ch_button_y_scrollbar.pack(side="right", fill="y")
ch_button_x_scrollbar = Scrollbar(ch_scroll_bar_frame, orient="horizontal", command=ch_canvas.xview)
ch_button_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
inside_character_frame = Frame(ch_canvas)
inside_character_frame.bind("<Configure>", lambda e: ch_canvas.configure(scrollregion=ch_canvas.bbox("all")))

# Canvas Config
ch_canvas.create_window((0, 0), window=inside_character_frame, anchor="nw")
ch_canvas.configure(yscrollcommand=ch_button_y_scrollbar.set)
ch_canvas.configure(xscrollcommand=ch_button_x_scrollbar.set)
ch_canvas.pack(side="left", fill="both", expand=True)


# Scroll Bar stuff
ch_scroll_bar_frame = Frame(main_character_frame)
ch_scroll_bar_frame.pack(fill="both", expand=True)

# Create Canvas
global ch_canvas
ch_canvas = Canvas(ch_scroll_bar_frame, height=600)

# Create ScrollBar
ch_button_x_scrollbar = Scrollbar(ch_scroll_bar_frame, orient="horizontal", command=ch_canvas.xview)
ch_button_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
inside_character_frame = Frame(ch_canvas)
inside_character_frame.bind("<Configure>", lambda e: ch_canvas.configure(scrollregion=ch_canvas.bbox("all")))

# Canvas Config
ch_canvas.create_window((0, 0), window=inside_character_frame, anchor="nw")
ch_canvas.configure(xscrollcommand=ch_button_x_scrollbar.set)
ch_canvas.pack(side="left", fill="both", expand=True)


