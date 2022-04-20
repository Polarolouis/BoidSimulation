import tkinter
import boid

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

WIDTH, HEIGHT = (800, 600)
NUMBER_OF_BOIDS = 20
NUMBER_OF_STEPS = 100

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
## Label number of iterations
label_iterations = tkinter.Label(top_frame, text=f"Iterations : {0}", font=("Helvetica", 16))
label_iterations.pack(side=tkinter.RIGHT)

# Bottom Frame
bottom_frame = tkinter.Frame(root)
bottom_frame.pack(side=tkinter.BOTTOM, fill=tkinter.X)
## Button to start the simulation
button_start = tkinter.Button(bottom_frame, text="Start", font=("Helvetica", 16), command=lambda: start_simulation(root, NUMBER_OF_BOIDS, WIDTH, HEIGHT))
button_start.pack(side=tkinter.LEFT)
## Button to stop the simulation
button_stop = tkinter.Button(bottom_frame, text="Stop", font=("Helvetica", 16), command=lambda: stop_simulation(root))
button_stop.pack(side=tkinter.RIGHT)
## Button to reset the simulation
button_reset = tkinter.Button(bottom_frame, text="Reset", font=("Helvetica", 16), command=lambda: reset_simulation(root, NUMBER_OF_BOIDS, WIDTH, HEIGHT))
button_reset.pack(side=tkinter.RIGHT)

#------------------------------------------------------------------------------
# Canvas
#------------------------------------------------------------------------------
canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, background='ivory')
canvas.pack()

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------

def start_simulation(root, number_of_boids, width, height):
    """Start the simulation"""
    # Create the simulation space
    simulation_space = boid.SimulationSpace(width, height)
    # Populate the simulation space
    simulation_space.populate(number_of_boids)
    # Start the simulation
    simulation_space.start_simulation(number_of_steps=NUMBER_OF_STEPS)
    create_boids_canvas(canvas, simulation_space)
    # Start the simulation loop
    simulation_loop(root, canvas, simulation_space)

def create_boids_canvas(canvas, simulation_space):
    """Create the boids on the canvas"""
    for boid in simulation_space.boids:
        # Extract the boid's position
        x, y = boid.get_coords()
        # Create the boid on the canvas
        boid.canvas_item = canvas.create_oval(x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius, fill="black")

def update_canvas(canvas, simulation_space):
    """Update the canvas"""
    for boid in simulation_space.boids:
        # Extract the boid's position
        x, y = boid.get_coords()
        # Update the boid on the canvas
        canvas.coords(boid.canvas_item, x - boid.radius, y - boid.radius, x + boid.radius, y + boid.radius)

def simulation_loop(root, canvas, simulation_space):
    """Simulation loop"""
    # Update the simulation
    simulation_space.next_step()
    # Update the canvas
    update_canvas(canvas, simulation_space)
    # Check if the simulation is finished
    if simulation_space.finished:
        return
    # Check if the simulation is paused
    if simulation_space.paused:
        pass
    # Continue the simulation loop
    root.after(10, lambda: simulation_loop(root, canvas, simulation_space))


#------------------------------------------------------------------------------
# Main loop
#------------------------------------------------------------------------------
root.mainloop()