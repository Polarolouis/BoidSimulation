import time
import tkinter
import boid

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

WIDTH, HEIGHT = (800, 600)
NUMBER_OF_BOIDS = 20
NUMBER_OF_STEPS = 10_000
BOUNCING = True

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
button_start = tkinter.Button(bottom_frame, text="Start", font=("Helvetica", 16), command=lambda: (stock_simulation((start_simulation(root, NUMBER_OF_BOIDS, WIDTH, HEIGHT))), button_start.config(state="disable"), button_reset.config(state="normal"), button_pause.config(state="normal")))
button_start.pack(side=tkinter.LEFT)
## Button to pause the simulation
button_pause = tkinter.Button(bottom_frame, text="Pause/Resume", font=("Helvetica", 16), command=lambda: (sim_space.toggle_pause(), label_messages.config(text="Simulation paused" if sim_space.paused else "", fg="red")))
button_pause.config(state="disable")
button_pause.pack(side=tkinter.LEFT)
## Button to reset the simulation
button_reset = tkinter.Button(bottom_frame, text="Reset", font=("Helvetica", 16), command=lambda: (reset_simulation(sim_space, canvas), button_start.config(state="normal"), button_reset.config(state="disable"), button_pause.config(state="disable"), label_messages.config(text="")))
button_reset.config(state="disable")
button_reset.pack(side=tkinter.RIGHT)

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
    simulation_space.populate(number_of_boids, bouncing=BOUNCING)
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
        boid.canvas_item = canvas.create_oval(x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius, fill="black")

def update_canvas(canvas, simulation_space):
    """Update the canvas"""
    for index, boid in enumerate(simulation_space.boids):
        # Extract the boid's position
        x, y = boid.get_coords()
        # Update the boid on the canvas
        canvas.coords(boid.canvas_item, x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius)

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
root.mainloop()