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
normalization = True
results_file = open('results.csv', mode='w')
results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
results_writer.writerow(['Preference_satisfied','Distance','Conflict'])
#while(counterp < target or counterf<target):
while(counter < mc):
    masses = [generate_random_mass(k,p) for i in range(2)]
    m1 = masses[0]
    m2 = masses[1]
    mJ = m1.combine_conjunctive(m2, normalization)
   # mJ = m1.combine_conjunctive_disjunctive(m2)
    da = 0.05
    m1d = m1.copy().discount(1-da)
    m2d = m2.copy().discount(1-da)
    mJ1d = m2.combine_conjunctive(m1d, normalization)
    mJ2d = m1.combine_conjunctive(m2d, normalization)
    #mJ1d = m2.combine_conjunctive_disjunctive(m1d)
    #mJ2d = m1.combine_conjunctive_disjunctive(m2d)
    #check that decision (mJ) = decision (m1) =/= decision (m2)
    if (m2.max_bel() != m1.max_bel()) and (mJ.max_bel() == m1.max_bel()):
        counter= counter+1
        decision = mJ.max_bel()
        dbel1 = (mJ.bel(decision) - mJ1d.bel(decision) ) / da
        dbel2 = (mJ.bel(decision) - mJ2d.bel(decision) ) / da
        dpl1 = (mJ.pl(decision) - mJ1d.pl(decision) ) / da
        dpl2 = (mJ.pl(decision) - mJ2d.pl(decision) ) / da
        d1 = np.array([dbel1, dpl1])
        d2 = np.array([dbel2, dpl2])
        pos = np.array([1,1])
        impact1 = np.dot(d1, pos) / np.linalg.norm(pos)
        impact2 = np.dot(d2, pos) / np.linalg.norm(pos)
        dis = m1.distance(m2)
        confl = m1.combine_conjunctive(m2, False)[frozenset()]
        if dbel1 < dbel2:
            failbel = failbel+1
        if dpl1 < dpl2:
            failpl = failpl+1
        if impact1 < impact2:
            fail = fail+1
            counterf = counterf+1
            sat = False
            if counterf<target:
                results_writer.writerow([sat, dis, confl])
        else:
            sat = True
            counterp = counterp +1
            if counterp<target:
                results_writer.writerow([sat, dis, confl])

results_file.close()
print(failbel/mc)
print(failpl/mc)
print(fail/mc)