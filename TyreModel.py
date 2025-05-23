import math
import pandas as pd

import fastf1 as ff1
from fastf1 import plotting
import numpy as np
from matplotlib import pyplot as plt

def TyreModel(slip_angle, slip_ratio, Fz):
    """
    A simple linear tyre model with friction circle.
    alpha: slip angle (rad)
    kappa: slip ratio
    Fz: vertical load (N)
    Ca: cornering stiffness (N/rad)
    Ck: longitudinal stiffness (N)
    mu: friction coefficient

    Returns:
        Fx: Longtidunal Force.
        Fy: Lateral Force.
    """
    
     # Tyre stiffness constants (simplified)
    C_alpha = 80000  # cornering stiffness [N/rad]
    C_kappa = 100000  # longitudinal stiffness [N]

    # Friction coefficient (assumed constant)
    mu = 1.2  # dry asphalt

    # Limit forces using Coulomb friction (Fx² + Fy² ≤ (mu * Fz)²)
    Fx = C_kappa * slip_ratio
    Fy = -C_alpha * slip_angle

    total_force = math.sqrt(Fx ** 2 + Fy ** 2)
    F_max = mu * Fz


    if total_force > F_max:
        scale = F_max/total_force
        Fx = Fx * scale
        Fy = Fy * scale


    return (Fx, Fy)

# Enable the cache by providing the name of the cache folder
ff1.Cache.enable_cache(r'D:\Electric Vehicle Engineering\automotive connectivity')

# Setup plotting
plotting.setup_mpl()

# We choose the session and load it
session = ff1.get_session(2020, 'Monza', 'Q')
session.load()

# We choose the driver and obtain his best lap
driver = 'HAM'

# pick fastest lap of the selected driver
fastest_driver_lap = session.laps.pick_driver(driver).pick_fastest()
telemetry_driver = fastest_driver_lap.get_telemetry().add_distance()

v = telemetry_driver['Speed'] / 3.6    # Speed in m/s
time_float = telemetry_driver['Time'] / np.timedelta64(1, 's')    # Time as a float variable instead of a date - telemetry driver has time as date

# We calculate the longitudinal acceleration and filter it
ax = np.gradient(v)/np.gradient(time_float)
ax_smooth = np.convolve(ax, np.ones((3,))/3, mode = 'same')


print(len(v))

lap_time_str = str(fastest_driver_lap['LapTime']).replace("0 days ", "")
print(f"Fastest Lap Time: {fastest_driver_lap['LapTime']}")



# Test example
slip_angle = 0.05        # rad (~2.8 degrees)
slip_ratio = 0.1         # 10% slip
Fz = 3000                # N (approx. 300 kg)

Fx, Fy = TyreModel(slip_angle, slip_ratio, Fz)



print(f"Fx = {Fx:.2f} N")
print(f"Fy = {Fy:.2f} N")

"""
next step: import slip angle from fastf1 lib"
"""