import tkinter
import boid as bd

window = tkinter.Tk()
window.title("Boid Simulation")

show_range = False

SIZE = 500

space = bd.SimulationSpace(SIZE, SIZE)

canvas = tkinter.Canvas(window, width=SIZE, height=SIZE)
canvas.pack()
paused = True


def initialise_simulation():
    """Initialise the simulation"""
    global space
    global paused
    del space
    space = bd.SimulationSpace(SIZE, SIZE)
    space.populate(20, bouncing=False)
    paused = True
    canvas.delete('all')
    for boid in space.boids:
        x_pos, y_pos = boid.get_coords()
        x_vel, y_vel = boid.get_velocity()
        if show_range:
            boid.near_canvas_id = canvas.create_oval(x_pos - boid.near_distance, y_pos - boid.near_distance, x_pos + boid.near_distance, y_pos + boid.near_distance, fill="", outline="gray")
        boid.canvas_id = canvas.create_line(x_pos, y_pos, x_pos+x_vel, y_pos+y_vel, fill="red", width=5, arrow=tkinter.LAST)
window.configure(width=SIZE, height=SIZE)

# Top frame
top_frame = tkinter.Frame(window)
top_frame.pack(side=tkinter.TOP)

## Iteration counter label
iteration_label = tkinter.Label(top_frame, text="Iteration: 0")
iteration_label.pack(side=tkinter.LEFT)

def update_iteration_label(space):
    """Update the iteration label"""
    iteration_label.configure(text=f"Iteration: {space.iteration}")

def toggle_paused():
    """Toggle the paused state"""
    global paused
    paused = not paused

# Control Frame Bottom
command_frame = tkinter.LabelFrame(window, text="Commands")
command_frame.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.BOTH)

## Control Frame Left
control_frame = tkinter.LabelFrame(command_frame, text="Controls of the simulation")
control_frame.pack(side=tkinter.LEFT)

### Start Button
start_button = tkinter.Button(control_frame, text="Start", command=lambda: start_simulation(space))
start_button.pack()

### Pause/Resume Button
resume_pause_button = tkinter.Button(control_frame, text="Resume/Pause", \
    command=lambda: (toggle_paused() ,move_boid_canvas(space)))
resume_pause_button.pack()

### Next Step Button
next_step_button = tkinter.Button(control_frame, text="Next Step", \
    command=lambda: (space.next_step(), move_boid_canvas(space)))
next_step_button.pack()

## Window Frame Right
settings_frame = tkinter.LabelFrame(command_frame, text="Settings")
settings_frame.pack(side=tkinter.RIGHT)

### Reinitialise Button
reinitialise_button = tkinter.Button(settings_frame, text="Reinitialise", \
    command=lambda: (initialise_simulation(), move_boid_canvas(space)))
reinitialise_button.pack()

def move_boid_canvas(space):
    """Move the boid canvas"""
    update_iteration_label(space)
    for boid in space.boids:
        x_pos, y_pos = boid.get_coords()
        x_vel, y_vel = boid.get_velocity()
        if show_range:
            canvas.coords(boid.near_canvas_id, x_pos - boid.near_distance, y_pos - boid.near_distance, x_pos + boid.near_distance, y_pos + boid.near_distance)
        canvas.coords(boid.canvas_id, x_pos, y_pos, x_pos+x_vel, y_pos+y_vel)

def iterate_simulation(space):
    """Move the boid canvas and update the position"""
    if not paused:
        move_boid_canvas(space)
        space.next_step()
    window.after(10, lambda: iterate_simulation(space))

def start_simulation(space):
    """Start the simulation"""
    toggle_paused()
    iterate_simulation(space)


initialise_simulation()
window.mainloop()