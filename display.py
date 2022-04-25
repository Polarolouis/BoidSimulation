import tkinter
import boid

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

WIDTH, HEIGHT = (1000, 600)
NUMBER_OF_BOIDS = 50
NUMBER_OF_STEPS = 1_000
BOUNCING = True
ALIGNMENT = True
SEPARATION = True
COHESION = True
WIND = False
WIND_SPEED = 0
WIND_DIRECTION = 0
GOAL = False
GOAL_X = 0
GOAL_Y = 0

sim_space = None

#------------------------------------------------------------------------------
# Main window
#------------------------------------------------------------------------------
root = tkinter.Tk()
root.configure(background='white')
root.title("Boids")

# Top Frame
top_frame = tkinter.Frame(root)
top_frame.pack(side=tkinter.TOP, fill=tkinter.X)
## Label number of boids
label_number_of_boids = tkinter.Label(top_frame, text=f"Boids : {NUMBER_OF_BOIDS}", font=("Helvetica", 16))
label_number_of_boids.pack(side=tkinter.LEFT)
##
label_messages = tkinter.Label(top_frame, text="", font=("Helvetica", 16))
label_messages.pack()
## Label number of iterations
label_iterations = tkinter.Label(top_frame, text=f"Iterations : {0}", font=("Helvetica", 16))
label_iterations.pack(side=tkinter.RIGHT)

# Bottom Frame
bottom_frame = tkinter.Frame(root)
bottom_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
## Button to start the simulation
button_start = tkinter.Button(bottom_frame, text="Start", font=("Helvetica", 16), command=lambda: (stock_simulation((start_simulation(root, NUMBER_OF_BOIDS, WIDTH, HEIGHT))), \
    button_start.config(state="disable"), button_reset.config(state="normal"), button_pause.config(state="normal"), disable_parameters_on_start()))
button_start.pack(side=tkinter.LEFT)
## Button to pause the simulation
button_pause = tkinter.Button(bottom_frame, text="Pause/Resume", font=("Helvetica", 16), command=lambda: (sim_space.toggle_pause(), label_messages.config(text="Simulation paused" if sim_space.paused else "", fg="red")))
button_pause.config(state="disable")
button_pause.pack(side=tkinter.LEFT)
## Button to reset the simulation
button_reset = tkinter.Button(bottom_frame, text="Reset", font=("Helvetica", 16), command=lambda: (reset_simulation(sim_space, canvas), \
    button_start.config(state="normal"), button_reset.config(state="disable"), button_pause.config(state="disable"), label_messages.config(text=""), enable_parameters_on_reset()))
button_reset.config(state="disable")
button_reset.pack(side=tkinter.RIGHT)

# Parameters frame (right)
parameters_frame = tkinter.Frame(root)
parameters_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)

## Validation button
def validate_parameters():
    """Set the parameters"""
    global NUMBER_OF_BOIDS, NUMBER_OF_STEPS, BOUNCING, ALIGNMENT, SEPARATION, COHESION, WIND, WIND_SPEED, WIND_DIRECTION, GOAL, GOAL_X, GOAL_Y
    BOUNCING = True if bouncing_boolean.get() else False
    NUMBER_OF_BOIDS = int(number_of_boids_slider.get())
    label_number_of_boids.config(text=f"Boids : {NUMBER_OF_BOIDS}")
    NUMBER_OF_STEPS = int(number_of_steps_spinbox.get())
    
    ALIGNMENT = True if alignment_boolean.get() else False
    COHESION = True if cohesion_boolean.get() else False
    SEPARATION = True if separation_boolean.get() else False
    WIND = True if wind_boolean.get() else False
    if WIND:
        WIND_SPEED = float(wind_speed_slider.get()/10)
        WIND_DIRECTION = int(wind_direction_slider.get())
    GOAL = True if goal_boolean.get() else False
    if GOAL:
        GOAL_X = int(goal_x_slider.get())
        GOAL_Y = int(goal_y_slider.get())
    set_recap_labels()

## Bouncing checkbox 
bouncing_boolean = tkinter.BooleanVar()
bouncing_checkbox = tkinter.Checkbutton(parameters_frame, text="Bouncing", font=("Helvetica", 16), variable=bouncing_boolean, onvalue=True, offvalue=False, command= lambda: (validate_parameters()))
if BOUNCING:
    bouncing_checkbox.select()
bouncing_checkbox.pack()

## Number of boids slider
number_of_boids_slider = tkinter.Scale(parameters_frame, from_=1, to=1000, orient=tkinter.HORIZONTAL, length=200, label="Number of boids", font=("Helvetica", 16), command=lambda e: (validate_parameters()))
number_of_boids_slider.set(NUMBER_OF_BOIDS)
number_of_boids_slider.pack()

## Number of steps slider
label_number_of_steps = tkinter.Label(parameters_frame, text="Number of steps", font=("Helvetica", 16))
label_number_of_steps.pack()
tkinter.Label(parameters_frame, text="0 for infinite loop", font=("Helvetica", 10)).pack()
var_number_of_steps_spinbox = tkinter.StringVar()
var_number_of_steps_spinbox.set(NUMBER_OF_STEPS)
number_of_steps_spinbox = tkinter.Spinbox(parameters_frame, from_=0, to=1_000_000, textvariable=var_number_of_steps_spinbox, font=("Helvetica", 16), command= lambda: (validate_parameters()))
number_of_steps_spinbox.pack()

## Forces frame
forces_frame = tkinter.LabelFrame(parameters_frame, text="Forces", font=("Helvetica", 16))
forces_frame.pack()

### Alignment checkbox
alignment_boolean = tkinter.BooleanVar()
alignment_checkbox = tkinter.Checkbutton(forces_frame, text="Alignment", font=("Helvetica", 16), variable=alignment_boolean, onvalue=True, offvalue=False, command= lambda: (validate_parameters()))
if ALIGNMENT:
    alignment_checkbox.select() 
alignment_checkbox.pack()

### Cohesion checkbox
cohesion_boolean = tkinter.BooleanVar()
cohesion_checkbox = tkinter.Checkbutton(forces_frame, text="Cohesion", font=("Helvetica", 16), variable=cohesion_boolean, onvalue=True, offvalue=False, command= lambda: (validate_parameters()))
if COHESION:
    cohesion_checkbox.select()
cohesion_checkbox.pack()

### Separation checkbox
separation_boolean = tkinter.BooleanVar()
separation_checkbox = tkinter.Checkbutton(forces_frame, text="Separation", font=("Helvetica", 16), variable=separation_boolean, onvalue=True, offvalue=False, command= lambda: (validate_parameters()))
if SEPARATION:
    separation_checkbox.select()
separation_checkbox.pack()

### Wind checkbox

def toggle_wind_parameters():
    """ Show the wind parameters if the wind checkbox is selected """
    if wind_boolean.get():
        wind_parameters_frame.pack()
    else:
        wind_parameters_frame.pack_forget()

wind_boolean = tkinter.BooleanVar()
wind_checkbox = tkinter.Checkbutton(forces_frame, text="Wind", font=("Helvetica", 16), variable=wind_boolean, onvalue=True, offvalue=False, command=lambda: (toggle_wind_parameters(), validate_parameters()))

#### Wind parameters
wind_parameters_frame = tkinter.LabelFrame(forces_frame, text="Wind Settings", font=("Helvetica", 16))

if WIND:
    wind_checkbox.select()
    wind_parameters_frame.pack()
wind_checkbox.pack()

##### Wind speed slider
wind_speed_slider = tkinter.Scale(wind_parameters_frame, from_=0, to=10, orient=tkinter.HORIZONTAL, 
    length=200, tickinterval=2, label="Wind speed", font=("Helvetica", 16), command= lambda e: (validate_parameters()))
wind_speed_slider.set(0)
wind_speed_slider.pack()

##### Wind direction slider
wind_direction_slider = tkinter.Scale(wind_parameters_frame, from_=0, to=360, orient=tkinter.HORIZONTAL, 
    length=200, label="Wind direction", font=("Helvetica", 16), command= lambda e: (validate_parameters()))
wind_direction_slider.set(0)
wind_direction_slider.pack()

### Goal checkbox

def toggle_goal_parameters():
    """ Show the goal parameters if the goal checkbox is selected """
    if goal_boolean.get():
        goal_parameters_frame.pack()
    else:
        goal_parameters_frame.pack_forget()

goal_boolean = tkinter.BooleanVar()
goal_checkbox = tkinter.Checkbutton(forces_frame, text="Goal", font=("Helvetica", 16), variable=goal_boolean, onvalue=True, offvalue=False, command= lambda: (toggle_goal_parameters(), validate_parameters()))

#### Goal parameters frame
goal_parameters_frame = tkinter.LabelFrame(forces_frame, text="Goal Settings", font=("Helvetica", 16))

if GOAL:
    goal_checkbox.select()
    goal_parameters_frame.pack()
goal_checkbox.pack()

##### Goal x slider
goal_x_slider = tkinter.Scale(goal_parameters_frame, from_=0, to=WIDTH, orient=tkinter.HORIZONTAL,
    length=200, tickinterval=10, label="Goal x", font=("Helvetica", 16), command= lambda e: (validate_parameters()))
goal_x_slider.set(0)
goal_x_slider.pack()

##### Goal y slider
goal_y_slider = tkinter.Scale(goal_parameters_frame, from_=0, to=HEIGHT, orient=tkinter.HORIZONTAL,
    length=200, tickinterval=10, label="Goal y", font=("Helvetica", 16), command= lambda e: (validate_parameters()))
goal_y_slider.set(0)
goal_y_slider.pack()

button_validate = tkinter.Button(parameters_frame, text="Validate", font=("Helvetica", 16), command=lambda: validate_parameters())
button_validate.pack()

## Left recap frame
left_recap_frame = tkinter.Frame(root)
left_recap_frame.pack(side=tkinter.LEFT, fill=tkinter.Y)

### Recap LabelFrame
recap_label_frame = tkinter.LabelFrame(left_recap_frame, text="Recap", font=("Helvetica", 16))
recap_label_frame.pack()

### Display the parameters of the simulation
label_max_iterations = tkinter.Label(recap_label_frame, text=f"Max iterations: {NUMBER_OF_STEPS}", font=("Helvetica", 16))
label_max_iterations.pack()

label_bouncing = tkinter.Label(recap_label_frame, text=f"Bouncing : {BOUNCING}\n", font=("Helvetica", 16), fg="green" if BOUNCING else "red")
label_bouncing.pack()

label_forces = tkinter.LabelFrame(recap_label_frame, text="Forces :\n", font=("Helvetica", 16))
label_forces.pack()

label_alignment_forces = tkinter.Label(label_forces, text=f"Alignment : {ALIGNMENT}\n", font=("Helvetica", 16), fg="green" if ALIGNMENT else "red")
label_alignment_forces.pack()

label_cohesion_forces = tkinter.Label(label_forces, text=f"Cohesion : {COHESION}\n", font=("Helvetica", 16), fg="green" if COHESION else "red")
label_cohesion_forces.pack()

label_separation_forces = tkinter.Label(label_forces, text=f"Separation : {SEPARATION}\n", font=("Helvetica", 16), fg="green" if SEPARATION else "red")
label_separation_forces.pack()

labelframe_wind_forces = tkinter.LabelFrame(label_forces, text=f"Wind : {WIND}\n", font=("Helvetica", 16), fg="green" if WIND else "red")
labelframe_wind_forces.pack()

label_wind_speed = tkinter.Label(labelframe_wind_forces, text=f"Wind speed : {WIND_SPEED}", font=("Helvetica", 16))
label_wind_speed.pack()

label_wind_direction = tkinter.Label(labelframe_wind_forces, text=f"Wind direction : {WIND_DIRECTION}", font=("Helvetica", 16))
label_wind_direction.pack()

labelframe_goal_forces = tkinter.LabelFrame(label_forces, text=f"Goal : {GOAL}\n", font=("Helvetica", 16), fg="green" if GOAL else "red")
labelframe_goal_forces.pack()

label_goal_position = tkinter.Label(labelframe_goal_forces, text=f"Goal : ({GOAL_X},{GOAL_Y})", font=("Helvetica", 16))
label_goal_position.pack()

def set_recap_labels():
    """Set the recap labels"""
    global NUMBER_OF_STEPS, label_max_iterations, label_bouncing, BOUNCING, label_alignment_forces, ALIGNMENT, label_cohesion_forces, COHESION, \
    label_separation_forces, SEPARATION, labelframe_wind_forces, WIND, label_wind_speed, WIND_SPEED, label_wind_direction, WIND_DIRECTION, \
    labelframe_goal_forces, GOAL, label_goal_position, GOAL_X, GOAL_Y

    if not NUMBER_OF_STEPS:
        label_max_iterations.config(text="Max iterations :  ∞")
    else:
        label_max_iterations.config(text=f"Max iterations: {NUMBER_OF_STEPS}")
    label_bouncing.config(text=f"Bouncing : {BOUNCING}\n", fg="green" if BOUNCING else "red")
    label_alignment_forces.config(text=f"Alignment : {ALIGNMENT}\n", fg="green" if ALIGNMENT else "red")
    label_cohesion_forces.config(text=f"Cohesion : {COHESION}\n", fg="green" if COHESION else "red")
    label_separation_forces.config(text=f"Separation : {SEPARATION}\n", fg="green" if SEPARATION else "red")
    labelframe_wind_forces.config(text=f"Wind : {WIND}\n", fg="green" if WIND else "red")
    label_wind_speed.config(text=f"Wind speed : {WIND_SPEED}")
    label_wind_direction.config(text=f"Wind direction : {WIND_DIRECTION}")
    labelframe_goal_forces.config(text=f"Goal : {GOAL}\n", fg="green" if GOAL else "red")
    label_goal_position.config(text=f"Goal : ({GOAL_X},{GOAL_Y})")
    

def disable_parameters_on_start():
    """Disable the parameters on start"""
    bouncing_checkbox.config(state="disable")
    number_of_boids_slider.config(state="disable")
    number_of_steps_spinbox.config(state="disable")
    button_validate.config(state="disable")
    alignment_checkbox.config(state="disable")
    cohesion_checkbox.config(state="disable")
    separation_checkbox.config(state="disable")
    wind_checkbox.config(state="disable")
    wind_speed_slider.config(state="disable")
    wind_direction_slider.config(state="disable")
    goal_checkbox.config(state="disable")
    goal_x_slider.config(state="disable")
    goal_y_slider.config(state="disable")

def enable_parameters_on_reset():
    """Enable the parameters on reset"""
    bouncing_checkbox.config(state="normal")
    number_of_boids_slider.config(state="normal")
    number_of_steps_spinbox.config(state="normal")
    button_validate.config(state="normal")
    alignment_checkbox.config(state="normal")
    cohesion_checkbox.config(state="normal")
    separation_checkbox.config(state="normal")
    wind_checkbox.config(state="normal")
    wind_speed_slider.config(state="normal")
    wind_direction_slider.config(state="normal")
    goal_checkbox.config(state="normal")
    goal_x_slider.config(state="normal")
    goal_y_slider.config(state="normal")

#------------------------------------------------------------------------------
# Canvas
#------------------------------------------------------------------------------
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, background='ivory')
canvas.pack()

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def stock_simulation(simulation_space):
    """Stock the simulation"""
    global sim_space
    sim_space = simulation_space

def start_simulation(root, number_of_boids, width, height):
    """Start the simulation"""
    # Create the simulation space
    simulation_space = boid.SimulationSpace(width, height)
    # Populate the simulation space
    simulation_space.populate(number_of_boids, bouncing=BOUNCING, 
        alignment_bool=ALIGNMENT, cohesion_bool=COHESION, separation_bool=SEPARATION, wind_bool=WIND, wind_speed=WIND_SPEED, wind_direction=WIND_DIRECTION, goal_bool=GOAL, goal_x=GOAL_X, goal_y=GOAL_Y)
    # Start the simulation
    simulation_space.start_simulation(number_of_steps=NUMBER_OF_STEPS)
    create_boids_canvas(canvas, simulation_space)
    # Start the simulation loop
    simulation_loop(root, canvas, simulation_space)
    return simulation_space

def create_boids_canvas(canvas, simulation_space):
    """Create the boids on the canvas"""
    for boid in simulation_space.boids:
        # Extract the boid's position
        x, y = boid.get_coords()
        # Create the boid on the canvas
        boid.canvas_item = canvas.create_oval(x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius, fill="green" if boid.the_chosen_one else "black")
        boid.velocity_item = canvas.create_line(x, y, x + boid.velocity[0][0], y + boid.velocity[1][0], fill="red", width=2, arrow="last")
        if GOAL:
            canvas.goal_item = canvas.create_rectangle(GOAL_X, GOAL_Y, GOAL_X+10, GOAL_Y+10, fill="blue")

def update_canvas(canvas, simulation_space):
    """Update the canvas"""
    for index, boid in enumerate(simulation_space.boids):
        # Extract the boid's position
        x, y = boid.get_coords()
        # Update the boid on the canvas
        canvas.coords(boid.canvas_item, x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius)
        canvas.coords(boid.velocity_item, x, y, x + boid.velocity[0][0], y + boid.velocity[1][0])
        if GOAL:
            canvas.coords(canvas.goal_item, GOAL_X, GOAL_Y, GOAL_X+10, GOAL_Y+10)

def clear_canvas(simulation_space, canvas):
    """Clear the canvas"""
    if simulation_space.finished:
        canvas.delete("all")
    else:
        print("The simulation is not finished")
        label_messages.config(text="The simulation is not finished", fg="red")
        label_messages.after(2000, lambda: label_messages.config(text=""))

def simulation_loop(root, canvas, simulation_space):
    """Simulation loop"""
    if simulation_space.finished:
        return
    
    if max_iterations_reached(simulation_space):
        stop_simulation(simulation_space)
    
    if not simulation_space.paused:
        # Update the simulation
        simulation_space.next_step()
        # Update the canvas
        update_canvas(canvas, simulation_space)
        # Update the number of iterations
        label_iterations.config(text=f"Iterations : {simulation_space.iteration}")
        # Check if the simulation is finished
    # Continue the simulation loop
    root.after(10, lambda: simulation_loop(root, canvas, simulation_space))

def max_iterations_reached(simulation_space):
    """Check if the maximum number of iterations is reached"""
    if NUMBER_OF_STEPS == 0:
        return False
    return simulation_space.iteration >= NUMBER_OF_STEPS-1

def stop_simulation(simulation_space):
    """Stop the simulation"""
    simulation_space.finish_simulation()
    print("Simulation finished")

def reset_simulation(simulation_space, canvas):
    """Reset the simulation"""
    print("Reset the simulation")
    stop_simulation(simulation_space)
    clear_canvas(simulation_space, canvas)
    # We clear the simulation space
    simulation_space.clear()
    label_iterations.config(text=f"Iterations : {simulation_space.iteration}")
    


#------------------------------------------------------------------------------
# Main loop
#------------------------------------------------------------------------------

# the window is maximized
root.state('zoomed')
root.mainloop()