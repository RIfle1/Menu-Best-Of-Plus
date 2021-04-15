import tkinter
from tkinter import *
from tkinter import messagebox
game = Tk()
game.title("Game Creator")
# game.minsize(640, 480)
# game.maxsize(1280, 720)
# game.geometry("1980x1080")
# game.resizable(width=False, height=True)
# game.positionfrom("user")
# game.positionfrom("user")
# game.geometry("480x480+120+120")


# How to center the screen
screen_x = game.winfo_screenwidth()
screen_y = game.winfo_screenheight()
window_x = 1200
window_y = 800

pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)

game.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# How to create a menu

print("abc")


game.mainloop()