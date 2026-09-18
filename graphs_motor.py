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


# ---- Motor curves ----
omega = np.linspace(0, motor["speed_noload"], 200)
tau = tau_dcmotor(omega, motor)
P = tau * omega

plt.figure(figsize=(7, 10))
plt.subplot(3, 1, 1)
plt.plot(tau, omega)
plt.xlabel("Motor shaft torque [Nm]")
plt.ylabel("Motor shaft speed [rad/s]")
plt.title("DC Motor: Speed vs. Torque")
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(tau, P)
plt.xlabel("Motor shaft torque [Nm]")
plt.ylabel("Motor power [W]")
plt.title("DC Motor: Power vs. Torque")
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(omega, P)
plt.xlabel("Motor shaft speed [rad/s]")
plt.ylabel("Motor power [W]")
plt.title("DC Motor: Power vs. Speed")
plt.grid(True)

plt.tight_layout()
plt.show()

