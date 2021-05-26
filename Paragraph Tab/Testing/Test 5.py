import tkinter as tk
from tkinter import ttk

test_main_error_frame = tk.Tk()
test_main_error_frame_1 = ttk.Frame(test_main_error_frame)
canvas = tk.Canvas(test_main_error_frame_1)
scrollbar = ttk.Scrollbar(test_main_error_frame_1, orient="vertical", command=canvas.yview)
test_main_error_frame_0 = ttk.Frame(canvas)


test_main_error_frame_0.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

canvas.create_window((0, 0), window=test_main_error_frame_0, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

test_main_error_frame_1.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

test_main_error_frame.mainloop()