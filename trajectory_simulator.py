import datetime
import json
import os
import time
import boid
import colored


# ---------------------------------------------------------------------------------------------------------------------
#                                                      CONSTANTS
# ---------------------------------------------------------------------------------------------------------------------

SEPARATION_LINE = "-" * (104)

RED = colored.fg("red")
GREEN = colored.fg("green")
WHITE = colored.fg("white")
YELLOW = colored.fg("yellow")

ETA_ITERATION_SEPARATOR = 25

LENGHT_PROGRESSBAR = 60

DEFAULT_WIDTH, DEFAULT_HEIGHT = (1200, 800)

DEFAULT_NUMBER_OF_BOIDS = 50
DEFAULT_NUMBER_OF_STEPS = 1_000

DEFAULT_BOUNCING = True

DEFAULT_WIND_SPEED = 0
DEFAULT_WIND_DIRECTION = 0

DEFAULT_GOAL_X = DEFAULT_WIDTH/2
DEFAULT_GOAL_Y = DEFAULT_HEIGHT/2

DEFAULT_ALIGNMENT_FORCE_MULTIPLICATOR = 1
DEFAULT_COHESION_FORCE_MULTIPLICATOR = 1
DEFAULT_SEPARATION_FORCE_MULTIPLICATOR = 1
DEFAULT_GOAL_FORCE_MULTIPLICATOR = 0

# Assign default values to the constants
parameters = {"WIDTH":DEFAULT_WIDTH, "HEIGHT":DEFAULT_HEIGHT, "NUMBER_OF_BOIDS":DEFAULT_NUMBER_OF_BOIDS, 
                        "NUMBER_OF_STEPS":DEFAULT_NUMBER_OF_STEPS, "BOUNCING":DEFAULT_BOUNCING, 
                        "WIND_SPEED":DEFAULT_WIND_SPEED, "WIND_DIRECTION":DEFAULT_WIND_DIRECTION, "GOAL_X":DEFAULT_GOAL_X,
                        "GOAL_Y":DEFAULT_GOAL_Y, "ALIGNMENT_FORCE_MULTIPLICATOR":DEFAULT_ALIGNMENT_FORCE_MULTIPLICATOR, 
                        "COHESION_FORCE_MULTIPLICATOR":DEFAULT_COHESION_FORCE_MULTIPLICATOR, 
                        "SEPARATION_FORCE_MULTIPLICATOR":DEFAULT_SEPARATION_FORCE_MULTIPLICATOR, 
                        "GOAL_FORCE_MULTIPLICATOR":DEFAULT_GOAL_FORCE_MULTIPLICATOR}



# Defines the maximum inputs for the simulation
max_parameters = {"MAX_WIDTH":2000, "MAX_HEIGHT":2000, "MAX_NUMBER_OF_BOIDS":(DEFAULT_WIDTH / 2 * boid.Boid.radius) * (DEFAULT_HEIGHT / 2 * boid.Boid.radius),
                    "MAX_NUMBER_OF_STEPS":1_000_000, "MAX_BOUNCING":True, "MAX_WIND_SPEED":100, "MAX_WIND_DIRECTION":360,
                    "MAX_GOAL_X":DEFAULT_WIDTH, "MAX_GOAL_Y":DEFAULT_HEIGHT, "MAX_ALIGNMENT_FORCE_MULTIPLICATOR":2,
                    "MAX_COHESION_FORCE_MULTIPLICATOR":2, "MAX_SEPARATION_FORCE_MULTIPLICATOR":2, "MAX_GOAL_FORCE_MULTIPLICATOR":2}


# ---------------------------------------------------------------------------------------------------------------------
#                                                      INPUT MENU
# ---------------------------------------------------------------------------------------------------------------------

# Define the input menu
def input_and_verification(variable_name : str, minimum, maximum, type_of_input=int):
    """Display the input menu and verify the input
    Arguments:
        variable_name {str} -- The name of the variable
        minimum {int} -- The minimum value of the variable
        maximum {int} -- The maximum value of the variable
        type_of_input {int} -- The type of the input
    Returns:
        type_of_input -- The input"""
    input_is_valid = False
    while not input_is_valid:
        
        # Check if the type is either int or float
        special = ""
        if type_of_input == int:
            input_value = -5
        elif type_of_input == float:
            input_value = -5.5
        elif type_of_input == bool:
            input_value = False
            special = ", 1 for True/ 0 for False"
        else:
            raise TypeError("The type of the input is not valid !")

        # Try to convert the input to the type of the input
        try:
            input_value = type_of_input(input(f"\nEnter the value for {variable_name} (minimum: {minimum}, maximum: {maximum}{special}): "))
            if input_value < minimum or input_value > maximum:
                print(f"The value {input_value} is not in the range {minimum} to {maximum}\n")
            else:
                input_is_valid = True
        except ValueError:
            print("Invalid input. Please try again.")
        
    return input_value

# Function to display the current values of the constants
def display_current_values(parameters_name_list):
    """Display the current values of the constants
    Arguments:
        parameters_list {list} -- The list of the parameters
    """
    os.system("cls" if os.name == "nt" else "clear")
    print(f'{"+----------------------+":^104}')
    print(f'{"| Trajectory Simulator |":^104}')
    print(f'{"+----------------------+":^104}')
    print(SEPARATION_LINE)
    print(f"+{'Current values':^102}+")
    print(SEPARATION_LINE)
    for index, (parameter_name, value) in enumerate(parameters_name_list.items()):
        print(f"|{f'{index + 1}. {parameter_name} = {value}':^102}|")

def menu(parameters, max_parameters):
    """Display the menu and return the new value for constants
    Arguments:
        parameters_name_list {list} -- The list of the parameters
    """
    # Display the current values of the constants
    display_current_values(parameters)
    #default_color = colored.fg("default")
    print(SEPARATION_LINE)
    print(f'|{f"{GREEN}    0. Validate{WHITE}":<121}|')
    print(f'|{f"{RED}   -1. Exit{WHITE}":<121}|')
    print(SEPARATION_LINE)

    # Get the input
    input_value = input_and_verification("input", -1, 16, int)

    out_name = ""
    out_value = -1
    # Update the constants
    if input_value == 1:
        out_name = "WIDTH"
        out_value = input_and_verification("WIDTH", 0, max_parameters["MAX_WIDTH"], int)
    elif input_value == 2:
        out_name = "HEIGHT"
        out_value = input_and_verification("HEIGHT", 0, max_parameters["MAX_HEIGHT"], int)
    elif input_value == 3:
        out_name = "NUMBER_OF_BOIDS"
        out_value = input_and_verification("NUMBER_OF_BOIDS", 0, max_parameters["MAX_NUMBER_OF_BOIDS"], int)
    elif input_value == 4:
        out_name = "NUMBER_OF_STEPS"
        out_value = input_and_verification("NUMBER_OF_STEPS", 0, max_parameters["MAX_NUMBER_OF_STEPS"], int)
    elif input_value == 5:
        out_name = "BOUNCING"
        out_value = input_and_verification("BOUNCING", 0, 1, bool)
    elif input_value == 6:
        out_name = "WIND_SPEED"
        out_value = input_and_verification("WIND_SPEED", 0, max_parameters["MAX_WIND_SPEED"], float)
    elif input_value == 7:
        out_name = "WIND_DIRECTION"
        out_value = input_and_verification("WIND_DIRECTION", 0, max_parameters["MAX_WIND_DIRECTION"], int)
    elif input_value == 8:
        out_name = "GOAL_X"
        out_value = input_and_verification("GOAL_X", 0, max_parameters["MAX_GOAL_X"], int)
    elif input_value == 9:
        out_name = "GOAL_Y"
        out_value = input_and_verification("GOAL_Y", 0, max_parameters["MAX_GOAL_Y"], int)
    elif input_value == 10:
        out_name = "ALIGNMENT_FORCE_MULTIPLICATOR"
        out_value = input_and_verification("ALIGNMENT_FORCE_MULTIPLICATOR", 0, max_parameters["MAX_ALIGNMENT_FORCE_MULTIPLICATOR"], float)
    elif input_value == 11:
        out_name = "COHESION_FORCE_MULTIPLICATOR"
        out_value = input_and_verification("COHESION_FORCE_MULTIPLICATOR", 0, max_parameters["MAX_COHESION_FORCE_MULTIPLICATOR"], float)
    elif input_value == 12:
        out_name = "SEPARATION_FORCE_MULTIPLICATOR"
        out_value = input_and_verification("SEPARATION_FORCE_MULTIPLICATOR", 0, max_parameters["MAX_SEPARATION_FORCE_MULTIPLICATOR"], float)
    elif input_value == 13:
        out_name = "GOAL_FORCE_MULTIPLICATOR"
        out_value = input_and_verification("GOAL_FORCE_MULTIPLICATOR", 0, max_parameters["MAX_GOAL_FORCE_MULTIPLICATOR"], float)
    elif input_value == 0:
        out_name = "VALIDATE"
        out_value = True
    elif input_value == -1:
        out_name = "EXIT"
        out_value = False
    else:
        raise ValueError("The input is not valid !")
    return out_name, out_value

def update_max_values(parameters, max_parameters):
    """Update the max values"""
    max_parameters["MAX_NUMBER_OF_BOIDS"] = (parameters["WIDTH"]/2*boid.Boid.radius) * (parameters["HEIGHT"]/2*boid.Boid.radius)
    max_parameters["MAX_GOAL_X"] = parameters["WIDTH"]
    max_parameters["MAX_GOAL_Y"] = parameters["HEIGHT"]

def loop_menu(parameters, max_parameters):
    """Loop the menu until the user wants to exit or validate the constants"""

    in_menu = True
    quit = False
    while in_menu:
        out_name, out_value = menu(parameters, max_parameters)
        if out_name == "VALIDATE":
            in_menu = False
        elif out_name == "EXIT":
            in_menu = False
            quit = True
        else:
            parameters[out_name] = out_value
            update_max_values(parameters, max_parameters)
    if quit:
        return False
    else:
        return True

if loop_menu(parameters, max_parameters):
    filename = f"{parameters['NUMBER_OF_BOIDS']}_boids_in_{parameters['WIDTH']}x{parameters['HEIGHT']}_space_with_{parameters['NUMBER_OF_STEPS']}_steps_alignment_force_{parameters['ALIGNMENT_FORCE_MULTIPLICATOR']}_cohesion_force_{parameters['COHESION_FORCE_MULTIPLICATOR']}_separation_force_{parameters['SEPARATION_FORCE_MULTIPLICATOR']}_wind_speed_{parameters['WIND_SPEED']}_wind_direction_{parameters['WIND_DIRECTION']}_goal_force_{parameters['GOAL_FORCE_MULTIPLICATOR']}_goal_position_{parameters['GOAL_X']}x{parameters['GOAL_Y']}_bouncing_{parameters['BOUNCING']}"
    if os.path.isfile(filename):
        print(f"WARNING : {RED}The file {filename} already exists !{WHITE}")
        print(f"Do you want to overwrite it ? {YELLOW}(y/n) {WHITE}")
        answer = input()
        if answer == "y":
            print(f"{GREEN}The file {filename} will be overwritten !{WHITE}")
        elif answer == "n":
            print(f"{RED}The file {filename} will not be overwritten !{WHITE}")
            exit()
    print(SEPARATION_LINE)
    print(f'{"SIMULATION STARTED":^104}')
    print(SEPARATION_LINE)
    # Create the simulation
    width, height = parameters["WIDTH"], parameters["HEIGHT"]
    simulation = boid.SimulationSpace(width, height)
    boid.Boid.set_force_parameters(alignment_force=parameters["ALIGNMENT_FORCE_MULTIPLICATOR"], 
            cohesion_force=parameters["COHESION_FORCE_MULTIPLICATOR"], separation_force=parameters["SEPARATION_FORCE_MULTIPLICATOR"], 
            wind_speed=parameters["WIND_SPEED"], wind_direction=parameters["WIND_DIRECTION"], goal_force=parameters["GOAL_FORCE_MULTIPLICATOR"], 
            bouncing = parameters["BOUNCING"])
    boid.Boid.set_goal_position(parameters["GOAL_X"], parameters["GOAL_Y"])
    # Create the boids
    simulation.populate(parameters["NUMBER_OF_BOIDS"], parameters["GOAL_X"], parameters["GOAL_Y"], space_fill = "even")

    # Create the dictionnary of the boids
    boids = {0 : { boid.id : boid.get_coords() for boid in simulation.boids}}

    def rgb_to_hex(r, g, b):
        """Convert rgb to hex"""
        return '#%02x%02x%02x' % (r, g, b)

    # Iterate the simulation
    print(SEPARATION_LINE)
    print(f'{"COMPUTING SIMULATION":^104}')
    print(SEPARATION_LINE)
    start = 0
    end = 0
    time_between_steps = 0
    estimated_remaining_time = parameters["NUMBER_OF_STEPS"] * parameters["NUMBER_OF_BOIDS"]
    start_full = time.time()
    for i in range(1, parameters["NUMBER_OF_STEPS"]+1):
        ratio = (i/parameters["NUMBER_OF_STEPS"])
        progressbar = "[" + "#"*int(ratio*79) + " "*(79-int(ratio*79)) + "]"
        red_part = 255 - int(ratio*255)
        green_part = int(ratio*255)
        blue_part = 0
        color = colored.fg(rgb_to_hex(red_part, green_part, blue_part))
        percentage = round(ratio*100, 2)
        time_between_steps += round(end - start, 2) * (1/ETA_ITERATION_SEPARATOR)
        if i%ETA_ITERATION_SEPARATOR == 0:
            estimated_remaining_time = round((parameters["NUMBER_OF_STEPS"] - i) * time_between_steps, 2)
            
            # Reset the time_between_steps
            time_between_steps = 0
            
            estimated_remaining_time = datetime.timedelta(seconds=estimated_remaining_time)
        progressbar = f"{color + progressbar:=<29}{WHITE} {percentage:2.2f}% | ETA {estimated_remaining_time}"
        print(f"\r{progressbar:^100}", end="")
        #print(f"\r{percentage}%", end="")
        start = time.time()
        simulation.next_step()
        current_position = simulation.get_positions()
        boids[i] = dict()
        for boid_id in range(parameters["NUMBER_OF_BOIDS"]):
            boids[i][boid_id] = current_position[boid_id]
        end = time.time()
    end_full = time.time()
    time_to_completion = datetime.timedelta(seconds=round(end_full - start_full, 2))
    print(f"\nSimulation completed in {time_to_completion}")
    print("\n" + SEPARATION_LINE)
    print(f'{"SIMULATION FINISHED":^104}')
    print(SEPARATION_LINE)

    # Saving the data to a file
    print(SEPARATION_LINE)
    print(f'{"SAVING SIMULATION":^104}')
    print(SEPARATION_LINE)
    # Checking if the file exists
    with open(f"{filename}.json", "w", encoding="utf8") as file:
        json.dump(boids, file)
    print(SEPARATION_LINE)
    print(f'{f"SIMULATION SAVED TO : {filename:<50}.json":^104}')
    print(SEPARATION_LINE)