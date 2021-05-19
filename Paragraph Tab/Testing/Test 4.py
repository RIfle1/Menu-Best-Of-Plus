from tkinter import *
import tkinter

top = tkinter.Tk()

B1 = tkinter.Button(top, text="arrow", relief=RAISED,cursor="arrow").pack()
B2 = tkinter.Button(top, text="circle", relief=RAISED,cursor="circle").pack()
B3 = tkinter.Button(top, text="clock", relief=RAISED,cursor="clock").pack()
B4 = tkinter.Button(top, text="cross", relief=RAISED,cursor="cross").pack()
B5 = tkinter.Button(top, text="dotbox", relief=RAISED,cursor="dotbox").pack()
B6 = tkinter.Button(top, text="exchange", relief=RAISED,cursor="exchange").pack()
B7 = tkinter.Button(top, text="fleur", relief=RAISED,cursor="fleur").pack()
B8 = tkinter.Button(top, text="heart", relief=RAISED,cursor="heart").pack()
B9 = tkinter.Button(top, text="man", relief=RAISED,cursor="man").pack()
B10 = tkinter.Button(top, text="mouse", relief=RAISED,cursor="mouse").pack()
B11 = tkinter.Button(top, text="pirate", relief=RAISED,cursor="pirate").pack()
B12 = tkinter.Button(top, text="plus", relief=RAISED,cursor="plus").pack()
B13 = tkinter.Button(top, text="shuttle", relief=RAISED,cursor="shuttle").pack()
B14 = tkinter.Button(top, text="sizing", relief=RAISED,cursor="sizing").pack()
B15 = tkinter.Button(top, text="spider", relief=RAISED,cursor="spider").pack()
B16 = tkinter.Button(top, text="spraycan", relief=RAISED,cursor="spraycan").pack()
B17 = tkinter.Button(top, text="star", relief=RAISED,cursor="star").pack()
B18 = tkinter.Button(top, text="target", relief=RAISED,cursor="target").pack()
B19 = tkinter.Button(top, text="tcross", relief=RAISED,cursor="tcross").pack()
B20 = tkinter.Button(top, text="trek", relief=RAISED,cursor="trek").pack()
B21 = tkinter.Button(top, text="watch", relief=RAISED,cursor="watch").pack()

m = Message(top)
m.pack()
txt = Text(top, background=m.cget("background"), relief="flat",
    borderwidth=0, font=m.cget("font"), state="disabled")
txt.pack()
m.destroy()

top.mainloop()
