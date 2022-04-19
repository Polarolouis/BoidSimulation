import math
import random

class Boid:
    """Boid class"""
    near_distance = 50 # Distance to be considered near
    chaotic_probability = 1e-3
    weight_of_cohesion = 1
    def __init__(self, x_pos, y_pos, speed, angle, width, height, bouncing):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = speed
        self.angle = angle
        self.width = width
        self.height = height
        self.x_vel = self.speed * math.cos(self.angle)
        self.y_vel = self.speed * math.sin(self.angle)
        self.radius = 5
        self.bouncing = bouncing

        self.near_boids = []
    
    def update_velocity(self):
        """Update the velocity of the boid"""
        # Cohesion behaviour
        self.cohesion()

        # Collision avoidance behaviour
        self.avoid_collision()
        
        # Chaotic angle
        if random.random()< self.chaotic_probability:
            self.angle = 0.5 * random.random() * 360 + 0.5 * self.angle

        # Update the velocity

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
        if self.near_boids:
            x_vel_avg /= len(self.near_boids)
            y_vel_avg /= len(self.near_boids)
        
        
        # Calculate the average angle of the boids
        angle_avg = 0
        for boid in self.near_boids:
            angle_avg += boid.angle
        if self.near_boids:
            angle_avg /= len(self.near_boids)

        
        # Calculate the new velocity
        self.x_vel += 0.5 *(x_vel_avg - self.x_vel)
        self.y_vel += 0.5 *(y_vel_avg - self.y_vel)

        # Calculate the new angle
        self.angle += self.weight_of_cohesion * (angle_avg - self.angle)

    
    def avoid_collision(self):
        """Avoid collision behaviour"""
        pass
    

    def update_position(self):
        """Update the position of the boid"""
        # statement to check if the boid is out of bounds
        # and bounce it back if it is
        if self.bouncing:
            if self.x_pos + self.x_vel > self.width:
                self.x_vel = - self.x_vel
            elif self.x_pos + self.x_vel < 0:
                self.x_vel = - self.x_vel
            
            if self.y_pos + self.y_vel > self.height:
                self.y_vel = - self.y_vel
            elif self.y_pos + self.y_vel < 0:
                self.y_vel = - self.y_vel
        else:
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

    def bbox(self):
        """Returns the bounding box of the boid"""
        return (self.x_pos - self.radius, self.y_pos - self.radius, self.x_pos + self.radius, self.y_pos + self.radius)
    
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
    
    def populate(self, number_of_boids, bouncing=True):
        """Populate the simulation space with boids"""
        for _ in range(number_of_boids):
            x_pos = random.randint(0, self.width)
            y_pos = random.randint(0, self.height)
            speed = 5 # random.randint(1, 10)
            angle = random.randint(0, 360)
            boid = Boid(x_pos, y_pos, speed, angle, self.width, self.height, bouncing=bouncing)
            self.boids.append(boid)
    
    def next_step(self):
        """Update the simulation space"""
        for boid in self.boids:
            boid.find_near_boids(self.boids, boid.near_distance)
            boid.update_velocity()
            boid.update_position()