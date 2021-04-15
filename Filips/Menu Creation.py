import tkinter
from tkinter import *
from tkinter import messagebox
app = Tk()
app.title("Game Creator")
# game.minsize(640, 480)
# game.maxsize(1280, 720)
# game.geometry("1980x1080")
# game.resizable(width=False, height=True)
# game.positionfrom("user")
# game.positionfrom("user")
# game.geometry("480x480+120+120")


# How to center the screen
screen_x = app.winfo_screenwidth()
screen_y = app.winfo_screenheight()
window_x = 1200
window_y = 800

pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)

app.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")

# How to create a menu

main_menu = tkinter.Menu(app)

first_menu = tkinter.Menu(main_menu)
first_menu.add_command(label="Option 1")
first_menu.add_command(label="Option 2")
first_menu.add_command(label="Option 3")

second_menu = tkinter.Menu(main_menu)
second_menu.add_command(label="Command 1")
second_menu.add_command(label="Command 2")
second_menu.add_command(label="Command 3")

main_menu.add_cascade(label="First", menu=first_menu)
main_menu.add_cascade(label="First", menu=second_menu)

# Main Loop
app.mainloop()
app.config(menu=main_menu)