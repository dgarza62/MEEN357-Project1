import numpy as np
from scipy.special import erf

# (input validation)

def _is_scalar(x):
    return (isinstance(x, (int, float, np.integer, np.floating))
            and not isinstance(x, (bool, np.bool_)))

def _is_scalar_or_vector(x):
    if _is_scalar(x):
        return True
    if isinstance(x, np.ndarray):
        return x.ndim <= 1 and np.issubdtype(x.dtype, np.number)
    return False

def _finish(result, original):
    """Return a float if the original input was a scalar, else an ndarray."""
    if _is_scalar(original) or (isinstance(original, np.ndarray) and original.ndim == 0):
        return float(result)
    return np.asarray(result, dtype=float)

def _require_dict(x, name):
    if not isinstance(x, dict):
        raise Exception('%s must be a dict.' % name)

def _require_angles(angle):
    if not _is_scalar_or_vector(angle):
        raise Exception('terrain_angle must be a scalar or a 1D numpy array.')
    if np.any(np.abs(np.asarray(angle, dtype=float)) > 75):
        raise Exception('All terrain angles must be between -75 and +75 degrees.')

def _require_same_size(a, b):
    if np.shape(a) != np.shape(b):
        raise Exception('omega and terrain_angle must be the same size.')

def _require_Crr(Crr):
    if not _is_scalar(Crr) or Crr <= 0:
        raise Exception('Crr must be a positive scalar.')

# Required functions
def tau_dcmotor(omega, motor):
    """Motor shaft torque [Nm] for motor shaft speed omega [rad/s]."""
    if not _is_scalar_or_vector(omega):
        raise Exception('omega must be a scalar or a 1D numpy array.')
    _require_dict(motor, 'motor')

    w = np.asarray(omega, dtype=float)
    tau_s = motor['torque_stall']
    tau_nl = motor['torque_noload']
    w_nl = motor['speed_noload']

    tau = tau_s - ((tau_s - tau_nl) / w_nl) * w
    tau = np.where(w < 0, tau_s, tau)      # spinning backwards -> stall torque
    tau = np.where(w > w_nl, 0.0, tau)     # faster than no-load -> no torque
    return _finish(tau, omega)

def get_gear_ratio(speed_reducer):
    """Gear ratio Ng of a reverted gear train: (d2/d1)^2."""
    _require_dict(speed_reducer, 'speed_reducer')
    if str(speed_reducer['type']).strip().lower() != 'reverted':
        raise Exception("Unsupported speed reducer type '%s'. Only 'reverted' is "
                        "valid in this phase." % speed_reducer['type'])
    return (speed_reducer['diam_gear'] / speed_reducer['diam_pinion']) ** 2

def get_mass(rover):
    """Total rover mass [kg] (chassis, power, payload, 6 wheel assemblies)."""
    _require_dict(rover, 'rover')
    wa = rover['wheel_assembly']
    per_wheel = wa['wheel']['mass'] + wa['speed_reducer']['mass'] + wa['motor']['mass']
    return (rover['chassis']['mass'] + rover['power_subsys']['mass']
            + rover['science_payload']['mass'] + 6 * per_wheel)

def F_drive(omega, rover):
    """Combined drive force [N] from all six wheels for motor shaft speed omega."""
    if not _is_scalar_or_vector(omega):
        raise Exception('omega must be a scalar or a 1D numpy array.')
    _require_dict(rover, 'rover')

    wa = rover['wheel_assembly']
    tau_in = tau_dcmotor(omega, wa['motor'])
    Ng = get_gear_ratio(wa['speed_reducer'])
    tau_out = Ng * tau_in
    Fd = 6 * tau_out / wa['wheel']['radius']
    return _finish(Fd, omega)

def F_gravity(terrain_angle, rover, planet):
    """Gravity force [N] along the direction of travel (uphill -> negative)."""
    _require_angles(terrain_angle)
    _require_dict(rover, 'rover')
    _require_dict(planet, 'planet')

    ang = np.asarray(terrain_angle, dtype=float)
    Fgt = -get_mass(rover) * planet['g'] * np.sin(np.radians(ang))
    return _finish(Fgt, terrain_angle)

def F_rolling(omega, terrain_angle, rover, planet, Crr):
    """Rolling resistance force [N] summed over six wheels (always <= 0)."""
    if not _is_scalar_or_vector(omega) or not _is_scalar_or_vector(terrain_angle):
        raise Exception('omega and terrain_angle must be scalars or 1D numpy arrays.')
    _require_same_size(omega, terrain_angle)
    _require_angles(terrain_angle)
    _require_dict(rover, 'rover')
    _require_dict(planet, 'planet')
    _require_Crr(Crr)

    wa = rover['wheel_assembly']
    Ng = get_gear_ratio(wa['speed_reducer'])
    v = wa['wheel']['radius'] * np.asarray(omega, dtype=float) / Ng   # rover speed
    ang = np.asarray(terrain_angle, dtype=float)
    Fn = get_mass(rover) * planet['g'] * np.cos(np.radians(ang))       # total normal force
    Frr = -erf(40 * v) * Crr * Fn                                      # 6 x (Fn/6 * Crr)
    return _finish(Frr, omega)

def F_net(omega, terrain_angle, rover, planet, Crr):
    """Net force [N] on the rover in its direction of motion."""
    if not _is_scalar_or_vector(omega) or not _is_scalar_or_vector(terrain_angle):
        raise Exception('omega and terrain_angle must be scalars or 1D numpy arrays.')
    _require_same_size(omega, terrain_angle)
    _require_angles(terrain_angle)
    _require_dict(rover, 'rover')
    _require_dict(planet, 'planet')
    _require_Crr(Crr)

    Fnet = (F_drive(omega, rover)
            + F_gravity(terrain_angle, rover, planet)
            + F_rolling(omega, terrain_angle, rover, planet, Crr))
    return _finish(Fnet, omega)

