import json
import os
import tkinter

PAUSED = False
SPEED = 10


def get_json_files_name():
    """List all the json files in the current directory"""
    # Get all the files in the directory
    files = os.listdir("./json")
    # Get the file names
    files_name = [file for file in files if file.endswith(".json")]
    return files_name


def menu():
    """Display the menu"""
    possibles_files = dict(enumerate(get_json_files_name()))
    for index, file in possibles_files.items():
        print(f"{index+1} - {file}")
    print("0 - Exit")
    selected_index = -1  # Default value
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
with open("json/" + filename, "r", encoding="utf8") as f:
    raw_data = json.load(f)
    for key in raw_data:
        data[int(key)] = raw_data[key]

alignment_force = 0.0
cohesion_force = 0.0
separation_force = 0.0
wind_speed = 0.0
wind_direction = 0
goal_force = 0.0
goal_position_string = ""
goal_x = 0.0
goal_y = 0.0

if len(filename.strip().split("_")) > 8:
    number_of_boids, _, _, geometry, _, _, max_iteration, \
        _, _, _, alignment_force, _, _, cohesion_force, _, _,\
        separation_force, _, _, wind_speed, _, _, wind_direction,\
        _, _, goal_force, _, _, goal_position_string, _, \
        bouncing = filename.strip().split("_")
else:
    number_of_boids, _, _, geometry, _, _, max_iteration, * \
        _ = filename.strip().split("_")

number_of_boids = int(number_of_boids)
max_iteration = int(max_iteration)
alignment_force = float(alignment_force)
cohesion_force = float(cohesion_force)
separation_force = float(separation_force)
wind_speed = float(wind_speed)
wind_direction = int(wind_direction)
goal_force = float(goal_force)
goal_position_string = goal_position_string.split("x")
goal_x, goal_y = (float(x) for x in goal_position_string)

print(f"Max iteration: {max_iteration}")

# Create the window
root = tkinter.Tk()
root.title("Trajectory display")
root.geometry(f"{geometry}")

width, height = geometry.split("x")
width = int(width)
height = int(height)

canvas = tkinter.Canvas(root, width=width, height=height, bg="white")
canvas.grid(row=1, column=1, columnspan=3)

# Top Frame
top_frame = tkinter.Frame(root)
top_frame.grid(row=0, column=1, columnspan=3)

iteration_label = tkinter.Label(
    top_frame, text="Iteration:", font=("Helvetica", 20))
iteration_label.grid(row=0, column=0)

# Left frame
left_frame = tkinter.Frame(root)
left_frame.grid(row=0, column=0, rowspan=2)

# Speed slider
speed_slider = tkinter.Scale(left_frame, from_=1, to=1000, length=200,
                             orient=tkinter.HORIZONTAL, command=lambda e: set_speed())
speed_slider.set(SPEED)
speed_slider.grid(row=1, column=0, columnspan=3)

# Start button
start_button = tkinter.Button(
    left_frame, text="Start", command=lambda: (update_canvas(1)))
start_button.grid(row=2, column=0)

# Pause/Resume button
pause_button = tkinter.Button(
    left_frame, text="Pause", command=lambda e: pause_unpause())
pause_button.grid(row=2, column=1)

# Quit button
quit_button = tkinter.Button(
    left_frame, text="Quit", command=root.quit, bg="red")
quit_button.grid(row=2, column=2)

# Right frame
right_frame = tkinter.Frame(root)
right_frame.grid(row=0, column=4, rowspan=2)

bouncing_label = tkinter.Label(right_frame, text=f"Bouncing: {bouncing}")

alignment_force_label = tkinter.Label(
    right_frame, text=f"Alignment force: {alignment_force}")
alignment_force_label.grid(row=0, column=0)

cohesion_force_label = tkinter.Label(
    right_frame, text=f"Cohesion force: {cohesion_force}")
cohesion_force_label.grid(row=1, column=0)

separation_force_label = tkinter.Label(
    right_frame, text=f"Separation force: {separation_force}")
separation_force_label.grid(row=2, column=0)

wind_force_label = tkinter.Label(right_frame, text=f"Wind force: {wind_speed}")
wind_force_label.grid(row=3, column=0)

wind_speed_label = tkinter.Label(right_frame, text=f"Wind speed: {wind_speed}")
wind_speed_label.grid(row=4, column=0)

goal_force_label = tkinter.Label(right_frame, text=f"Goal force: {goal_force}")
goal_force_label.grid(row=5, column=0)

goal_position_label = tkinter.Label(
    right_frame, text=f"Goal position: {goal_x}, {goal_y}")


list_of_boid_canvas = []
goal_canvas = 0

# Creation of the canvas
for i in range(number_of_boids):
    x, y = data[0][str(i)]
    list_of_boid_canvas.append(
        canvas.create_oval(x-5, y-5, x+5, y+5, fill="grey"))
if goal_force != 0:
    goal_canvas = canvas.create_oval(
        goal_x-5, goal_y-5, goal_x+5, goal_y+5, fill="blue")

iteration_label.configure(
    text=f"Iteration: {0}/{max_iteration}", font=("Helvetica", 20))


def update_canvas(current_turn):
    """Update the canvas"""
    if not PAUSED:
        iteration_label.configure(
            text=f"Iteration: {current_turn}/{max_iteration}")
        for i in range(number_of_boids):
            x, y = data[current_turn][str(i)]
            canvas.coords(list_of_boid_canvas[i], x-5, y-5, x+5, y+5)
        if goal_force != 0:
            canvas.coords(goal_canvas, goal_x-5, goal_y-5, goal_x+5, goal_y+5)
        root.after(SPEED, lambda: (update_canvas(current_turn+1)
                   if current_turn < max_iteration else None))
    else:
        root.after(SPEED, lambda: (update_canvas(current_turn)))


def pause_unpause():
    """Pause or unpause the simulation"""
    global PAUSED
    PAUSED = not PAUSED


def set_speed():
    """Set the speed of the simulation"""
    global SPEED, speed_slider
    SPEED = int(speed_slider.get())


# Maximize the window
root.attributes("-fullscreen", True)
root.state("zoomed")
root.mainloop()
