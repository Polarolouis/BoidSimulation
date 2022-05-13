from datetime import timedelta
import math
import pickle
import time
from pathlib import Path
import statistics as stats
import colored

from matplotlib import pyplot as plt

import boid as bd


def rgb_to_hex(r, g, b):
    """Convert RGB to hex"""
    return f"#{r:02x}{g:02x}{b:02x}"


ETA_ITERATION_SEPARATOR = 5
WHITE = colored.fg(rgb_to_hex(255, 255, 255))


def measure_execution_time(function, N, *, repeats=1, verbose=False):
    """Measure the execution time of a function"""
    output = [(0, 0)]
    time_between_steps = 0
    start = 0
    end = 0
    estimated_remaining_time = 0
    for i in range(1, N+1):
        ratio = (i/N)
        progressbar = "[" + "#"*int(ratio*79) + " "*(79-int(ratio*79)) + "]"
        red_part = 255 - int(ratio*255)
        green_part = int(ratio*255)
        blue_part = 0
        color = colored.fg(rgb_to_hex(red_part, green_part, blue_part))
        percentage = round(ratio*100, 2)
        if percentage < 10:
            percentage = " " + str(percentage)
        time_between_steps += round(end - start, 2) * \
            (1/ETA_ITERATION_SEPARATOR)
        if i % ETA_ITERATION_SEPARATOR == 0:
            estimated_remaining_time = round(
                (N - i) * time_between_steps, 2)

            # Reset the time_between_steps
            time_between_steps = 0

            estimated_remaining_time = timedelta(
                seconds=estimated_remaining_time)
        progressbar = f"{color + progressbar:=<29}{WHITE} {percentage}% | ETA {str(estimated_remaining_time)[:-4]}"
        print(f"\r{progressbar:^100}", end="")
        times = []
        for _ in range(repeats):
            start = time.time()
            function(i)
            end = time.time()
            times.append(end - start)
        mean_execution_time = stats.mean(times)
        if repeats > 1:
            variance_execution_time = stats.variance(times)
        else:
            variance_execution_time = 0
        output.append((mean_execution_time, variance_execution_time))
        eta_end = time.time()
    return output


def simulate(n):
    """Simulate the boids"""
    size = 500
    space = bd.SimulationSpace(size, size)
    space.populate(n, space_fill="even")
    for _ in range(50):
        space.next_step()

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------


N = 100
repeats = 5

type_of_algorithm = "Naive"

name = f"{type_of_algorithm}_N{N}_repeats{repeats}.dat"

# Checking if the file exists
path = Path(name)
if path.exists():
    print(f"File {name} already exists. Skipping simulation.")
    with open(name, "rb") as file:
        output = pickle.load(file)
else:
    print(f"Simulating {type_of_algorithm} with N={N} and repeats={repeats}")
    output = measure_execution_time(simulate, N, repeats=repeats, verbose=True)
    with open(name, "wb") as file:
        pickle.dump(output, file)


mean_times = [mean for mean, _ in output]
variance_times = [variance for _, variance in output]
absc = range(len(mean_times))
# Calculating the upper and lower bounds
positive_standard_deviance = [
    math.sqrt(variance) for variance in variance_times]
negative_standard_deviance = [- standard_deviance
                              for standard_deviance in positive_standard_deviance]

plt.plot(absc, mean_times, label=type_of_algorithm)
plt.legend([f"{type_of_algorithm}"])
plt.xlabel("Number of boids")
plt.ylabel("Execution time")
plt.title(
    f"Execution time of {type_of_algorithm} with N={N} and repeats={repeats}")
plt.show()
