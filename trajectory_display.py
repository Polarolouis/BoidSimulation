import json
import os
import tkinter

def get_json_files_name():
    """List all the json files in the current directory"""
    # Get all the files in the directory
    files = os.listdir(".")
    # Get the file names
    files_name = [file for file in files if file.endswith(".json")]
    return files_name

def menu():
    """Display the menu"""
    possibles_files = dict(enumerate(get_json_files_name()))
    for index, file in possibles_files.items():
        print(f"{index+1} - {file}")
    print("0 - Exit")
    selected_index = -1 # Default value
    inputIsValid = False
    while not inputIsValid:
        try:
            selected_index = int(input("Select a file by its index: "))
            selected_index -= 1
            inputIsValid = selected_index in possibles_files.keys()
            if selected_index == -1:
                inputIsValid = True
            if not inputIsValid:
                print("Input not in the possibilities, please try again")
        except ValueError:
            print("Please enter an integer")
            continue
    if selected_index == -1:
        return False
    
    return possibles_files[selected_index]

filename = menu()
if not filename:
    print("Exiting")
    quit()
print(f"Selected file: {filename}")
data = dict()
with open(filename, "r", encoding="utf8") as f:
    raw_data = json.load(f)
    for key in raw_data:
        data[int(key)] = raw_data[key]


number_of_boids, _, _, geometry, _, _, max_iteration, _ = filename.strip().split("_")

number_of_boids = int(number_of_boids)
max_iteration = int(max_iteration)

print(f"Max iteration: {max_iteration}")

# Create the window
root = tkinter.Tk()
root.title("Trajectory display")
root.geometry(f"{geometry}")

width, height = geometry.split("x")
width = int(width)
height = int(height)

canvas = tkinter.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

list_of_boid_canvas = []

# Creation of the canvas
for i in range(number_of_boids):
    x, y = data[0][str(i)]
    list_of_boid_canvas.append(canvas.create_oval(x-5, y-5, x+5, y+5, fill="grey"))

current_turn = 1

def update_canvas(current_turn):
    """Update the canvas"""
    for i in range(number_of_boids):
        x, y = data[current_turn][str(i)]
        canvas.coords(list_of_boid_canvas[i], x-5, y-5, x+5, y+5)
    root.after(100, lambda : (update_canvas(current_turn+1) if current_turn < max_iteration else None))

update_canvas(current_turn)

root.mainloop()
