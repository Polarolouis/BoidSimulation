import tkinter
import boid as bd

window = tkinter.Tk()
window.title("Boid Simulation")

size = 500
space = bd.SimulationSpace(size, size)
space.populate(200, bouncing=False)

window.configure(width=size, height=size)
space.canvas = tkinter.Canvas(window, width=size, height=size)
space.canvas.pack()

for boid in space.boids:
    boid.near_canvas_id = space.canvas.create_oval(boid.x_pos - boid.near_distance, boid.y_pos - boid.near_distance, boid.x_pos + boid.near_distance, boid.y_pos + boid.near_distance, fill="", outline="gray")
    boid.canvas_id = space.canvas.create_line(boid.x_pos, boid.y_pos, boid.x_pos+boid.x_vel, boid.y_pos+boid.y_vel, fill="red", width=5, arrow=tkinter.LAST)
def move_boid_canvas(space):
    """Move the boid canvas and update the position"""
    for boid in space.boids:
        space.canvas.coords(boid.near_canvas_id, boid.x_pos - boid.near_distance, boid.y_pos - boid.near_distance, boid.x_pos + boid.near_distance, boid.y_pos + boid.near_distance)
        space.canvas.coords(boid.canvas_id, boid.x_pos, boid.y_pos, boid.x_pos+boid.x_vel, boid.y_pos+boid.y_vel)
    
    window.after(10, lambda: (space.next_step(), move_boid_canvas(space)))
space.canvas.after(10, lambda: (space.next_step(),move_boid_canvas(space)) )
window.mainloop()