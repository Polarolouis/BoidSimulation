import math
import random
import numpy as np

class Boid:
    """Boid class"""
    near_distance = 25 # Distance to be considered near
    chaotic_probability = 0
    weight_of_cohesion = 1
    max_speed = 5
    max_separation_force = 1
    max_cohesion_force = 0.75*max_separation_force
    
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
        heading_correction = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids:
            heading_avg = np.array([[0], [0]], dtype=np.float64)
            for boid in self.near_boids:
                heading_avg += boid.velocity
                heading_avg /= len(self.near_boids)
            heading_correction = heading_avg - self.velocity
            if np.linalg.norm(heading_correction) > self.max_speed:
                heading_correction = heading_correction / np.linalg.norm(heading_correction) * self.max_speed
        return heading_correction

    def cohesion(self):
        """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
        Returns : the correction to add to the velocity""" 
        # Calculate the average position of the boids
        correction_to_avg = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids:
            position_avg = np.array([[0], [0]], dtype=np.float64)
            for boid in self.near_boids:
                position_avg += boid.position
            position_avg /= len(self.near_boids)
            correction_to_avg = position_avg - self.position
            if np.linalg.norm(correction_to_avg) > self.max_speed:
                correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_speed
            if np.linalg.norm(correction_to_avg) > self.max_cohesion_force:
                correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_cohesion_force
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
        if np.linalg.norm(separation_correction) > self.max_speed:
            separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_speed
        if np.linalg.norm(separation_correction) > self.max_separation_force:
            separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_separation_force
        return separation_correction

    def apply_force(self, force):
        """Apply a force to the boid by incrementing the acceleration"""
        self.acceleration += force

    def apply_rules(self):
        """Apply the rules of the flock to the boid"""
        self.apply_force(self.alignment())
        self.apply_force(self.cohesion())
        self.apply_force(self.separation())

    def check_edges(self):
        """Check if the boid is out of bounds"""
        # If bouncing is on, bounce the boid back into the screen
        if self.bouncing:
            velocity = self.velocity
            if self.position[0] + self.velocity[0] < self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[0] + self.velocity[0] > self.width - self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[1] + self.velocity[1] < self.radius:
                velocity[1] = -self.velocity[1]
            if self.position[1] + self.velocity[1] > self.height - self.radius:
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

    def is_out_of_space(self):
        """Check if the boid is out of space"""
        if self.position[0] < 0 or self.position[0] > self.width or self.position[1] < 0 or self.position[1] > self.height:
            return True
        else:
            return False
    
    def bring_back_to_space(self):
        """Bring the boid back to space"""
        if self.is_out_of_space():
            self.position[0] =  self.width / 2
            self.position[1] = self.height / 2
            return True

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

        # If velocity exceeds the max speed, set it to the max speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        # Update the position
        self.position += self.velocity

        self.bring_back_to_space()

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
    """Class for the simulation space"""
    counter = 0
    def __init__(self, width, height):
        """Initialize the simulation space"""
        self.width = width
        self.height = height
        self.boids = []
        self.iteration = 0
        self.paused = True
        self.finished = False
        self.number_of_steps = 10
        self.counter = SimulationSpace.counter
        SimulationSpace.counter += 1
        
    
    def populate(self, number_of_boids, bouncing=True):
        """Populate the simulation space with boids"""
        for _ in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            x_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            y_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            boid = Boid(x_pos, y_pos, x_vel, y_vel, self.width, self.height, bouncing=bouncing)
            self.boids.append(boid)
    
    def next_step(self):
        """Update the simulation space"""
        print(f"Space {self.counter} | Iteration : {self.iteration}" )
        self.iteration += 1
        for boid in self.boids:
            boid.find_near_boids(self.boids)
            boid.update()

# Method to control the state of the simulation   
    def start_simulation(self, number_of_steps=10):
        """Start the simulation"""
        self.paused = False
        self.number_of_steps = number_of_steps
        self.finished = False

    def toggle_pause(self):
        """Toggle the pause state of the simulation"""
        self.paused = not self.paused

    def finish_simulation(self):
        """Finish the simulation"""
        self.finished = True

# Method to clear the simulation space
    
    def clear(self):
        """Reset the simulation"""
        self.boids = []
        self.iteration = 0
        self.paused = True
        self.finished = False