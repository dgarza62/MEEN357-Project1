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

# ---- Speed reducer output curves ----
Ng = get_gear_ratio(speed_reducer)
omega_in = np.linspace(0, motor["speed_noload"], 200)
tau_in = tau_dcmotor(omega_in, motor)
tau_out = Ng * tau_in
omega_out = omega_in / Ng
P_out = tau_out * omega_out

plt.figure(figsize=(7, 10))
plt.subplot(3, 1, 1)
plt.plot(tau_out, omega_out)
plt.xlabel("Speed reducer output torque [Nm]")
plt.ylabel("Speed reducer output speed [rad/s]")
plt.title("Speed Reducer Output: Speed vs. Torque")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(tau_out, P_out)
plt.xlabel("Speed reducer output torque [Nm]")
plt.ylabel("Speed reducer output power [W]")
plt.title("Speed Reducer Output: Power vs. Torque")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(omega_out, P_out)
plt.xlabel("Speed reducer output speed [rad/s]")
plt.ylabel("Speed reducer output power [W]")
plt.title("Speed Reducer Output: Power vs. Speed")
plt.grid(True)

plt.tight_layout()
plt.show()

