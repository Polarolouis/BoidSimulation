import math
import pickle
import time
from pathlib import Path
import statistics as stats

from matplotlib import pyplot as plt

import boid as bd


def measure_execution_time(function, N, *, repeats=1, verbose=False):
    """Measure the execution time of a function"""
    output = [(0, 0)]
    for i in range(1, N+1):
        if verbose:
            print(f"{i/N*100:.2f}%", end="\r")
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
    return output


def simulate(n):
    """Simulate the boids"""
    size = 500
    space = bd.SimulationSpace(size, size)
    space.populate(n, bouncing=False)
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
