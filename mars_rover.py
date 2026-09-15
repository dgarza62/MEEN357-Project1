import math
import scipy as sy

# connect to static ip

# High speed entry into Martian atmosphere

# Parachute deployment and deceleration

# Powered descent

# Sky Crane operation
# Rover is lowered gently to Martian surface
# From a hovering platform


# Once rover on the ground
# System modeling and preliminary analysis of the rover

# Dynamical modeling and analysis of the rover

# Simulation of landing phase

# System optimization / Decision making


wheel = {'radius': 0.3,
         'mass': 1.0}
speed_reducer = {'type': 'reverted',
                  'diam_pinion': 0.04,
                  'diam_gear': 0.07,
                  'mass': 1.5}
motor = {'torque_stall': 170,
         'torque_noload': 0,
         'speed_noload': 3.80,
         'mass': 5.0}
wheel_assembly = {'wheel': wheel,
                  'speed_reducer': speed_reducer,
                  'motor': motor,}
chassis = {'mass': 659}
science_payload = {'mass': 75}
power_subsys = {'mass': 90}
planet = {'g': 3.72}
rover = {'name': 'Marvin the Martian',
         'wheel_assembly': wheel_assembly,
         'chassis': chassis,
         'science_payload': science_payload,
         'power_subsys': power_subsys}

# DC Motor, Speed Reducer, Drive Wheel
def get_mass():
    mass = 6*wheel['mass']+(6*motor['mass'])+science_payload['mass']+power_subsys['mass']+chassis['mass']+speed_reducer['mass']
    return mass
def get_gear_ratio():
    gear_ratio = (speed_reducer['diam_gear']/speed_reducer['diam_pinion']) ** 2
    return gear_ratio
def tau_dcmotor():
    shaft_speed = int(input("what is the shaft speed (rad/s)? "))

    shaft_torque = motor['torque_stall'] - ((motor['torque_stall']-motor['torque_noload'])/(motor['speed_noload']))*shaft_speed
    shaft_speed = motor['speed_noload']*(1 - ((shaft_torque - motor['torque_noload'])/(motor['torque_stall']-motor['torque_noload'])))

    return shaft_speed, shaft_torque
def F_drive():
    # Wheel assembly details
    alpha = int(input("what is the angle of the inclined terrain? "))
    C_rr = int(input("what is the rolling resistance coefficient? "))
    v = int(input("what is the velocity of the rover (m/s)? "))

    F_rrs = C_rr*get_mass()*planet['g']*math.cos(math.radians(alpha))
    F_rr = math.erf(40*v)*(F_rrs)

    F_d = F_rr + get_mass()*planet['g']*math.sin(math.radians(alpha))

    return F_rrs, F_rr, F_d, alpha
def F_gravity():

    alpha = int(input("what is the angle of the inclined terrain? "))
    F_xg = get_mass()*planet['g']*math.cos(math.radians(alpha))
    F_yg = get_mass()*planet['g']*math.sin(math.radians(alpha))

    F_g = math.sqrt(F_xg**2 + F_yg**2)

    return F_xg, F_yg, F_g, alpha
def F_rolling():
    F_rrs, F_rr, _, _ = F_drive()

    F_rrt = math.sqrt((F_rr)**2 + (F_rrs)**2)

    return F_rrt
def F_net():
    _, _, F_d, alpha = F_drive()
    normal_force = get_mass()*planet['g']*math.cos(math.radians(alpha))

    # Translational Force
    F_net = math.sqrt((normal_force)**2 + (F_d)**2)
    return F_net




