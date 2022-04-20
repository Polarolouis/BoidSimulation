import math
import random
import numpy as np

class Boid:
    """Boid class"""
    near_distance = 50 # Distance to be considered near
    chaotic_probability = 0
    weight_of_cohesion = 1
    def __init__(self, x_pos, y_pos, x_vel, y_vel, width, height, bouncing):
        # Initialise the boid position and velocity
        self.position = np.array([[x_pos], [y_pos]], dtype=np.float64)
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)
        self.acceleration = np.array([[0], [0]], dtype=np.float64)

        self.width = width
        self.height = height

        self.radius = 5
        self.bouncing = bouncing

        self.near_boids = []   

# Flock calculation
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance"""
        self.near_boids = []
        for boid in boids:
            if (not np.array_equal(self.position, boid.position)) and self.distance(boid) < self.near_distance:
                self.near_boids.append(boid)

    def distance(self, other_boid):
        """Return the distance between two boids"""
        return np.linalg.norm(self.position - other_boid.position)

# Flock behaviour
    def alignment(self):
        """Alignment behaviour to steer towards the average heading of the boids in the near_boids list
        Returns : the correction to add to the velocity""" 
        # Calculate the average heading of the boids
        heading_avg = np.array([[0], [0]], dtype=np.float64)
        for boid in self.near_boids:
            heading_avg += boid.velocity
        if self.near_boids:
            heading_avg /= len(self.near_boids)
        heading_correction = heading_avg - self.velocity
        return heading_correction

    def cohesion(self):
        """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
        Returns : the correction to add to the velocity""" 
        # Calculate the average position of the boids
        position_avg = np.array([[0], [0]], dtype=np.float64)
        for boid in self.near_boids:
            position_avg += boid.position
        if self.near_boids:
            position_avg /= len(self.near_boids)
        correction_to_avg = position_avg - self.position
        return correction_to_avg

    def separation(self):
        """Separation behaviour to avoid collisions with other boids
        Returns : the correction to add to the velocity"""
        separation_correction = np.array([[0], [0]], dtype=np.float64)
        for boid in self.near_boids:
            distance_to_boid = self.distance(boid)
            diff = np.asarray(self.position - boid.position, dtype=np.float64)
            np.divide(diff, np.asarray(distance_to_boid, dtype=np.float64), out=diff)
            separation_correction += diff
        if self.near_boids:
            separation_correction /= len(self.near_boids)
        return separation_correction

    def apply_force(self, force):
        """Apply a force to the boid by incrementing the acceleration"""
        self.acceleration += force

    def apply_rules(self):
        """Apply the rules of the flock to the boid"""
        self.apply_force(self.separation())
        self.apply_force(self.alignment())
        self.apply_force(self.cohesion())

    def check_edges(self):
        """Check if the boid is out of bounds"""
        # If bouncing is on, bounce the boid back into the screen
        if self.bouncing:
            velocity = self.velocity
            if self.position[0] < self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[0] > self.width - self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[1] < self.radius:
                velocity[1] = -self.velocity[1]
            if self.position[1] > self.height - self.radius:
                velocity[1] = -self.velocity[1]
            return velocity
        else:
            # If bouncing is off, check if the boid is out of bounds
            # And if it is, set the boid to the opposite side
            position = self.position
            if self.position[0] < self.radius:
                position[0] = self.width - self.radius
            if self.position[0] > self.width - self.radius:
                position[0] = self.radius
            if self.position[1] < self.radius:
                position[1] = self.height - self.radius
            if self.position[1] > self.height - self.radius:
                position[1] = self.radius
            return position

# Update the boid
    def update(self):
        """Update the velocity and the position of the boid"""
        # We need to have found the near_boids list before we can apply the rules
        self.apply_rules()
        # The acceleration is the sum of the forces

        # Update the velocity
        self.velocity += self.acceleration
        
        # Check if the boid is out of bounds and apply the correction
        if self.bouncing:
            # If we bounce the output is the velocity
            self.velocity = self.check_edges()
        else:
            # If we don't bounce the output is the position
            self.position = self.check_edges()

        # Update the position
        self.position += self.velocity

        # Reset the acceleration
        self.acceleration = np.array([[0], [0]], dtype=np.float64)

# Methods for the display
    def get_coords(self):
        """Returns the coordinates of the boid"""
        x_pos, y_pos = self.position
        return (*x_pos, *y_pos) # unpacking the tuple

    def get_velocity(self):
        """Returns the velocity of the boid"""
        x_vel, y_vel = self.velocity
        return (*x_vel, *y_vel)

    def bbox(self):
        """Returns the bounding box of the boid"""
        x_pos, y_pos = self.position
        return (x_pos - self.radius, y_pos - self.radius, x_pos + self.radius, y_pos + self.radius)

class SimulationSpace:
    """Simulation space class"""
    def __init__(self, width, height):
        """Initialize the simulation space"""
        self.width = width
        self.height = height
        self.boids = []
        self.iteration = 0
    
    def populate(self, number_of_boids, bouncing=True):
        """Populate the simulation space with boids"""
        for _ in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            x_vel = 0.01 # random.randint(1, 5)
            y_vel = 0.01 # random.randint(1, 5)
            boid = Boid(x_pos, y_pos, x_vel, y_vel, self.width, self.height, bouncing=bouncing)
            self.boids.append(boid)
    
    def next_step(self):
        """Update the simulation space"""
        self.iteration += 1
        for boid in self.boids:
            boid.find_near_boids(self.boids)
            boid.update()