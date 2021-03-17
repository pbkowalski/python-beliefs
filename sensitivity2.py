from pyds import MassFunction
from itertools import product
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


k = 5
p=3
mc=800000
counter = 0
counterp = 0
counterf = 0
target = 20000
fail = 0
failbel = 0
failpl = 0
normalization = False

masses = [generate_random_mass(k,p) for i in range(5)]
mJ = masses[0].combine_conjunctive(masses[1:], normalization)
da = 0.05
md = [m.copy().discount(1-da) for m in masses]
mJds = [m.combine_conjunctive(masses[:i] + masses[i+1:], normalization) for i, m in enumerate(md)]

dconflda = [ (mJ[frozenset()] - mJd[frozenset()]) /da for mJd in mJds]


