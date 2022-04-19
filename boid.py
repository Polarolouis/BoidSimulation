import math
import random
import tkinter

class Boid:
    """Boid class"""
    near_distance = 50 # Distance to be considered near
    def __init__(self, x_pos, y_pos, speed, angle, width, height):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.angle = angle
        self.width = width
        self.height = height
        self.x_vel = self.speed * math.cos(self.angle)
        self.y_vel = self.speed * math.sin(self.angle)
        self.radius = 5

        self.near_boids = []
    
    def update_velocity(self):
        """Update the velocity of the boid"""
        # Cohesion behaviour
        self.cohesion()

        # Collision avoidance behaviour
        self.avoid_collision()
        
        # Separation behaviour
        self.separation()
        
        # Update the velocity
        if random.random()<1e-5:
            self.angle = random.random()*360
        self.x_vel = self.speed * math.cos(self.angle)
        self.y_vel = self.speed * math.sin(self.angle)

    def cohesion(self):
        """Cohesion behaviour to move towards the average position of the boids"""
        # Calculate the average velocity of the boids
        x_vel_avg = 0
        y_vel_avg = 0
        for boid in self.near_boids:
            x_vel_avg += boid.x_vel
            y_vel_avg += boid.y_vel
        x_vel_avg /= len(self.near_boids)
        y_vel_avg /= len(self.near_boids)
        
        # Calculate the average position of the boids
        x_pos_avg = 0
        y_pos_avg = 0
        for boid in self.near_boids:
            x_pos_avg += boid.x_pos
            y_pos_avg += boid.y_pos
        x_pos_avg /= len(self.near_boids)
        y_pos_avg /= len(self.near_boids)
        
        # Calculate the average angle of the boids
        angle_avg = 0
        for boid in self.near_boids:
            angle_avg += boid.angle
        angle_avg /= len(self.near_boids)
        
        # Calculate the new velocity
        self.x_vel += (x_vel_avg - self.x_vel) / 2
        self.y_vel += (y_vel_avg - self.y_vel) / 2
        self.angle += (angle_avg - self.angle) / 2

    
    def avoid_collision(self):
        """Avoid collision behaviour"""
        for boid in self.near_boids:
            if self.distance(boid) < self.radius * 4:
                self.x_vel += (boid.x_vel - self.x_vel) / 2
                self.y_vel += (boid.y_vel - self.y_vel) / 2
                self.angle += (boid.angle - self.angle) / 2
    
    def separation(self):
        """Separation behaviour"""
        for boid in self.near_boids:
            if self.distance(boid) < self.radius * 2:
                self.x_vel += (boid.x_pos - self.x_pos) / 2
                self.y_vel += (boid.y_pos - self.y_pos) / 2
                self.angle += (boid.angle - self.angle) / 2

    def update_position(self):
        """Update the position of the boid"""
        # statement to check if the boid is out of bounds
        # and bounce it back if it is
        if self.x_pos + self.x_vel > self.width:
            self.x_pos = 0
            self.x_vel = self.x_vel
        elif self.x_pos + self.x_vel < 0:
            self.x_pos = self.width
            self.x_vel = self.x_vel
        
        if self.y_pos + self.y_vel > self.height:
            self.y_pos = 0
            self.y_vel = self.y_vel
        elif self.y_pos + self.y_vel < 0:
            self.y_pos = self.height
            self.y_vel = self.y_vel
        
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
    
    def find_near_boids(self, boids, distance):
        """Sets a list of boids that are within a certain distance"""
        near_boids = []
        for boid in boids:
            if self.distance(boid) < distance:
                near_boids.append(boid)
        self.near_boids = near_boids
    
    def distance(self, boid):
        """Return the distance between two boids"""
        return math.sqrt((self.x_pos - boid.x_pos)**2 + (self.y_pos - boid.y_pos)**2)

class SimulationSpace:
    """Simulation space class"""
    def __init__(self, width, height):
        """Initialize the simulation space"""
        self.width = width
        self.height = height
        self.boids = []
    
    def populate(self, number_of_boids):
        """Populate the simulation space with boids"""
        for i in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            speed = 9
            angle = random.randint(0, 360)
            boid = Boid(x_pos, y_pos, speed, angle, self.width, self.height)
            self.boids.append(boid)
    
    def next_step(self):
        """Update the simulation space"""
        for boid in self.boids:
            boid.find_near_boids(self.boids, boid.near_distance)
            boid.update_velocity()
            boid.update_position()

window = tkinter.Tk()
window.title("Boid Simulation")

size = 500
space = SimulationSpace(size, size)
space.populate(200)

window.configure(width=size, height=size)
space.canvas = tkinter.Canvas(window, width=size, height=size)
space.canvas.pack()

for boid in space.boids:
    boid.canvas_id = space.canvas.create_oval(boid.x_pos - boid.radius, boid.y_pos - boid.radius, boid.x_pos + boid.radius, boid.y_pos + boid.radius, fill="black")
    boid.near_canvas_id = space.canvas.create_oval(boid.x_pos - boid.near_distance, boid.y_pos - boid.near_distance, boid.x_pos + boid.near_distance, boid.y_pos + boid.near_distance, fill="red")
    
def move_boid_canvas(space):
    """Move the boid canvas and update the position"""
    for boid in space.boids:
        space.canvas.coords(boid.canvas_id, boid.x_pos - boid.radius, boid.y_pos - boid.radius, boid.x_pos + boid.radius, boid.y_pos + boid.radius)
    window.after(10, lambda: (space.next_step(), move_boid_canvas(space)))
space.canvas.after(10, lambda: (space.next_step(),move_boid_canvas(space)) )
window.mainloop()