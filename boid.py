import math
import random
import numpy as np

class Boid:
    """Boid class"""
    radius = 5
    near_distance = 10*radius # Distance to be considered near
    chaotic_probability = 0
    weight_of_cohesion = 1
    max_speed = 5
    max_separation_force = 1
    max_cohesion_force = 1
    
    
    def __init__(self, x_pos, y_pos, x_vel, y_vel, width, height, bouncing, alignment_bool = True, 
                cohesion_bool = True, separation_bool = True, wind_bool = True, wind_speed = 0, wind_direction = 0, the_chosen_one = False):
        # Initialise the boid position and velocity
        self.position = np.array([[x_pos], [y_pos]], dtype=np.float64)
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)
        self.acceleration = np.array([[0], [0]], dtype=np.float64)

        self.width = width
        self.height = height

        self.bouncing = bouncing

        self.near_boids = []   

        self.alignment_bool = alignment_bool
        self.cohesion_bool = cohesion_bool
        self.separation_bool = separation_bool
        self.wind_bool = wind_bool
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction * 2 * math.pi / 360
        self.the_chosen_one = the_chosen_one

# Flock calculation
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance"""
        self.near_boids = []
        for boid in boids:
            if (not np.array_equal(self.position, boid.position)) and (boid not in self.near_boids) and self.distance(boid) < self.near_distance:
                self.near_boids.append(boid)
                boid.near_boids.append(self)

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
                position_avg += boid.position #* self.distance(boid)**2
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
            diff /= distance_to_boid
            separation_correction += diff
        if self.near_boids:
            separation_correction /= len(self.near_boids)
        # if np.linalg.norm(separation_correction) > self.max_speed:
        #     separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_speed
        # if np.linalg.norm(separation_correction) > self.max_separation_force:
        #     separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_separation_force
        return separation_correction

    def wind(self):
        """Apply wind to the boid"""
        x_wind_speed = self.wind_speed * math.cos(self.wind_direction)
        y_wind_speed = self.wind_speed * math.sin(self.wind_direction)
        
        # Prevent wind speed from exceeding max speed
        if np.linalg.norm(np.array([[x_wind_speed], [y_wind_speed]])) > self.max_speed:
            x_wind_speed = x_wind_speed / np.linalg.norm(np.array([[x_wind_speed], [y_wind_speed]])) * self.max_speed
            y_wind_speed = y_wind_speed / np.linalg.norm(np.array([[x_wind_speed], [y_wind_speed]])) * self.max_speed
        return np.array([[x_wind_speed],[y_wind_speed]], dtype=np.float64)

    def apply_rules(self):
        """Apply the rules of the flock to the boid"""
        if self.the_chosen_one:
            print("The chosen one : " + str(self.position))
        if self.alignment_bool:
            alignment = self.alignment()
            if self.the_chosen_one:
                print("Alignment: " + str(np.linalg.norm(alignment)))
            self.acceleration += alignment

        
        if self.cohesion_bool:
            cohesion = self.cohesion()
            if self.the_chosen_one:
                print("Cohesion: " + str(np.linalg.norm(cohesion)))
            self.acceleration += cohesion
        
        if self.separation_bool:
            separation = self.separation()
            if self.the_chosen_one:
                print("Separation: " + str(np.linalg.norm(separation)))
            self.acceleration += separation
        
        if self.wind_bool:
            wind = self.wind()
            if self.the_chosen_one:
                print("Wind: " + str(np.linalg.norm(wind)))
            self.acceleration += wind
        
        if self.the_chosen_one:
            print("Acceleration: " + str(np.linalg.norm(self.acceleration)))

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

        # If the boid is out of space, bring it back to space
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
        
    
    def populate(self, number_of_boids, alignment_bool, cohesion_bool, separation_bool, wind_bool, wind_speed, wind_direction, bouncing=True):
        """Populate the simulation space with boids"""
        for _ in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            x_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            y_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            boid = Boid(x_pos, y_pos, x_vel, y_vel, self.width, self.height, bouncing=bouncing, 
                alignment_bool=alignment_bool, cohesion_bool=cohesion_bool, separation_bool=separation_bool, 
                wind_bool=wind_bool, wind_speed=wind_speed, wind_direction=wind_direction, the_chosen_one=True if _ == 0 else False)
            self.boids.append(boid)
    
    def next_step(self):
        """Update the simulation space"""
        print(f"-------------------------\nSpace {self.counter} | Iteration : {self.iteration}\n-------------------------------" )
        self.iteration += 1
        for boid in self.boids:
            boid.find_near_boids(self.boids)
            boid.update()
    
    def distances_matrix(self):
        """Returns the distances matrix"""
        distances = np.zeros((len(self.boids), len(self.boids)))
        N = len(self.boids)
        iteration = 0
        for i, boid_i in enumerate(self.boids):
            for j, boid_j in enumerate(self.boids):
                iteration += 1
                print(f"Space {self.counter} | Iteration : {iteration}")
                distances[i, j] = np.linalg.norm(boid_i.position - boid_j.position)
                distances[j, i] = distances[i, j]
                if (distances + np.eye(N=N, M=N)).all() != 0:
                    break
        return distances

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
