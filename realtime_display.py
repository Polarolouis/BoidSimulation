import tkinter
import boid

# ------------------------------------------------------------------------------
# Main window
# ------------------------------------------------------------------------------
root = tkinter.Tk()
root.configure(background='white')
root.title("Boids")

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

WIDTH, HEIGHT = (root.winfo_screenwidth() - 472,
                 root.winfo_screenheight()-300)  # (1200, 800)
NUMBER_OF_BOIDS = 50
NUMBER_OF_STEPS = 1_000
BOUNCING = True
WIND_SPEED = 0
WIND_DIRECTION = 0
GOAL_X = WIDTH/2
GOAL_Y = HEIGHT/2

OBSTACLE = []

ALIGNMENT_FORCE_MULTIPLICATOR = 1
COHESION_FORCE_MULTIPLICATOR = 1
SEPARATION_FORCE_MULTIPLICATOR = 1
GOAL_FORCE_MULTIPLICATOR = 1

SIMULATION_SPEED = 10  # Time between each step in milliseconds

sim_space = None

# ------------------------------------------------------------------------------
# Divisions of the main window
# ------------------------------------------------------------------------------


def validate_parameters():
    """Set the parameters
    Global variables are set to the values of the parameters"""

    global NUMBER_OF_BOIDS, NUMBER_OF_STEPS, BOUNCING, WIND_SPEED, \
        WIND_DIRECTION, GOAL_X, GOAL_Y, ALIGNMENT_FORCE_MULTIPLICATOR, \
        COHESION_FORCE_MULTIPLICATOR, SEPARATION_FORCE_MULTIPLICATOR, \
        GOAL_FORCE_MULTIPLICATOR, SIMULATION_SPEED
    BOUNCING = True if bouncing_boolean.get() else False
    NUMBER_OF_BOIDS = int(number_of_boids_slider.get())
    if NUMBER_OF_BOIDS >= 100:
        label_warning.config(
            text="A lot of boids means slower real-time simulation consider using pre-computing !", fg="red", font=("Helvectica", 16))
    else:
        label_warning.config(text="", fg="black")
    label_number_of_boids.config(text=f"Boids : {NUMBER_OF_BOIDS}")
    NUMBER_OF_STEPS = int(number_of_steps_spinbox.get())

    WIND_SPEED = float(wind_speed_slider.get())
    WIND_DIRECTION = int(wind_direction_slider.get())

    GOAL_X = int(goal_x_slider.get())
    GOAL_Y = int(goal_y_slider.get())

    ALIGNMENT_FORCE_MULTIPLICATOR = float(alignment_force_slider.get())
    COHESION_FORCE_MULTIPLICATOR = float(cohesion_force_slider.get())
    SEPARATION_FORCE_MULTIPLICATOR = float(separation_force_slider.get())
    GOAL_FORCE_MULTIPLICATOR = float(goal_force_slider.get())

    SIMULATION_SPEED = int(simulation_speed_slider.get())

    boid.Boid.set_goal_position(GOAL_X, GOAL_Y)
    boid.Boid.set_force_parameters(ALIGNMENT_FORCE_MULTIPLICATOR, COHESION_FORCE_MULTIPLICATOR,
                                   SEPARATION_FORCE_MULTIPLICATOR, GOAL_FORCE_MULTIPLICATOR, WIND_SPEED, WIND_DIRECTION, BOUNCING)
    set_recap_labels()


# Top Frame
top_frame = tkinter.Frame(root)
top_frame.grid(row=0, column=0, sticky="n")


##
label_messages = tkinter.Label(top_frame, text="", font=("Helvetica", 12))
label_messages.grid(row=0, column=0, sticky="nswe")

# Bottom Frame
bottom_frame = tkinter.Frame(root)
bottom_frame.grid(row=0, column=0, sticky="s")

# Slider to set the simulation speed
simulation_speed_slider = tkinter.Scale(bottom_frame, from_=1, to=100, orient=tkinter.HORIZONTAL,
                                        label="Simulation speed", length=200, command=lambda e: validate_parameters())
simulation_speed_slider.set(SIMULATION_SPEED)
simulation_speed_slider.grid(row=0, columnspan=3, sticky="w")

# Button to start the simulation
button_start = tkinter.Button(bottom_frame, text="Start", font=("Helvetica", 12), command=lambda: (stock_simulation((start_simulation(root, NUMBER_OF_BOIDS, WIDTH, HEIGHT))),
                                                                                                   button_start.config(state="disable"), button_reset.config(state="normal"), button_pause.config(state="normal"), disable_parameters_on_start(), canvas.bind("<Button-1>", lambda e: integrate_click(*callback(e)))), bg="green")
button_start.grid(row=1, column=0, sticky="w")

# Button to pause the simulation
button_pause = tkinter.Button(bottom_frame, text="Pause/Resume", font=("Helvetica", 12), command=lambda: (
    sim_space.toggle_pause(), label_messages.config(text="Simulation paused" if sim_space.paused else "", fg="red")))
button_pause.config(state="disable")
button_pause.grid(row=1, column=1, sticky="w")

# Button to reset the simulation
button_reset = tkinter.Button(bottom_frame, text="Reset", font=("Helvetica", 12), command=lambda: (reset_simulation(sim_space, canvas),
                                                                                                   button_start.config(state="normal"), button_reset.config(
                                                                                                       state="disable"), button_pause.config(state="disable"), label_messages.config(text=""),
                                                                                                   enable_parameters_on_reset(), label_messages.config(text="Simulation reset", fg="red"), canvas.unbind("<Button-1>")), fg="red")
button_reset.config(state="disable")
button_reset.grid(row=2, column=0, sticky="e")

# Button to quit
button_quit = tkinter.Button(bottom_frame, text="Quit", font=(
    "Helvetica", 12), command=lambda: (root.destroy()), bg="red")
button_quit.grid(row=2, column=1, sticky="e")

# Parameters frame (right)
parameters_frame = tkinter.LabelFrame(
    root, text="Parameters", font=("Helvetica", 12))
parameters_frame.grid(row=0, column=3, sticky="nswe")

# Bouncing checkbox
bouncing_boolean = tkinter.BooleanVar()
bouncing_checkbox = tkinter.Checkbutton(parameters_frame, text="Bouncing", font=(
    "Helvetica", 12), variable=bouncing_boolean, onvalue=True, offvalue=False, command=lambda: (validate_parameters()))
if BOUNCING:
    bouncing_checkbox.select()
bouncing_checkbox.grid(row=0, column=0, sticky="w")

# Number of boids slider
number_of_boids_slider = tkinter.Scale(parameters_frame, from_=1, to=400, orient=tkinter.HORIZONTAL,
                                       length=200, label="Number of boids", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
number_of_boids_slider.set(NUMBER_OF_BOIDS)
number_of_boids_slider.grid(row=1, column=0, sticky="w")

# Number of steps slider
label_number_of_steps = tkinter.Label(
    parameters_frame, text="Number of steps", font=("Helvetica", 12))
label_number_of_steps.grid(row=2, column=0, sticky="ew")
tkinter.Label(parameters_frame, text="0 for infinite loop", font=(
    "Helvetica", 10)).grid(row=3, column=0, sticky="ew")
var_number_of_steps_spinbox = tkinter.StringVar()
var_number_of_steps_spinbox.set(NUMBER_OF_STEPS)
number_of_steps_spinbox = tkinter.Spinbox(parameters_frame, from_=0, to=1_000_000, textvariable=var_number_of_steps_spinbox, font=(
    "Helvetica", 12), command=lambda: (validate_parameters()))
number_of_steps_spinbox.grid(row=4, column=0, sticky="we")

# Forces frame
forces_frame = tkinter.LabelFrame(
    parameters_frame, text="Forces", font=("Helvetica", 12))
forces_frame.grid(row=5, column=0, columnspan=2, sticky="we")

# Alignment force
alignment_force_slider = tkinter.Scale(forces_frame, from_=0, to=2, resolution=0.1, orient=tkinter.HORIZONTAL,
                                       length=200, label="Alignment force", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
alignment_force_slider.set(ALIGNMENT_FORCE_MULTIPLICATOR)
alignment_force_slider.grid(row=0, column=0, columnspan=2, sticky="we")


# Cohesion force
cohesion_force_slider = tkinter.Scale(forces_frame, from_=0, to=2, resolution=0.1, orient=tkinter.HORIZONTAL,
                                      length=200, label="Cohesion force", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
cohesion_force_slider.set(COHESION_FORCE_MULTIPLICATOR)
cohesion_force_slider.grid(row=1, column=0, sticky="we")


# Separation force
separation_force_slider = tkinter.Scale(forces_frame, from_=0, to=2, resolution=0.1, orient=tkinter.HORIZONTAL, length=200,
                                        label="Separation force multiplicator", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
separation_force_slider.set(SEPARATION_FORCE_MULTIPLICATOR)
separation_force_slider.grid(row=2, column=0, sticky="we")

# Wind parameters
wind_parameters_frame = tkinter.LabelFrame(
    forces_frame, text="Wind Settings", font=("Helvetica", 12))
wind_parameters_frame.grid(row=3, column=0, sticky="we")

# Wind speed slider
wind_speed_slider = tkinter.Scale(wind_parameters_frame, from_=0, to=1, orient=tkinter.HORIZONTAL,
                                  length=200, resolution=0.01, label="Wind speed", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
wind_speed_slider.set(0)
wind_speed_slider.grid(row=0, column=0, sticky="we")

# Wind direction slider
wind_direction_slider = tkinter.Scale(wind_parameters_frame, from_=0, to=360, orient=tkinter.HORIZONTAL,
                                      length=200, label="Wind direction", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
wind_direction_slider.set(0)
wind_direction_slider.grid(row=1, column=0, sticky="we")

# Goal force
goal_force_slider = tkinter.Scale(forces_frame, from_=0, to=2, resolution=0.1, orient=tkinter.HORIZONTAL, command=lambda e: (
    validate_parameters()), length=200, label="Goal force multiplicatior", font=("Helvetica", 12))
goal_force_slider.set(GOAL_FORCE_MULTIPLICATOR)
goal_force_slider.grid(row=4, column=0, sticky="we")

# Goal parameters frame
goal_parameters_frame = tkinter.LabelFrame(
    forces_frame, text="Goal Settings", font=("Helvetica", 12))
goal_parameters_frame.grid(row=5, column=0, sticky="we")

# Goal x slider
goal_x_slider = tkinter.Scale(goal_parameters_frame, from_=0, to=WIDTH, orient=tkinter.HORIZONTAL,
                              length=200, tickinterval=0.4*WIDTH, label="Goal x", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
goal_x_slider.set(GOAL_X)
goal_x_slider.grid(row=0, column=0, sticky="we")

# Goal y slider
goal_y_slider = tkinter.Scale(goal_parameters_frame, from_=0, to=HEIGHT, orient=tkinter.HORIZONTAL,
                              length=200, tickinterval=0.4*HEIGHT, label="Goal y", font=("Helvetica", 12), command=lambda e: (validate_parameters()))
goal_y_slider.set(GOAL_Y)
goal_y_slider.grid(row=1, column=0, sticky="we")

# button_validate = tkinter.Button(parameters_frame, text="Validate", font=("Helvetica", 12), command=lambda: validate_parameters())
# button_validate.grid(row=6, column=0, sticky="w")

# Left recap frame
left_recap_frame = tkinter.Frame(root)
left_recap_frame.grid(row=0, column=0, sticky="w")

# Label number of boids
label_number_of_boids = tkinter.Label(
    left_recap_frame, text=f"Boids : {NUMBER_OF_BOIDS}", font=("Helvetica", 12))
label_number_of_boids.grid(row=0, column=0, sticky="w")

# Label number of iterations
label_iterations = tkinter.Label(
    left_recap_frame, text=f"Iterations : {0}", font=("Helvetica", 12))
label_iterations.grid(row=1, column=0, sticky="e")

# Recap LabelFrame
recap_label_frame = tkinter.LabelFrame(
    left_recap_frame, text="Recap", font=("Helvetica", 12))
recap_label_frame.grid(row=2, column=0, sticky="w")

# Display the parameters of the simulation
label_max_iterations = tkinter.Label(
    recap_label_frame, text=f"Max iterations: {NUMBER_OF_STEPS}", font=("Helvetica", 12))
label_max_iterations.grid(row=0, column=0, sticky="w")

label_bouncing = tkinter.Label(recap_label_frame, text=f"Bouncing : {BOUNCING}\n", font=(
    "Helvetica", 12), fg="green" if BOUNCING else "red")
label_bouncing.grid(row=1, column=0, sticky="w")

label_forces = tkinter.LabelFrame(
    recap_label_frame, text="Forces :\n", font=("Helvetica", 12))
label_forces.grid(row=2, column=0, sticky="w")

label_alignment_forces = tkinter.Label(label_forces, text=f"Alignment multiplicator : {ALIGNMENT_FORCE_MULTIPLICATOR}\n", font=(
    "Helvetica", 12), fg="green" if ALIGNMENT_FORCE_MULTIPLICATOR else "red")
label_alignment_forces.grid(row=0, column=0, sticky="w")

label_cohesion_forces = tkinter.Label(label_forces, text=f"Cohesion multiplicator : {COHESION_FORCE_MULTIPLICATOR}\n", font=(
    "Helvetica", 12), fg="green" if COHESION_FORCE_MULTIPLICATOR else "red")
label_cohesion_forces.grid(row=1, column=0, sticky="w")

label_separation_forces = tkinter.Label(label_forces, text=f"Separation multiplicator : {SEPARATION_FORCE_MULTIPLICATOR}\n", font=(
    "Helvetica", 12), fg="green" if SEPARATION_FORCE_MULTIPLICATOR else "red")
label_separation_forces.grid(row=2, column=0, sticky="w")

labelframe_wind_forces = tkinter.LabelFrame(label_forces, text=f"Wind :\n", font=(
    "Helvetica", 12), fg="green" if WIND_SPEED else "red")
labelframe_wind_forces.grid(row=3, column=0, sticky="w")

label_wind_speed = tkinter.Label(
    labelframe_wind_forces, text=f"Wind speed : {WIND_SPEED}", font=("Helvetica", 12))
label_wind_speed.grid(row=0, column=0, sticky="w")

label_wind_direction = tkinter.Label(
    labelframe_wind_forces, text=f"Wind direction : {WIND_DIRECTION}", font=("Helvetica", 12))
label_wind_direction.grid(row=1, column=0, sticky="w")

labelframe_goal_forces = tkinter.LabelFrame(label_forces, text=f"Goal multiplicator : {GOAL_FORCE_MULTIPLICATOR}\n", font=(
    "Helvetica", 12), fg="green" if GOAL_FORCE_MULTIPLICATOR else "red")
labelframe_goal_forces.grid(row=4, column=0, sticky="w")

label_goal_position = tkinter.Label(
    labelframe_goal_forces, text=f"Goal : ({GOAL_X},{GOAL_Y})", font=("Helvetica", 12))
label_goal_position.grid(row=0, column=0, sticky="w")


def set_recap_labels():
    """Set the recap labels"""

    global NUMBER_OF_STEPS, label_max_iterations, label_bouncing, BOUNCING, label_alignment_forces, label_cohesion_forces,  \
        label_separation_forces, labelframe_wind_forces, label_wind_speed, WIND_SPEED, label_wind_direction, WIND_DIRECTION, \
        labelframe_goal_forces, label_goal_position, GOAL_X, GOAL_Y, ALIGNMENT_FORCE_MULTIPLICATOR, COHESION_FORCE_MULTIPLICATOR, \
        SEPARATION_FORCE_MULTIPLICATOR, GOAL_FORCE_MULTIPLICATOR

    if not NUMBER_OF_STEPS:
        label_max_iterations.config(text="Max iterations :  ∞")
    else:
        label_max_iterations.config(text=f"Max iterations: {NUMBER_OF_STEPS}")
    label_bouncing.config(
        text=f"Bouncing : {BOUNCING}\n", fg="green" if BOUNCING else "red")
    label_alignment_forces.config(
        text=f"Alignment multiplicator : {ALIGNMENT_FORCE_MULTIPLICATOR} \n", fg="green" if ALIGNMENT_FORCE_MULTIPLICATOR else "red")
    label_cohesion_forces.config(
        text=f"Cohesion multiplicator : {COHESION_FORCE_MULTIPLICATOR}\n", fg="green" if COHESION_FORCE_MULTIPLICATOR else "red")
    label_separation_forces.config(
        text=f"Separation : {SEPARATION_FORCE_MULTIPLICATOR}\n", fg="green" if SEPARATION_FORCE_MULTIPLICATOR else "red")
    labelframe_wind_forces.config(
        text=f"Wind\n", fg="green" if WIND_SPEED else "red")
    label_wind_speed.config(text=f"Wind speed : {WIND_SPEED}")
    label_wind_direction.config(text=f"Wind direction : {WIND_DIRECTION}")
    labelframe_goal_forces.config(
        text=f"Goal\n", fg="green" if GOAL_FORCE_MULTIPLICATOR else "red")
    label_goal_position.config(text=f"Goal : ({GOAL_X},{GOAL_Y})")


def disable_parameters_on_start():
    """Disable the parameters on start"""

    bouncing_checkbox.config(state="disable")
    number_of_boids_slider.config(state="disable")
    number_of_steps_spinbox.config(state="disable")
    # button_validate.config(state="disable")


def enable_parameters_on_reset():
    """Enable the parameters on reset"""

    bouncing_checkbox.config(state="normal")
    number_of_boids_slider.config(state="normal")
    number_of_steps_spinbox.config(state="normal")
    # button_validate.config(state="normal")


# ------------------------------------------------------------------------------
# Canvas
# ------------------------------------------------------------------------------
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, background='ivory')
canvas.grid(row=0, column=1, columnspan=2, sticky="")

# ------------------------------------------------------------------------------
# Pre-computing message label
# ------------------------------------------------------------------------------
label_warning = tkinter.Label(root, text="", font=("Helvetica", 12), fg="red")
label_warning.grid(row=1, column=1, columnspan=2, sticky="")

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def callback(event):
    """Click to place an obstacle
    Arguments:
        event {tkinter.Event} -- The event
    Returns:
        obstacle_x {int} -- The x position of the click
        obstacle_y {int} -- The y position of the click"""

    obstacle_x = event.x
    obstacle_y = event.y
    return obstacle_x, obstacle_y


def integrate_click(x, y):
    """Integrate the click to place an obstacle
    Arguments:
        x {int} -- The x position of the click
        y {int} -- The y position of the click"""

    global OBSTACLE, sim_space
    obstacle_x, obstacle_y = x, y
    if len(OBSTACLE) < 2:
        OBSTACLE.append((obstacle_x, obstacle_y))
    if len(OBSTACLE) == 2:
        if (OBSTACLE[0][0] < OBSTACLE[1][0] and OBSTACLE[0][1] < OBSTACLE[1][1]):
            sim_space.create_obstacle(
                OBSTACLE[0][0], OBSTACLE[0][1], OBSTACLE[1][0], OBSTACLE[1][1])
            create_obstacle_canvas(
                canvas, OBSTACLE[0][0], OBSTACLE[0][1], OBSTACLE[1][0], OBSTACLE[1][1])
        OBSTACLE = []


def integrate_right_click(x, y):
    """Use the right click position delete an obstacle
    Arguments:
        x {int} -- The x position of the click
        y {int} -- The y position of the click"""

    global sim_space
    for obstacle in sim_space.obstacles:
        if [x, y] in obstacle:
            sim_space.delete_obstacle(obstacle)
            delete_obstacle_canvas(canvas, obstacle)


def stock_simulation(simulation_space):
    """Stock the simulation
    Arguments:
        simulation_space {SimulationSpace} -- The simulation space"""

    global sim_space
    sim_space = simulation_space


def start_simulation(root, number_of_boids, width, height):
    """Start the simulation
    Arguments:
        root {tkinter.Tk} -- The root
        number_of_boids {int} -- The number of boids
        width {int} -- The width
        height {int} -- The height
    Returns:
        simulation_space {SimulationSpace} -- The simulation space"""

    # Create the simulation space
    simulation_space = boid.SimulationSpace(width, height)
    # Populate the simulation space
    simulation_space.populate(number_of_boids, space_fill="even")
    # Start the simulation
    simulation_space.start_simulation(number_of_steps=NUMBER_OF_STEPS)
    create_boids_canvas(canvas, simulation_space)
    # Start the simulation loop
    simulation_loop(root, canvas, simulation_space)
    return simulation_space


def create_boids_canvas(canvas, simulation_space):
    """Create the boids on the canvas
    Arguments:
        canvas {tkinter.Canvas} -- The canvas
        simulation_space {SimulationSpace} -- The simulation space"""

    for boid in simulation_space.boids:
        # Extract the boid's position
        x, y = boid.get_coords()
        # Create the boid on the canvas
        boid.canvas_item = canvas.create_oval(
            x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius, fill=boid.color)
        #boid.velocity_item = canvas.create_line(x, y, x + boid.velocity[0][0], y + boid.velocity[1][0], fill="red", width=2, arrow="last")
    if GOAL_FORCE_MULTIPLICATOR:
        canvas.goal_item = canvas.create_rectangle(
            GOAL_X-5, GOAL_Y-5, GOAL_X+5, GOAL_Y+5, fill="blue")


def create_obstacle_canvas(canvas, x0, y0, x1, y1):
    """Create the obstacle on the canvas
    Arguments:
        canvas {tkinter.Canvas} -- The canvas
        x0 {int} -- The x of the top left corner
        y0 {int} -- The y of the top left corner
        x1 {int} -- The x of the bottom right corner
        y1 {int} -- The y of the bottom right corner"""

    canvas.create_rectangle(x0, y0, x1, y1, fill="red")


def delete_obstacle_canvas(canvas, obstacle):
    """Delete the obstacle on the canvas
    Arguments:
        canvas {tkinter.Canvas} -- The canvas
        obstacle {list} -- The obstacle"""

    canvas.delete(obstacle)


def update_canvas(canvas, simulation_space):
    """Update the canvas
    Arguments:
        canvas {tkinter.Canvas} -- The canvas
        simulation_space {SimulationSpace} -- The simulation space"""

    for boid in simulation_space.boids:
        # Extract the boid's position
        x, y = boid.get_coords()
        # Update the boid on the canvas
        canvas.coords(boid.canvas_item, x - boid.radius, y -
                      boid.radius, x + boid.radius, y + boid.radius)
        canvas.itemconfig(boid.canvas_item, fill=boid.color)
        #canvas.coords(boid.velocity_item, x, y, x + boid.velocity[0][0], y + boid.velocity[1][0])
    if GOAL_FORCE_MULTIPLICATOR:
        canvas.coords(canvas.goal_item, GOAL_X-5, GOAL_Y-5, GOAL_X+5, GOAL_Y+5)


def clear_canvas(simulation_space, canvas):
    """Clear the canvas
    Arguments:
        simulation_space {SimulationSpace} -- The simulation space
        canvas {tkinter.Canvas} -- The canvas"""

    if simulation_space.finished:
        canvas.delete("all")
    else:
        print("The simulation is not finished")
        label_messages.config(text="The simulation is not finished", fg="red")
        label_messages.after(2000, lambda: label_messages.config(text=""))


def simulation_loop(root, canvas, simulation_space):
    global SIMULATION_SPEED
    """Simulation loop
    Arguments:
        root {tkinter.Tk} -- The root
        canvas {tkinter.Canvas} -- The canvas
        simulation_space {SimulationSpace} -- The simulation space"""

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
        label_iterations.config(
            text=f"Iterations : {simulation_space.iteration}")
        # Check if the simulation is finished
    # Continue the simulation loop
    root.after(SIMULATION_SPEED, lambda: simulation_loop(
        root, canvas, simulation_space))


def max_iterations_reached(simulation_space):
    """Check if the maximum number of iterations is reached
    Arguments:
        simulation_space {SimulationSpace} -- The simulation space
    Returns:
        bool -- True if the maximum number of iterations is reached, False otherwise"""

    if NUMBER_OF_STEPS == 0:
        return False
    return simulation_space.iteration >= NUMBER_OF_STEPS-1


def stop_simulation(simulation_space):
    """Stop the simulation
    Arguments:
        simulation_space {SimulationSpace} -- The simulation space"""

    simulation_space.finish_simulation()


def reset_simulation(simulation_space, canvas):
    """Reset the simulation
    Arguments:
        simulation_space {SimulationSpace} -- The simulation space
        canvas {tkinter.Canvas} -- The canvas"""

    stop_simulation(simulation_space)
    clear_canvas(simulation_space, canvas)
    # We clear the simulation space
    simulation_space.clear()
    label_iterations.config(text=f"Iterations : {simulation_space.iteration}")
    label_messages.after(2000, lambda: label_messages.config(text=""))


# ------------------------------------------------------------------------------
# Main loop
# ------------------------------------------------------------------------------
# the window is maximized
root.attributes("-fullscreen", True)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.mainloop()
