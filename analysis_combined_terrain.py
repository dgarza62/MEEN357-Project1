import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *

# ---- Rover / planet definitions (Appendix A & C) ----
wheel = {"radius": 0.30, "mass": 1.0}
speed_reducer = {"type": "reverted", "diam_pinion": 0.04, "diam_gear": 0.07, "mass": 1.5}
motor = {"torque_stall": 170, "torque_noload": 0, "speed_noload": 3.80, "mass": 5.0}
wheel_assembly = {"wheel": wheel, "speed_reducer": speed_reducer, "motor": motor}
rover = {"wheel_assembly": wheel_assembly,
         "chassis": {"mass": 659},
         "science_payload": {"mass": 75},
         "power_subsys": {"mass": 90}}
planet = {"g": 3.72}

from scipy.optimize import brentq

def max_speed(slope_deg, Crr):
    """Terminal rover speed [m/s]: motor speed where F_net = 0 (NaN if none)."""
    f = lambda w: F_net(w, slope_deg, rover, planet, Crr)
    a, b = 0.0, motor["speed_noload"]
    if f(a) * f(b) > 0:
        return float("nan")
    w = brentq(f, a, b)
    return wheel["radius"] * w / get_gear_ratio(speed_reducer)   # v = r*omega_out


Crr_array = np.linspace(0.01, 0.5, 25)
slope_array_deg = np.linspace(-15, 35, 25)
CRR, SLOPE = np.meshgrid(Crr_array, slope_array_deg)
VMAX = np.zeros(np.shape(CRR), dtype=float)

N = np.shape(CRR)[0]
for i in range(N):
    for j in range(N):
        VMAX[i, j] = max_speed(float(SLOPE[i, j]), float(CRR[i, j]))

plt.figure(figsize=(8, 6))
cs = plt.contourf(CRR, SLOPE, VMAX, 20)
cb = plt.colorbar(cs)
cb.set_label("Maximum rover speed [m/s]")
plt.xlabel("Coefficient of rolling resistance, Crr [-]")
plt.ylabel("Terrain slope [deg]")
plt.title("Max Rover Speed vs. Rolling Resistance and Terrain Slope\n(blank = no terminal speed)")
plt.show()

