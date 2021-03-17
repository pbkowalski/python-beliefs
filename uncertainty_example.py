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
mY = masses[0].combine_yager(masses[1:])
# mDisj = masses[0].combine_disjunctive(masses[1:])
mDP = masses[0].combine_conjunctive_disjunctive(masses[1:])

shap_DP_hartl = lambda m1, masses : m1.shapley_yager([m for m in masses if m is not m1], lambda x: mv.hartley_measure() - x.hartley_measure())
shaps_DP_hart= [-shap_DP_hartl(m, masses) for m in masses]

shap_Yag_hartl = lambda m1, masses : m1.shapley_conj_disj([m for m in masses if m is not m1], lambda x: mv.hartley_measure() -x.hartley_measure())
shaps_Yag_hart= [-shap_Yag_hartl(m, masses) for m in masses]

shap_DP_dv= lambda m1, masses : m1.shapley_conj_disj([m for m in masses if m is not m1], lambda x: x.distance(mv))
shaps_DP_dv= [-shap_DP_dv(m, masses) for m in masses]


shap_Yag_dv= lambda m1, masses : m1.shapley_yager([m for m in masses if m is not m1], lambda x: x.distance(mv))
shaps_Yag_dv= [-shap_Yag_dv(m, masses) for m in masses]
# shap_disj_hartl = lambda m1, masses : m1.shapley_disj([m for m in masses if m is not m1], lambda x: mv.hartley_measure() - x.hartley_measure())
# shaps_disj_hart= [shap_disj_hartl(m, masses) for m in masses]

da = 0.05
md = [m.copy().discount(1-da) for m in masses]
mYagerD = [m.combine_yager(masses[:i] + masses[i+1:]) for i, m in enumerate(md)]
# mDisjD = [m.combine_disjunctive(masses[:i] + masses[i+1:]) for i, m in enumerate(md)]
mDPD= [m.combine_conjunctive_disjunctive(masses[:i] + masses[i+1:]) for i, m in enumerate(md)]

# dHdisj = [ (mDisj.hartley_measure() - mD.hartley_measure())/da for mD in mDisjD]
dYagH = [ (mY.hartley_measure() - mD.hartley_measure())/da for mD in mYagerD]
dDPH = [ (mDP.hartley_measure() - mD.hartley_measure())/da for mD in mDPD]

dYagdv = [ ( mD.distance(mv) - mY.distance(mv) )/da for mD in mYagerD]
dDPdv = [ (mD.distance(mv) - mDP.distance(mv) )/da for mD in mDPD]

#mJnorm = mJ.copy().normalize()
# mJdnorms = [m.copy().normalize() for m in mJds]
# dconflda = [ (mJ[frozenset()] - mJd[frozenset()]) /da for mJd in mJds]
# dselfconda = [ (mJnorm.combine_conjunctive(mJnorm, False)[frozenset()]- mJdn.combine_conjunctive(mJdn, False)[frozenset()])/da for mJdn in mJdnorms]
# dkpidan = [ (mJdn.contour_consistency() - mJnorm.contour_consistency())/da for mJdn in mJdnorms]
# dkpida = [ (mJd.contour_consistency() - mJ.contour_consistency())/da for mJd in mJds]
#
# #Nadia's Shapley
# shap_autoconflict = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], True, lambda x : x.combine_conjunctive(x, False)[frozenset()])
# shap_emptyset = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], False, lambda x : x[frozenset()])
# shap_contour = lambda m1, masses : m1.shapley([m for m in masses if m is not m1], False, lambda x: x.contour_conflict() )
#
# ShapleysAutoConflict = [shap_autoconflict(m, masses) for m in masses]
# ShapleysEmptySet  = [shap_emptyset(m, masses) for m in masses]
# ShapleysContour = [shap_contour(m, masses) for m in masses]
# ShapleysContourNorm = [shap_contournorm(m, masses) for m in masses]
