from tkinter import *

test_main_error_frame = Tk()

# Tkinter widgets needed for scrolling.  The only native scrollable container that Tkinter provides is a canvas.
# A Frame is needed inside the Canvas so that widgets can be added to the Frame and the Canvas makes it scrollable.

canvas = Canvas(test_main_error_frame)
test_main_error_frame_0 = Frame(canvas)
ScrollBar = Scrollbar(test_main_error_frame)

# Sets up the Canvas, Frame, and scrollbars for scrolling

canvas.config(yscrollcommand=ScrollBar.set, highlightthickness=0)
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)
canvas.create_window(0, 0, window=test_main_error_frame_0, anchor=NW)

ScrollBar.config(orient=VERTICAL, command=canvas.yview)
ScrollBar.pack(fill=Y, side=RIGHT, expand=FALSE)


def errors_print():
    padding = 10
    errors_file = open("errors.txt", "r")
    text = errors_file.read()
    errors_list = text.split('###')

    for errors in errors_list[0:-1]:
        error_frame = LabelFrame(test_main_error_frame_0, height=100)
        error_frame.pack()
        error_message = Message(error_frame, text=errors, width=400)
        error_message.grid(column=0, row=0, padx=padding, pady=(padding, 0))

    # Update the scroll region after new widgets are added
    canvas.update_idletasks()
    canvas.config(scrollregion=test_main_error_frame_0.bbox())


button = Button(test_main_error_frame, text="press me", command=errors_print)
button.pack()

test_main_error_frame.mainloop()
