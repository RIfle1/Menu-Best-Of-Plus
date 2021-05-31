# importing os module
import os

# Directory
directory = "database_saves"

# Parent Directory path
parent_dir = "D:\Programming\Menu-Best-Of-Plus\Main\Player Code\Saved Games"

# Path
path = os.path.join(parent_dir, directory)

# Create the directory
os.mkdir(path)


