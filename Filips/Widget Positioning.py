import tkinter
from tkinter import *

app = Tk()
app.title("Widget Positioning")
screen_x = app.winfo_screenwidth()
screen_y = app.winfo_screenheight()
window_x = 1200
window_y = 800
pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)
app.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# Frame Widget

"""mainframe = tkinter.LabelFrame(app, text="Frame1", width=300, height=200, borderwidth=1)
mainframe.grid()"""

# How to change the position of a widget -> default side="top" with .pack()
# side="<top>" or "<bottom>"
# expand=<int>
# fill="both" or "y" or "x"
# padx="<int>" or pady="<int>" to move it by a certain amount of pixels from the left and the top
# ipadx="<int>" or ipady="<int>" to expand the button itself by a certain amount of pixels from the left and the top

# How to change the position of a widget with .grid()
# row=<int>, column=<int>
# rowspawn=<int>, columnspawn=<int>
# padx="<int>" or pady="<int>" to move it by a certain amount of pixels from the left and the top
# ipadx="<int>" or ipady="<int>" to expand the button itself by a certain amount of pixels from the left and the top
# stick="<>" north = n , east = e , south= s , west = w -> change the position of a button inside of it's grid

# How to change the position of a widget with .place()
# x=<int>, y=<int> position of the pixel is the top left of the widget
btn = tkinter.Button(app, text="Button", width=6, height=1)
btn.place(x=50, y=0)
btn2 = tkinter.Button(app, text="Button 2", width=6, height=1)
btn2.place(x=0, y=0)



app.mainloop()
