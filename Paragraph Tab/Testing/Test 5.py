from tkinter import *
from tkinter import ttk

# Scroll Bar stuff
pg_2_main_frame_1 = Frame(tab_id)
pg_2_main_frame_1.pack(fill="both", expand=True)

# Create Canvas
pg_2_canvas = Canvas(pg_2_main_frame_1)

# Create ScrollBar
pg_2_y_scrollbar = Scrollbar(pg_2_main_frame_1, orient="vertical", command=pg_2_canvas.yview)
pg_2_y_scrollbar.pack(side="right", fill="y")
pg_2_x_scrollbar = Scrollbar(pg_2_main_frame_1, orient="horizontal", command=pg_2_canvas.xview)
pg_2_x_scrollbar.pack(side="bottom", fill="x")

# Frame To Put Objects in
pg_2_main_frame_2 = Frame(pg_2_canvas)
pg_2_main_frame_2.bind("<Configure>", lambda e: pg_2_canvas.configure(scrollregion=pg_2_canvas.bbox("all")))

# Canvas Config
pg_2_canvas.create_window((0, 0), window=pg_2_main_frame_2, anchor="nw")
pg_2_canvas.configure(yscrollcommand=pg_2_y_scrollbar.set)
pg_2_canvas.configure(xscrollcommand=pg_2_x_scrollbar.set)
pg_2_canvas.pack(side="left", fill="both", expand=True)
