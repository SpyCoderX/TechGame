import os
os.chdir("./Images/")
for file in os.listdir():
    if file.startswith("Tile_"):
        os.rename()