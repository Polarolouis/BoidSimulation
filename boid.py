# %%
import math
import random
import numpy as np
#%% 
class Boid:
    """Boid class"""
    radius = 5
    near_distance_alignment = 10*radius # Distance to be considered near
    near_distance_cohesion = 0.5*near_distance_alignment
    near_distance_separation = 4*radius
    chaotic_probability = 0.1
    
    alignment_force = 1
    cohesion_force = 1
    separation_force = 1
    goal_force = 1

    max_speed = 5
    max_alignment_force = 1
    max_cohesion_force = 1
    max_separation_force = 1
    max_goal_force = 1
    
    
    
    def __init__(self, x_pos, y_pos, x_vel, y_vel, bouncing, wind_speed = 0, 
                wind_direction = 0, the_chosen_one = False):
        # Initialise the boid position and velocity
        self.position = np.array([[x_pos], [y_pos]], dtype=np.float64)
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)
        self.acceleration = np.array([[0], [0]], dtype=np.float64)
        self.new_acceleration = np.array([[0], [0]], dtype=np.float64)

        self.bouncing = bouncing

        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []

        self.wind_speed = wind_speed
        self.wind_direction = wind_direction * 2 * math.pi / 360
        self.the_chosen_one = the_chosen_one
        self.color = "green" if self.the_chosen_one else "grey"
        self.boids_rate = 0

    @classmethod
    def set_width(cls, width):
        """Set the width of the space"""
        cls.width = width

    @classmethod
    def set_height(cls, height):
        """Set the height of the space"""
        cls.height = height
    
    @classmethod
    def set_force_parameters(cls, alignment_force, cohesion_force, separation_force, goal_force):
        """Set the force parameters"""
        cls.alignment_force = alignment_force
        cls.cohesion_force = cohesion_force
        cls.separation_force = separation_force
        cls.goal_force = goal_force
    
    @classmethod
    def set_goal_position(cls, goal_x, goal_y):
        """Set the goal position"""
        cls.goal_position = np.array([[goal_x], [goal_y]], dtype=np.float64)

# Flock calculation
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance"""
        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []

        filtered_boids = (boid for boid in boids if (not np.array_equal(self.position, boid.position)) and ((self.position[0] - self.near_distance_alignment < boid.position[0] and self.position[1] - self.near_distance_alignment < boid.position[1]) and (self.position[0] + self.near_distance_alignment > boid.position[0] and self.position[1] + self.near_distance_alignment > boid.position[1])))
        for boid in filtered_boids:
            dist = np.linalg.norm(self.position - boid.position)
            if (boid not in self.near_boids_alignment) and dist < self.near_distance_alignment and dist > self.near_distance_cohesion:
                self.near_boids_alignment.append((boid, dist))
                boid.near_boids_alignment.append((self, dist))
            
            if (boid not in self.near_boids_cohesion) and dist < self.near_distance_cohesion and dist > self.near_distance_separation:
                self.near_boids_cohesion.append((boid, dist))
                boid.near_boids_cohesion.append((self, dist))
            
            if (boid not in self.near_boids_separation) and dist < self.near_distance_separation:
                self.near_boids_separation.append((boid, dist))
                boid.near_boids_separation.append((self, dist))

    def distance(self, other_boid):
        """Return the distance between two boids"""
        return np.linalg.norm(self.position - other_boid.position)


# Flock behaviour
    def alignment(self):
        """Alignment behaviour to steer towards the average heading of the boids in the near_boids list
        Returns : the correction to add to the velocity""" 
        # Calculate the average heading of the boids
        heading_correction = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_alignment:            
            # Taking the the fastest boid as a leader
            heading_correction = max(self.near_boids_alignment, key=lambda boid_and_distance: np.linalg.norm(boid_and_distance[0].velocity))[0].velocity
            # for boid in self.near_boids:
            #     heading_avg += boid.velocity
            #     heading_avg /= len(self.near_boids)
            # heading_correction = heading_avg - self.velocity
        if np.linalg.norm(heading_correction):
            heading_correction = heading_correction / np.linalg.norm(heading_correction) * self.max_speed
        
        if np.linalg.norm(heading_correction) > self.max_alignment_force:
            heading_correction = heading_correction / np.linalg.norm(heading_correction) * self.max_alignment_force
        return heading_correction * Boid.alignment_force

    def cohesion(self):
        """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
        Returns : the correction to add to the velocity""" 
        # Calculate the average position of the boids
        correction_to_avg = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_cohesion:
            position_avg = np.array([[0], [0]], dtype=np.float64)
            for boid, distance in self.near_boids_cohesion:
                position_avg += boid.position #* self.distance(boid)**2
            position_avg /= len(self.near_boids_cohesion)
            correction_to_avg = position_avg - self.position
            if np.linalg.norm(correction_to_avg):
                correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_speed
        if np.linalg.norm(correction_to_avg) > self.max_cohesion_force:
            correction_to_avg = correction_to_avg / np.linalg.norm(correction_to_avg) * self.max_cohesion_force
        return correction_to_avg * Boid.cohesion_force

    def separation(self):
        """Separation behaviour to avoid collisions with other boids
        Returns : the correction to add to the velocity"""
        separation_correction = np.array([[0], [0]], dtype=np.float64)
        for boid, distance in self.near_boids_separation:
            diff = self.position - boid.position
            diff /= distance
            separation_correction += diff
        if self.near_boids_separation:
            separation_correction /= len(self.near_boids_separation)
        # if np.linalg.norm(separation_correction) > 0:
        #     separation_correction = separation_correction / np.linalg.norm(separation_correction) * self.max_speed
        if np.linalg.norm(separation_correction):
            separation_correction = (separation_correction / np.linalg.norm(separation_correction)) * self.max_separation_force
        
        return separation_correction * Boid.separation_force

    def wind(self):
        """Apply wind to the boid"""
        x_wind_speed = self.wind_speed * math.cos(self.wind_direction)
        y_wind_speed = self.wind_speed * math.sin(self.wind_direction)

        return np.array([[x_wind_speed],[y_wind_speed]], dtype=np.float64)

    def goal(self):
        """Apply goal force to the boid"""
        goal_force = np.array([[0], [0]], dtype=np.float64)
        if self.goal_position is not None:
            goal_force = self.goal_position - self.position
            
            # Distance based coefficient
            goal_force *= np.linalg.norm(goal_force)

            if np.linalg.norm(goal_force) > self.max_goal_force:
                goal_force = goal_force / np.linalg.norm(goal_force) * self.max_goal_force
        return goal_force * Boid.goal_force

    def apply_rules(self):
        """Apply the rules of the flock to the boid"""
        if self.the_chosen_one:
            print("The chosen one : " + str(self.position))

        if self.cohesion_force > 0:
            cohesion = self.cohesion()
            if self.the_chosen_one:
                print("Cohesion: " + str(np.linalg.norm(cohesion)))
            self.acceleration += cohesion
        
        if self.separation_force > 0:
            separation = self.separation()
            if self.the_chosen_one:
                print("Separation: " + str(np.linalg.norm(separation)))
            self.acceleration += separation
        
        if self.wind_speed > 0:
            wind = self.wind()
            if self.the_chosen_one:
                print("Wind: " + str(np.linalg.norm(wind)))
            self.acceleration += wind

        if self.alignment_force > 0:
            alignment = self.alignment()
            if self.the_chosen_one:
                print("Alignment: " + str(np.linalg.norm(alignment)))
            self.acceleration += alignment

        if self.goal_force > 0:
            goal = self.goal()
            if self.the_chosen_one:
                print("Goal: " + str(np.linalg.norm(goal)))
            self.acceleration += goal

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

# Functions to color the boid according to the surrounding density
    def calculate_near_boids_number(self):
        """Calculate the number of boids near the boid"""
        return len(self.near_boids_cohesion) + len(self.near_boids_separation)
    
    def update_color_boids_rate(self):
        """Update the color of the boid based on the density of the boids near it"""
        boids_rate = self.boids_rate
        def rgb_hack(rgb):
            return "#%02x%02x%02x" % rgb
        red = 255
        green = 255 - int(boids_rate * 255)
        blue = 255 - int(boids_rate * 255)
        self.color = rgb_hack((red, green, blue))

    def set_boids_rate(self, boids_rate):
        """Set the density of the boids near the boid"""
        self.boids_rate = boids_rate

# Functions for the collision with obstacles

    def reverse_velocity(self):
        """Reverse the velocity of the boid"""
        self.velocity *= -1

    # def can_reach_obstacle(self, obstacle):
    #     """Check if the boid can reach the obstacle
    #     Returns:
    #         True if it can reach the obstacle, False otherwise"""
    #     x_boid, y_boid = self.get_coords()
    #     x_boid_velocity, y_boid_velocity = self.get_velocity()
    #     (x0_obstacle, x1_obstacle),  (y0_obstacle, y1_obstacle) = obstacle.get_coords()
    #     x_collision, y_collision = True, True
    #     # If x_boid_velocity is positive, the boid is moving to the right
    #     if x_boid_velocity > 0:
    #         # Can reach the obstacle if we can pass the x0_obstacle
    #         x_collision = x0_obstacle < x_boid + x_boid_velocity
    #     # If x_boid_velocity is negative, the boid is moving to the left
    #     else:
    #         # Can reach the obstacle if we can pass the x1_obstacle
    #         x_collision = x1_obstacle > x_boid + x_boid_velocity
        
    #     # If y_boid_velocity is positive, the boid is moving down
    #     if y_boid_velocity > 0:
    #         # Can reach the obstacle if we can pass the y0_obstacle
    #         y_collision = y0_obstacle < y_boid + y_boid_velocity
    #     # If y_boid_velocity is negative, the boid is moving up
    #     else:
    #         # Can reach the obstacle if we can pass the y1_obstacle
    #         y_collision = y1_obstacle > y_boid + y_boid_velocity
    #     return x_collision and y_collision
            
            
        
    # def bounce_if_collision(self, obstacle):
    #     """Check if the boid collides with the obstacle
    #     Returns:
    #         True if the boid collides with the obstacle, False otherwise"""
    #     (x0, x1), (y0, y1) = obstacle.get_coords()

    #     # If the x_velocity is positive, the boid is moving to the right
    #     if self.velocity[0] > 0:
    #         # If we would pass the left side, reverse the x velocity
    #         if self.position[0] + self.velocity[0] > x0:
    #             self.velocity[0] *= -1
    #     else: # The boid is moving left
    #         # If we would pass the right side, reverse the x velocity
    #         if self.position[0] + self.velocity[0] < x1:
    #             self.velocity[0] *= -1
    #     # If the y_velocity is positive, the boid is moving down
    #     if self.velocity[1] > 0:
    #         # If we would pass the top side, reverse the y velocity
    #         if self.position[1] + self.velocity[1] > y0:
    #             self.velocity[1] *= -1
    #     else: # The boid is moving up
    #         # If we would pass the bottom side, reverse the y velocity
    #         if self.position[1] + self.velocity[1] < y1:
    #             self.velocity[1] *= -1
    
    def bounce_if_collision_with_obstacles(self, obstacle):
        """Check if the boid collides with the obstacle
        and if it does, bounce it"""
        x_vel = self.velocity[0]
        y_vel = self.velocity[1]
        # If the boid is moving to the right
        if self.velocity[0] > 0:
            x_vel = self.velocity[0] + self.radius
        else:
            x_vel = self.velocity[0] - self.radius
        # If the boid is moving down
        if self.velocity[1] > 0:
            y_vel = self.velocity[1] + self.radius
        else:
            y_vel = self.velocity[1] - self.radius

        jump_coords = list(self.position)
        jump_coords[0] = jump_coords[0][0] + x_vel
        jump_coords[1] = jump_coords[1][0] + y_vel
        if jump_coords in obstacle:
            self.reverse_velocity()

        
    def get_the_obstacles_collisions(self, obstacles_list):
        """Check if the boid collides with an obstacle
        And reverse the velocity if it does"""
        for obstacle in obstacles_list:
            # We build a list of obstacles that the boid can reach
            self.bounce_if_collision_with_obstacles(obstacle)

# Update the boid
    def update(self, obstacles_list):
        """Update the velocity and the position of the boid"""
        # The acceleration is the sum of the forces

        # Update the velocity
        self.velocity += self.acceleration
        
        # Chaotic behaviour
        if self.chaotic_probability < random.random():
            angle = random.uniform(0, 2 * math.pi)
            self.velocity[0] += math.cos(angle)
            self.velocity[1] += math.sin(angle)

        # Check if the boid is out of bounds and apply the correction
        if self.bouncing:
            # If we bounce the output is the velocity
            self.velocity = self.check_edges()
        else:
            # If we don't bounce the output is the position
            self.position = self.check_edges()
        
        # Check if the boid will collide with an obstacle
        self.get_the_obstacles_collisions(obstacles_list)

        # If velocity exceeds the max speed, set it to the max speed
        if np.linalg.norm(self.velocity) > self.max_speed:
            self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.max_speed
        # Update the position
        self.position += self.velocity

        # If the boid is out of space, bring it back to space
        self.bring_back_to_space()

        # Reset the acceleration
        self.acceleration = np.array([[0], [0]], dtype=np.float64)

    def get_coords(self):
        """Returns the coordinates of the boid
        Returns:
            (x, y) the coordinates of the boid"""
        x_pos, y_pos = self.position
        return (*x_pos, *y_pos) # unpacking the tuple

    def set_coords(self, x, y):
        """Set the coordinates of the boid"""
        self.position = np.array([[x], [y]], dtype=np.float64)

    def get_velocity(self):
        """Returns the velocity of the boid"""
        x_vel, y_vel = self.velocity
        return (*x_vel, *y_vel)
    
    def set_velocity(self, x_vel, y_vel):
        """Set the velocity of the boid"""
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)

    def bbox(self):
        """Returns the bounding box of the boid"""
        x_pos, y_pos = self.position
        return (x_pos - self.radius, y_pos - self.radius, x_pos + self.radius, y_pos + self.radius)

# %%
class Obstacle:
    """Class for the obstacles"""
    def __init__(self, x0, y0, x1, y1) -> None:
        self.coordinates = np.array([[x0, y0], [x1, y1]], dtype=np.float64)

    def __contains__(self, point):
        """Check if the point is inside the obstacle
        Returns:
            True if the point is inside the obstacle
            False if the point is outside the obstacle
        Arguments:
            point {[x,y]} -- The point to check"""
        x, y = point
        x_coord, y_coord = self.get_coords()
        if x_coord[0] <= x <= x_coord[1] and y_coord[0] <= y <= y_coord[1]:
            return True
        return False
    
    def get_coords(self):
        """Returns the coordinates of the obstacle
        Returns:
            (X,Y) with X the x coordinates and Y the y coordinates"""
        top_left_corner, bottom_right_corner = self.coordinates
        X = (top_left_corner[0], bottom_right_corner[0])
        Y = (top_left_corner[1], bottom_right_corner[1])
        return (X, Y)
    
    def get_center(self):
        """Returns the center of the obstacle
        Returns:
            The vector with the center of the obstacle"""
        X, Y = self.get_coords()
        return np.array([[(X[0] + X[1]) / 2], [(Y[0] + Y[1]) / 2]], dtype=np.float64)

#%% 
class SimulationSpace:
    """Class for the simulation space"""
    counter = 0
    def __init__(self, width, height):
        """Initialize the simulation space"""
        self.width = width
        self.height = height
        self.boids = []
        self.obstacles = []

        self.iteration = 0
        self.paused = True
        self.finished = False
        self.number_of_steps = 10
        self.counter = SimulationSpace.counter
        SimulationSpace.counter += 1
        
    
    def populate(self, number_of_boids, wind_speed, wind_direction, goal_x, goal_y, bouncing=True):
        """Populate the simulation space with boids"""
        Boid.set_width(self.width)
        Boid.set_height(self.height)
        Boid.set_goal_position(goal_x, goal_y)
        for _ in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            x_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            y_vel = random.randint(-Boid.max_speed, Boid.max_speed)
            boid = Boid(x_pos, y_pos, x_vel, y_vel, bouncing=bouncing,
             wind_speed=wind_speed, wind_direction=wind_direction, the_chosen_one=False) # True if _ == 0 else False
            self.boids.append(boid)
    
    def create_obstacle(self, x0, y0, x1, y1):
        """Create an obstacle"""
        self.obstacles.append(Obstacle(x0, y0, x1, y1))

    
    def next_step(self):
        """Update the simulation space"""

        self.iteration += 1
        for boid in self.boids:
            boid.find_near_boids(self.boids)
            boid.apply_rules()
            boid.set_boids_rate(boid.calculate_near_boids_number()/len(self.boids))
            boid.update_color_boids_rate()
        
        for boid in self.boids:
            boid.update(self.obstacles)

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
