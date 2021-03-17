from pyds import MassFunction
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
from string import ascii_lowercase
import random
from math import fsum
import numpy as np
import csv
def int2set(k):
    return [ascii_lowercase[i] for i in range(k.bit_length()) if k & (1<<i)]


def generate_random_mass(k,p):
    #check k< 2^p
    fsets = random.sample(list(range(1,2**p)), k)
    r = [random.random() for i in range(k)]
    normsum = fsum(r)
    probs = [p / normsum for p in r]
    m = MassFunction()
    for idx, f in enumerate(fsets):
        m[tuple(int2set(f))] = probs[idx]
    return m

# dbel1a = (mJ.bel('a') - mJ1d.bel('a') ) / da
# dbel2a = (mJ.bel('a') - mJ2d.bel('a') ) / da

def generate_vacuous_mass(k):
    m = MassFunction()
    m[tuple(int2set(2**k -1))] = 1
    return m
k = 5
p=3
mc=1800
counter = 0
counterp = 0
counterf = 0
target = 20000
fail = 0
failbel = 0
failpl = 0
normalization = False
U = []
D = []
mv = generate_vacuous_mass(k)
for i in range(mc):
    mass = generate_random_mass(k, p)
    U.append(mass.hartley_measure())
    D.append(1 - mass.distance(mv))
plt.scatter(D,U)
plt.show()

