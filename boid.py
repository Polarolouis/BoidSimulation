import logging
import math
import random
import numpy as np

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S', filename='boid.log', filemode='w')
logging.info('Started to log')


class Boid:
    """Boid class"""

    id = 0
    radius = 5
    near_distance_alignment = 10*radius  # Distance to be considered near
    near_distance_cohesion = 0.5*near_distance_alignment
    near_distance_separation = 4*radius
    near_distance_collision = 2.5*radius
    chaotic_probability = 0.0
    bouncing = False

    goal_position = np.array([[0], [0]], dtype=np.float64)

    number_of_around_to_be_dense = 2

    alignment_force = 1
    cohesion_force = 1
    separation_force = 1
    goal_multiplicator_force = 1
    wind_speed = 0
    wind_direction = 0

    max_speed = 3
    max_alignment_force = 1
    max_cohesion_force = 1
    max_separation_force = 1
    max_goal_force = 1

    def __init__(self, x_pos, y_pos, x_vel, y_vel, the_chosen_one=False):
        """Initialize the boid
        Arguments:
            x_pos {float} -- x position of the boid
            y_pos {float} -- y position of the boid
            x_vel {float} -- x velocity of the boid
            y_vel {float} -- y velocity of the boid
            the_chosen_one {bool} -- True if the boid is the chosen one"""

        # Identification of the boid
        self.id = Boid.id
        Boid.id += 1

        # Initialise the boid position and velocity
        self.position = np.array([[x_pos], [y_pos]], dtype=np.float64)
        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)
        self.acceleration = np.array([[0], [0]], dtype=np.float64)
        self.new_acceleration = np.array([[0], [0]], dtype=np.float64)

        # Initialise the boid neighbours lists
        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []
        self.near_boids_collision = []

        # Initialise the boid color related variables
        self.the_chosen_one = the_chosen_one
        self.color = "green" if self.the_chosen_one else "white"
        self.boids_rate = 0
        self.density = len(self.near_boids_cohesion) / \
            self.number_of_around_to_be_dense

    @classmethod
    def set_width(cls, width):
        """Class Method : Set the width of the space
        Arguments:
            width {int} -- width of the space"""

        logging.debug('Setting the width of the space to %s', width)
        cls.width = width

    @classmethod
    def set_height(cls, height):
        """Class Method : Set the height of the space
        Arguments:
            height {int} -- height of the space"""

        logging.debug('Setting the height of the space to %s', height)
        cls.height = height

    @classmethod
    def set_force_parameters(cls, alignment_force, cohesion_force, separation_force, goal_force, wind_speed, wind_direction, bouncing):
        """Class Method : Set the force parameters
        Arguments:
            alignment_force {float} -- alignment force
            cohesion_force {float} -- cohesion force
            separation_force {float} -- separation force
            goal_force {float} -- goal force
            wind_speed {float} -- wind speed
            wind_direction {float} -- wind direction
            bouncing {bool} -- True if the boids bounce off the walls"""

        cls.alignment_force = alignment_force
        cls.cohesion_force = cohesion_force
        cls.separation_force = separation_force
        cls.goal_force = goal_force
        cls.wind_speed = wind_speed
        cls.wind_direction = wind_direction * 2 * math.pi / 360
        cls.bouncing = bouncing
        logging.debug('Setting the force parameters to %s', [
                      alignment_force, cohesion_force, separation_force, goal_force, wind_speed, wind_direction, bouncing])

    @classmethod
    def set_goal_position(cls, goal_x, goal_y):
        """Class Method : Set the goal position
        Arguments:
            goal_x {float} -- x position of the goal
            goal_y {float} -- y position of the goal"""

        cls.goal_position = np.array([[goal_x], [goal_y]], dtype=np.float64)
        logging.debug('Setting the goal position to %s', cls.goal_position)

# Flock calculation
    def find_near_boids(self, boids):
        """Sets a list of boids that are within a certain distance
        Arguments:
            boids {list} -- list of boids"""

        self.near_boids_alignment = []
        self.near_boids_cohesion = []
        self.near_boids_separation = []
        self.near_boids_collision = []

        filtered_boids = (boid for boid in boids if (self.id != boid.id) and ((self.position[0][0] - self.near_distance_alignment < boid.position[0][0] and self.position[1][0] - self.near_distance_alignment < boid.position[1][0]) and (
            self.position[0][0] + self.near_distance_alignment > boid.position[0][0] and self.position[1][0] + self.near_distance_alignment > boid.position[1][0])))
        logging.debug('Filtered boids: %s', filtered_boids)

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

            if (boid not in self.near_boids_collision) and dist < self.near_distance_collision:
                self.near_boids_collision.append((boid, dist))
                boid.near_boids_collision.append((self, dist))

        logging.debug('Near boids ids for alignment: %s', [
                      boid.id for boid, _ in self.near_boids_alignment])
        logging.debug('Near boids ids for cohesion: %s', [
                      boid.id for boid, _ in self.near_boids_cohesion])
        logging.debug('Near boids ids for separation: %s', [
                      boid.id for boid, _ in self.near_boids_separation])
        logging.debug('Near boids ids for collision: %s', [
                      boid.id for boid, _ in self.near_boids_collision])


# Flock behaviour


    def alignment(self):
        """Alignment behaviour to steer towards the average heading of the boids in the near_boids list
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        # Calculate the average heading of the boids
        heading_correction = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_alignment:
            # Taking the the fastest boid as a leader
            heading_correction = max(self.near_boids_alignment, key=lambda boid_and_distance: np.linalg.norm(
                boid_and_distance[0].velocity))[0].velocity

        if np.linalg.norm(heading_correction) > self.max_alignment_force:
            heading_correction = heading_correction / \
                np.linalg.norm(heading_correction) * self.max_alignment_force

        logging.debug('Alignment heading correction: %s', heading_correction)
        logging.debug('The alignment force is: %s', Boid.alignment_force)
        logging.debug('The correction for alignment is: %s',
                      heading_correction * Boid.alignment_force)

        return heading_correction * Boid.alignment_force

    def cohesion(self):
        """Cohesion behaviour to steer towards the average position of the boids in the near_boids list
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        # Calculate the average position of the boids
        correction_to_avg = np.array([[0], [0]], dtype=np.float64)
        if self.near_boids_cohesion:
            position_avg = np.array([[0], [0]], dtype=np.float64)
            for boid, _ in self.near_boids_cohesion:
                position_avg += boid.position
            position_avg /= len(self.near_boids_cohesion)
            correction_to_avg = position_avg - self.position
        if np.linalg.norm(correction_to_avg) > self.max_cohesion_force:
            correction_to_avg = correction_to_avg / \
                np.linalg.norm(correction_to_avg) * self.max_cohesion_force

        logging.debug('Cohesion correction to avg: %s', correction_to_avg)
        logging.debug('The cohesion force is: %s', Boid.cohesion_force)
        logging.debug('The correction for cohesion is: %s',
                      correction_to_avg * Boid.cohesion_force)

        return correction_to_avg * Boid.cohesion_force

    def separation(self):
        """Separation behaviour to avoid collisions with other boids
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        separation_correction = np.array([[0], [0]], dtype=np.float64)
        for boid, distance in self.near_boids_separation:
            diff = self.position - boid.position
            diff /= distance
            separation_correction += diff
        if self.near_boids_separation:
            separation_correction /= len(self.near_boids_separation)
        if np.linalg.norm(separation_correction):
            separation_correction = (
                separation_correction / np.linalg.norm(separation_correction)) * self.max_separation_force

        logging.debug('Separation correction: %s', separation_correction)
        logging.debug('The separation force is: %s', Boid.separation_force)
        logging.debug('The correction for separation is: %s',
                      separation_correction * Boid.separation_force)

        return separation_correction * Boid.separation_force

    def collision(self):
        """collision behavior to prevent boids from going through each other
        Returns:
            np.array([float,float]) -- [x velocity, y velocity]"""
        if len(self.near_boids_collision) == 1:
            x_vel = self.velocity[0][0]
            y_vel = self.velocity[1][0]
            vel = np.array([x_vel, y_vel], dtype=np.float64)

            for boid, distance in self.near_boids_collision:
                diff = self.position - boid.position
                diff_norm = np.linalg.norm(diff)
                x_diff = diff[0][0]
                y_diff = diff[1][0]
                if distance <= 1.9*boid.radius:
                    self.velocity = np.array(
                        [[-x_diff/diff_norm], [-y_diff/diff_norm]], dtype=np.float64)
                else:
                    normal = np.array([[-y_diff, x_diff]], dtype=np.float64)
                    normal_norm = np.linalg.norm(normal)
                    new_vel = (np.dot(normal, vel)/(normal_norm**2))*normal
                    x_new_vel = new_vel[0][0]
                    y_new_vel = new_vel[0][1]
                    self.velocity = np.array(
                        [[x_new_vel], [y_new_vel]], dtype=np.float64)
        elif len(self.near_boids_collision) == 2:
            """We want the boid to go away from it's two neighbors"""
            boid1 = self.near_boids_collision[0][0]
            boid2 = self.near_boids_collision[1][0]
            diff = boid1.position-boid2.position
            x_diff = diff[0][0]
            y_diff = diff[1][0]
            normal = np.array([[-y_diff], [x_diff]], dtype=np.float64)
            normal_norm = np.linalg.norm(normal)
            # determining if using the normal vector as velocity reduces or augments the distance between boids
            new_pos = self.position+(normal/normal_norm)
            new_diff = new_pos-boid1.position
            new_dist = np.linalg.norm(new_diff)
            if new_dist <= self.near_distance_collision:
                new_vel = -2 * normal / normal_norm
            else:
                new_vel = 2 * normal / normal_norm
            self.vel = new_vel
    # (np.dot(normal,self.velocity)/(normal_norm**2))*normal

    def wind(self):
        """Apply wind to the boid
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        x_wind_speed = self.wind_speed * math.cos(self.wind_direction)
        y_wind_speed = self.wind_speed * math.sin(self.wind_direction)

        logging.debug('x wind speed: %s', x_wind_speed)
        logging.debug('y wind speed: %s', y_wind_speed)

        return np.array([[x_wind_speed], [y_wind_speed]], dtype=np.float64)

    def goal(self):
        """Apply goal force to the boid
        Returns:
            np.array([float, float]) -- [x acceleration, y acceleration]"""

        goal_force = np.array([[0], [0]], dtype=np.float64)
        if self.goal_position is not None:
            goal_force = self.goal_position - self.position

            # Distance based coefficient
            goal_force = np.linalg.norm(goal_force) * goal_force

            if np.linalg.norm(goal_force) > self.max_goal_force:
                goal_force = goal_force / \
                    np.linalg.norm(goal_force) * self.max_goal_force

        logging.debug('Goal force: %s', goal_force)
        logging.debug('The goal force is: %s', Boid.goal_multiplicator_force)
        logging.debug('The correction for goal is: %s',
                      goal_force * Boid.goal_multiplicator_force)

        return goal_force * Boid.goal_multiplicator_force

    def apply_rules(self):
        """Apply the rules of the flock to the boid
        By adding the forces of the different behaviours to the acceleration"""

        logging.debug('Applying rules to boid %s', self.id)
        logging.debug('----------------------------------')

        if self.goal_force > 0:
            goal = self.goal()
            self.acceleration += goal * (1/2 - self.density)

        if self.wind_speed > 0:
            wind = self.wind()
            self.acceleration += wind

        if self.alignment_force > 0:
            alignment = self.alignment()
            self.acceleration += alignment

        if self.cohesion_force > 0:
            cohesion = self.cohesion()
            self.acceleration += cohesion * (1/2 - self.density)

        if self.separation_force > 0:
            separation = self.separation()
            self.acceleration += separation * (1 + self.density)

        # if len(self.near_boids_collision) >= 3:
        #     # norm_vel=np.linalg.norm(self.velocity)
        #     self.velocity = -self.velocity

        logging.debug('Boid %s acceleration: %s', self.id, self.acceleration)
        logging.debug('----------------------------------')

    def check_edges(self):
        """Check if the boid is out of bounds
        Returns: 
            If the boids are bouncing: velocity np.array([float, float])
            If the boids are not bouncing: position np.array([float, float])"""

        # If bouncing is on, bounce the boid back into the screen
        if self.bouncing:

            logging.debug('Boid %s is bouncing', self.id)

            velocity = self.velocity
            if self.position[0] + self.velocity[0] < self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[0] + self.velocity[0] > self.width - self.radius:
                velocity[0] = -self.velocity[0]
            if self.position[1] + self.velocity[1] < self.radius:
                velocity[1] = -self.velocity[1]
            if self.position[1] + self.velocity[1] > self.height - self.radius:
                velocity[1] = -self.velocity[1]

            logging.debug('Boid %s velocity: %s', self.id, velocity)

            return velocity
        else:
            # If bouncing is off, check if the boid is out of bounds
            # And if it is, set the boid to the opposite side

            logging.debug('Boid %s is not bouncing', self.id)

            position = self.position
            if self.position[0] < self.radius:
                position[0] = self.width - self.radius
            if self.position[0] > self.width - self.radius:
                position[0] = self.radius
            if self.position[1] < self.radius:
                position[1] = self.height - self.radius
            if self.position[1] > self.height - self.radius:
                position[1] = self.radius

            logging.debug('Boid %s position: %s', self.id, position)

            return position

    def is_out_of_space(self):
        """Check if the boid is out of space
        Returns:
            bool -- True if the boid is out of space, False otherwise"""

        if self.position[0] < 0 or self.position[0] > self.width or self.position[1] < 0 or self.position[1] > self.height:
            return True
        else:
            return False

    def bring_back_to_space(self):
        """Bring the boid back to space"""

        if self.is_out_of_space():
            self.position[0] = self.width / 2
            self.position[1] = self.height / 2
            logging.warning(
                "Boid %s is out of space, brought back to space", self.id)

# Functions to color the boid according to the surrounding density
    def calculate_near_boids_number(self):
        """Calculate the number of boids near the boid
        Returns:
            int -- number of boids near the boid in the cohesion and separation circles"""

        return len(self.near_boids_cohesion) + len(self.near_boids_separation)

    def update_color_boids_rate(self):
        """Update the color of the boid based on the density of the boids near it
        Sets the color of the boid according to the color of the density of the boids near it"""

        boids_rate = self.boids_rate

        def rgb_hack(rgb):
            return "#%02x%02x%02x" % rgb
        red = 255
        green = 255 - int(boids_rate * 255)
        blue = 255 - int(boids_rate * 255)
        self.color = rgb_hack((red, green, blue))

    def set_boids_rate(self, boids_rate):
        """Sets the density of the boids near the boid"""

        self.boids_rate = boids_rate

# Functions for the collision with obstacles

    def reverse_velocity(self):
        """Reverse the velocity of the boid"""
        self.velocity *= -1

    def bounce_if_collision_with_obstacles(self, obstacle):
        """Check if the boid collides with the obstacle
        and if it does, bounce it
        Arguments:
            obstacle {Obstacle} -- The obstacle to check against"""

        (obs_x0, obs_x1), (obs_y0, obs_y1) = obstacle.get_coords()

        x, y = self.get_coords()

        if (x, y) in obstacle:
            # If the boids are trapped in the obstacle, we teleport them out
            self.position = np.array([[obs_x0 - self.radius], [obs_y0/2]])

        x_vel = self.velocity[0]
        y_vel = self.velocity[1]
        # If the boid is moving to the right
        if self.velocity[0] > 0:
            logging.debug('Boid %s is moving to the right', self.id)
            x_vel = self.velocity[0] + self.radius
        else:
            logging.debug('Boid %s is moving to the left', self.id)
            x_vel = self.velocity[0] - self.radius
        # If the boid is moving down
        if self.velocity[1] > 0:
            logging.debug('Boid %s is moving down', self.id)
            y_vel = self.velocity[1] + self.radius
        else:
            logging.debug('Boid %s is moving up', self.id)
            y_vel = self.velocity[1] - self.radius
        if (x + x_vel >= obs_x0 and x + x_vel <= obs_x1) and (y + y_vel >= obs_y0 and y + y_vel <= obs_y1):
            if y <= obs_y0 or y >= obs_y1:
                self.velocity[1] = -self.velocity[1]
            if x <= obs_x0 or x >= obs_x1:
                self.velocity[0] = -self.velocity[0]
        new_x, new_y = x + self.velocity[0], y + self.velocity[1]
        if (new_x, new_y) in obstacle:
            # If the boid will be in the obstacle even with the correction
            # we stop
            self.velocity = -self.velocity

    def get_the_obstacles_collisions(self, obstacles_list):
        """Check if the boid collides with an obstacle
        And reverse the velocity if it does
        Arguments:
            obstacles_list {list} -- List of obstacles to check against"""

        for obstacle in obstacles_list:
            # We build a list of obstacles that the boid can reach
            logging.debug(
                'Boid %s is checking if it can reach the obstacle', self.id)
            self.bounce_if_collision_with_obstacles(obstacle)

# Update the boid
    def update(self, obstacles_list):
        """Update the velocity and the position of the boid
        Arguments:
            obstacles_list {list} -- List of obstacles to check against"""

        logging.debug('Boid %s is updating', self.id)
        logging.debug('Boid %s position: %s', self.id, self.position)

        # Update the velocity
        logging.debug('Boid %s is updating the velocity from %s',
                      self.id, self.velocity)
        self.velocity += self.acceleration
        logging.debug('to %s', self.velocity)

        # Chaotic behaviour
        if self.chaotic_probability < random.random():
            logging.debug('Boid %s ', self.id)
            angle = random.uniform(0, 2 * math.pi)
            self.velocity[0] += math.cos(angle)
            self.velocity[1] += math.sin(angle)

        # Collision
        if self.near_boids_collision:
            self.collision()

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
            logging.debug(
                'Boid %s velocity exceeds the max speed, setting it to the max speed', self.id)
            self.velocity = self.velocity / \
                np.linalg.norm(self.velocity) * self.max_speed
            logging.debug('Boid %s velocity: %s', self.id, self.velocity)
        # Update the position
        self.position += self.velocity
        logging.debug('Boid %s new position: %s', self.id, self.position)

        # If the boid is out of space, bring it back to space
        self.bring_back_to_space()

        # Reset the acceleration
        self.acceleration = np.array([[0], [0]], dtype=np.float64)

    def get_coords(self):
        """Returns the coordinates of the boid
        Returns:
            (x, y) the coordinates of the boid"""
        x_pos, y_pos = self.position[0][0], self.position[1][0]

        return (x_pos, y_pos)  # unpacking the tuple

    def set_coords(self, x, y):
        """Set the coordinates of the boid
        Arguments:
            x: the x coordinate
            y: the y coordinate"""

        self.position = np.array([[x], [y]], dtype=np.float64)

    def get_velocity(self):
        """Returns the velocity of the boid
        Returns:
            (x_vel, y_vel) the velocity of the boid"""

        x_vel, y_vel = self.velocity
        return (*x_vel, *y_vel)

    def set_velocity(self, x_vel, y_vel):
        """Set the velocity of the boid
        Arguments:
            x_vel: the x velocity
            y_vel: the y velocity"""

        self.velocity = np.array([[x_vel], [y_vel]], dtype=np.float64)

    def bbox(self):
        """Returns the bounding box of the boid
        Returns:
            (x0, y0, x1, y1) the bounding box of the boid"""

        x_pos, y_pos = self.position
        return (x_pos - self.radius, y_pos - self.radius, x_pos + self.radius, y_pos + self.radius)


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
            logging.debug('Point (%s, %s) is inside the obstacle', x, y)
            return True
        logging.debug('Point (%s, %s) is outside the obstacle', x, y)
        return False

    def x_between_bounds(self, x):
        """Check if the x coordinate is between the x bounds of the obstacle
        Returns:
            True if the x coordinate is between the x bounds of the obstacle
            False if the x coordinate is not between the x bounds of the obstacle
        Arguments:
            x {float} -- The x coordinate to check"""

        x_coord, _ = self.get_coords()
        if x_coord[0] <= x <= x_coord[1]:
            return True
        return False

    def y_between_bounds(self, y):
        """Check if the y coordinate is between the y bounds of the obstacle
        Returns:
            True if the y coordinate is between the y bounds of the obstacle
            False if the y coordinate is not between the y bounds of the obstacle
        Arguments:
            y {float} -- The y coordinate to check"""

        _, y_coord = self.get_coords()
        if y_coord[0] <= y <= y_coord[1]:
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
            np.array([[x], [y]]) with x the x center and y the y center"""

        X, Y = self.get_coords()
        return np.array([[(X[0] + X[1]) / 2], [(Y[0] + Y[1]) / 2]], dtype=np.float64)


class SimulationSpace:
    """Class for the simulation space"""
    counter = 0

    def __init__(self, width, height):
        """Initialize the simulation space
        Arguments:
            width {int} -- The width of the space
            height {int} -- The height of the space"""

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

    def populate(self, number_of_boids, space_fill="random"):
        """Populate the simulation space with boids
        Arguments:
            number_of_boids {int} -- The number of boids to populate
            goal_x {float} -- The x coordinate of the goal
            goal_y {float} -- The y coordinate of the goal"""

        Boid.set_width(self.width)
        Boid.set_height(self.height)
        if space_fill == "random":
            logging.info(
                'Populating the simulation space with %s boids in random pattern', number_of_boids)
            for _ in range(number_of_boids):
                x_pos = random.randint(0, self.width)
                y_pos = random.randint(0, self.height)
                x_vel = random.randint(-Boid.max_speed, Boid.max_speed)
                y_vel = random.randint(-Boid.max_speed, Boid.max_speed)
                logging.debug(
                    'Creating boid at (%s, %s) with velocity (%s, %s)', x_pos, y_pos, x_vel, y_vel)
                # True if _ == 0 else False
                boid = Boid(x_pos, y_pos, x_vel, y_vel, the_chosen_one=False)
                self.boids.append(boid)
        elif space_fill == "even":
            logging.info(
                'Populating the simulation space with %s boids in even pattern', number_of_boids)
            X = np.arange(0+Boid.radius, self.width-Boid.radius,
                          math.sqrt((self.width*self.height)/number_of_boids))
            Y = np.arange(0+Boid.radius, self.height-Boid.radius,
                          math.sqrt((self.width*self.height)/number_of_boids))
            positions = []

            for x_pos in X:
                for y_pos in Y:
                    positions.append((x_pos, y_pos))
            for x_pos, y_pos in positions:
                if len(self.boids) < number_of_boids:
                    x_vel = random.randint(-Boid.max_speed, Boid.max_speed)
                    y_vel = random.randint(-Boid.max_speed, Boid.max_speed)
                    logging.debug(
                        'Creating boid at (%s, %s) with velocity (%s, %s)', x_pos, y_pos, x_vel, y_vel)
                    # True if _ == 0 else False
                    boid = Boid(x_pos, y_pos, x_vel, y_vel,
                                the_chosen_one=False)
                    self.boids.append(boid)
                else:
                    break

    def create_obstacle(self, x0, y0, x1, y1):
        """Create an obstacle
        Arguments:
            x0 {float} -- The x coordinate of the top left corner of the obstacle
            y0 {float} -- The y coordinate of the top left corner of the obstacle
            x1 {float} -- The x coordinate of the bottom right corner of the obstacle
            y1 {float} -- The y coordinate of the bottom right corner of the obstacle"""

        self.obstacles.append(Obstacle(x0, y0, x1, y1))
        logging.debug('Created obstacle at (%s, %s) to (%s, %s)',
                      x0, y0, x1, y1)

    def next_step(self):
        """Calculate the next iteration of the simulation"""

        self.iteration += 1
        logging.info('Iteration %s', self.iteration)
        logging.info('-----------------')
        for boid in self.boids:
            boid.find_near_boids(self.boids)
            boid.apply_rules()
            boid.set_boids_rate(
                boid.calculate_near_boids_number()/len(self.boids))
            boid.update_color_boids_rate()

        for boid in self.boids:
            boid.update(self.obstacles)
        logging.info('-----------------')

    def get_positions(self):
        """Returns the positions of the boids for the current iteration
        Returns:
            """

        return {boid.id: boid.get_coords() for boid in self.boids}

# Method to control the state of the simulation
    def start_simulation(self, number_of_steps=10):
        """Start the simulation
        Keyword Arguments:
            number_of_steps {int} -- The number of steps to run the simulation (default: {10})"""

        self.paused = False
        self.number_of_steps = number_of_steps
        self.finished = False
        logging.info('Simulation %s started', self.counter)

    def toggle_pause(self):
        """Toggle the pause state of the simulation"""

        self.paused = not self.paused
        if self.paused:
            logging.info('Simulation %s paused', self.counter)
        else:
            logging.info('Simulation %s resumed', self.counter)

    def finish_simulation(self):
        """Finish the simulation"""

        self.finished = True
        logging.info('Simulation %s finished', self.counter)

# Method to clear the simulation space

    def clear(self):
        """Reset the simulation"""

        self.boids = []
        self.iteration = 0
        self.paused = True
        self.finished = False
