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

omega = {'t', 'f','c'}
m1 = MassFunction([({'t'}, 0.6), (omega, 0.4)])
m2 = MassFunction([({'t','c'}, 0.7), (omega, 0.3)])
m3 = MassFunction([({'c'}, 0.4), ({'t'}, 0.3), (omega, 0.3)])
m4 = MassFunction([({'f'}, 0.7), (omega, 0.3)])

mv = MassFunction([(omega, 1)])
masses = [m1, m2, m3, m4]
mJ = masses[0].combine_conjunctive(masses[1:], False)
da = 0.05
md = [m.copy().discount(1-da) for m in masses]
mJds = [m.combine_conjunctive(masses[:i] + masses[i+1:], False) for i, m in enumerate(md)]

mJnorm = mJ.copy().normalize()
mJdnorms = [m.copy().normalize() for m in mJds]
dconflda = [ (mJ[frozenset()] - mJd[frozenset()]) /da for mJd in mJds]
dselfconda = [ (mJnorm.combine_conjunctive(mJnorm, False)[frozenset()]- mJdn.combine_conjunctive(mJdn, False)[frozenset()])/da for mJdn in mJdnorms]
dkpidan = [ (mJdn.contour_consistency() - mJnorm.contour_consistency())/da for mJdn in mJdnorms]
dkpida = [ (mJd.contour_consistency() - mJ.contour_consistency())/da for mJd in mJds]

#Nadia's Shapley
shap_autoconflict = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], True, lambda x : x.combine_conjunctive(x, False)[frozenset()])
shap_emptyset = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], False, lambda x : x[frozenset()])
shap_contour = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], False, lambda x: x.contour_conflict() )
shap_contournorm = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], True, lambda x: x.contour_conflict() )

ShapleysAutoConflict = [shap_autoconflict(m, masses) for m in masses]
ShapleysEmptySet  = [shap_emptyset(m, masses) for m in masses]
ShapleysContour = [shap_contour(m, masses) for m in masses]
ShapleysContourNorm = [shap_contournorm(m, masses) for m in masses]
