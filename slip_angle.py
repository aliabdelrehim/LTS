import math

import fastf1 as ff1
from fastf1 import plotting
import numpy as np
from matplotlib import pyplot as plt

import matplotlib.animation as animation
import os


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
telemetry_driver = fastest_driver_lap.get_telemetry()


v = telemetry_driver['Speed'] / 3.6    # Speed in m/s
time_float = telemetry_driver['Time'] / np.timedelta64(1, 's')    # Time as a float variable instead of a date - telemetry driver has time as date


# We calculate the longitudinal acceleration and filter it
a_long = np.gradient(v)/np.gradient(time_float)
a_long_smooth = np.convolve(a_long, np.ones((3,))/3, mode = 'same')


# Get position and time data
X = telemetry_driver['X'].values
Y = telemetry_driver['Y'].values
time = time_float.values  # Time array from your existing code

# car_data = fastest_driver_lap.get_car_data()

# Calculate derivatives
dt = np.gradient(time_float)
dX = np.gradient(X)
dY = np.gradient(Y)

# Velocity components from position data
vx = dX / dt
vy = dY / dt
v_mag = np.sqrt(vx**2 + vy**2)  # Ground speed magnitude

# Acceleration components
ax = np.gradient(vx) / dt
ay = np.gradient(vy) / dt

# We calculate the longitudinal acceleration and filter it
ax = np.gradient(v)/np.gradient(time_float)
ax_smooth = np.convolve(ax, np.ones((3,))/3, mode = 'same')

# Calculate lateral acceleration (component perpendicular to velocity direction)
a_lat = (vx * ay - vy * ax) / v_mag

# Smooth lateral acceleration
a_lat_smooth = np.convolve(a_lat, np.ones(3)/3, mode='same')

# Vehicle parameters
m = 750  # Total vehicle mass [kg]
C_alpha = 80000  # Cornering stiffness [N/rad]
C_kappa = 100000  # longitudinal stiffness [N]

# Calculate slip angle (convert from force to angle)
Fy_total = m * a_lat_smooth
slip_angle = -Fy_total / (2 * C_alpha)  # Assuming two tires contribute equally
slip_angle_deg = np.degrees(slip_angle)  # Convert to degrees

Fx_total = m * ax
slip_ratio = Fx_total / (2 * C_kappa)

lap_time_str = str(fastest_driver_lap['LapTime']).replace("0 days ", "")
print(f"Fastest Lap Time: {fastest_driver_lap['LapTime']}")
print("xxx", telemetry_driver['Distance'][:10], slip_angle_deg[:10].tolist())

distance = telemetry_driver['Distance'].values
slip_angle = slip_angle_deg

#########################################################################################################################3
#Plot distance against slip angle

# # 1. DATA OPTIMIZATION ========================================================
# # Downsample data (keep every 5th point)
# downsample = 2
# distance = distance[::downsample]  # Replace with your actual distance data (numpy array)
# slip_angle = slip_angle[::downsample]  # Replace with your slip angle data (numpy array)

# # 2. BLITTING SETUP ==========================================================
# fig, ax = plt.subplots()
# ax.set(xlim=(distance.min(), distance.max()),  # Remove dynamic limits
#      ylim=(slip_angle.min(), slip_angle.max()),
#      xlabel='Distance [m]',
#      ylabel='Angle [deg]')
# line, = ax.plot([], [], lw=1)  # Empty line object
# ax.legend(['Slip Angle'])

# # 3. PRE-COMPUTE FRAME DATA ==================================================
# # Pre-slice all possible frame data upfront
# x_frames = [distance[:k] for k in range(len(distance))]
# y_frames = [slip_angle[:k] for k in range(len(distance))]

# # 4. OPTIMIZED UPDATE FUNCTION ===============================================
# def update(frame):
#     line.set_data(x_frames[frame], y_frames[frame])
#     return line,

# # 5. HIGH-PERFORMANCE RENDERING ==============================================
# ani = animation.FuncAnimation(
#     fig=fig,
#     func=update,
#     frames=len(distance),
#     interval=10,  # 10ms = 100 FPS cap (system-dependent)
#     blit=True,     # Critical for speed
#     cache_frame_data=False
# )

# plt.show()
# ########################################################################################################

# #plot distance against fx and fy

# #1. DATA OPTIMIZATION ========================================================
# # Downsample data (keep every 5th point)
# downsample = 1
# distance = distance[::downsample]  # Replace with your actual distance data (numpy array)
# Fx_total = Fx_total[::downsample]  # Replace with your slip angle data (numpy array)
# Fy_total = Fy_total[::downsample]


# # 2. BLITTING SETUP ==========================================================
# fig, ax = plt.subplots(figsize=(12,6))

# # added dynamic limits
# ax.set(xlim=(distance.min()-0.05*distance.max(), distance.max()*1.1),  
#      ylim=(min(min(Fx_total), min(Fy_total))*1.1, max([max(Fx_total), max(Fy_total)])*1.1),
#      xlabel='Distance [m]',
#      ylabel='Force [deg]')
# line1, = ax.plot([], [], lw=2, label= 'Longtudinal Force [N]', color = 'red')  # Empty line object, to take [0] as ax.plot returns array of lines on axis of canvas, we have only one line so we choose 1 elemnt in this case
# line2, = ax.plot([], [], lw=2, label= 'Lateral Force [N]', color = 'blue', ls = '--')
# ax.set_xlabel('Distance [m]')
# ax.set_ylabel('Force [N]')
# ax.set_title(f'Hamilton 2020 Monza Qualifying Lap\n Estimated Lateral/Longitudinal Forces')
# ax.legend()

# # 3. PRE-COMPUTE FRAME DATA ==================================================
# # Pre-slice all possible frame data upfront
# x_frames = [distance[:k] for k in range(len(distance))]
# y_frames1 = [Fx_total[:k] for k in range(len(distance))]
# y_frames2 = [Fy_total[:k] for k in range(len(distance))]

# # 4. OPTIMIZED UPDATE FUNCTION ===============================================
# def update(frame):
#     line1.set_data(x_frames[frame], y_frames1[frame])
#     line2.set_data(x_frames[frame], y_frames2[frame])
#     return line1, line2

# # 5. HIGH-PERFORMANCE RENDERING ==============================================
# ani = animation.FuncAnimation(
#     fig=fig,
#     func=update,
#     frames=len(distance),
#     interval=10,  # 10ms = 100 FPS cap (system-dependent)
#     blit=True,     # Critical for speed
#     cache_frame_data=False
# )

# # animation path
# cwd = os.getcwd()
# save_path = os.path.join(cwd, 'Forces_New.mp4')
# print(f"### Animation will be saved to: {save_path} ###")


# ani.save(
#     'Forces_New.mp4',
#     writer='ffmpeg',          # Required for MP4
#     fps=30,                   # Frames per second
#     dpi=300,                  # Video resolution
#     bitrate=1800,             # Quality (higher = better)
#     progress_callback=lambda i, n: print(f"Saving frame {i}/{n}") 
# )

# plt.close()  # Free up memory after saving

















## Example of animated slip angle
#slicing every x = 2 points to speed up the animation 
# downsample = 2
# distance = distance[::downsample]
# slip_angle = slip_angle[::downsample]

# fig, ax = plt.subplots()
# line2 = ax.plot(distance[0], slip_angle[0], label=f'a7a2')[0]
# ax.set(xlim=[-10, max(distance)*1.1], ylim=[min(slip_angle), max(slip_angle)*1.1], xlabel='distance [m]', ylabel='Angle [deg]')
# ax.legend()

# def update(frame):
#     # for each frame, update the data stored on each artist.
#     # update the line plot:
#     line2.set_xdata(distance[:frame])
#     line2.set_ydata(slip_angle[:frame])
#     return (line2)

# ani = animation.FuncAnimation(fig=fig, func=update, frames=len(distance), interval=0.0001)
# plt.show()








# # Estimated Slip angle - non animated
# plt.figure(figsize=(12, 6))
# plt.plot(telemetry_driver['Distance'], slip_angle_deg, label='Estimated Slip Angle')
# plt.xlabel('Distance (m)')
# plt.ylabel('Slip Angle (degrees)')
# plt.title(f'Hamilton 2020 Monza Qualifying - Estimated Slip Angle\nFastest Lap: {lap_time_str}')
# plt.legend()
# plt.grid()
# plt.show()


# Long. & Lateral Forces vs Distance - non animated
plt.figure(figsize=(12, 6))
plt.plot(telemetry_driver['Distance'], Fx_total, 'r-', label='Longtidunal Force')
plt.plot(telemetry_driver['Distance'], Fy_total, 'b--', label='Lateral Force')

plt.xlabel('Distance [m]')
plt.ylabel('Force [N]')
plt.title(f'Hamilton 2020 Monza Qualifying Lap\n Estimated Lateral/Longitudinal Forces')


plt.legend()
plt.grid()
plt.show()

## Long. & Lateral Forces vs Distance - animated
# downsample = 2  # Keep every 5th point (adjust based on your data length)
# xdata = telemetry_driver['Distance'].values[::downsample]
# Fx_total = Fx_total[::downsample]  # Your longitudinal force array
# Fy_total = Fy_total[::downsample]  # Your lateral force array

# Fx_total = np.asarray(Fx_total)
# Fy_total = np.asarray(Fy_total)
# fig, axis = plt.subplots(figsize=(12, 6))
# line1 = axis.plot(xdata[0], Fx_total[0], color='red', label='Longtidunal Force')[0]
# line2 = axis.plot(xdata[0], Fy_total[0], 'b--', label='Lateral Force')[0]

# axis.set_xlim(xdata.min(), xdata.max())
# axis.set_ylim(min(Fx_total.min(), Fy_total.min()), 
#               max(Fx_total.max(), Fy_total.max()))

# axis.set_xlabel('Distance [m]')
# axis.set_ylabel('Force [N]')
# axis.set_title(f'Hamilton 2020 Monza Qualifying Lap\n Estimated Lateral/Longitudinal Forces')

# axis.legend()
# axis.grid()

# def update(frame):
   
#     line1.set_xdata(xdata[:frame])
#     line1.set_ydata(Fx_total[:frame])
#     line2.set_xdata(xdata[:frame])
#     line2.set_ydata(Fy_total[:frame])
#     return (line1, line2)

# ani = animation.FuncAnimation(fig=fig, func=update, frames=len(xdata)+1, interval=30, blit=True)
# # ani.save("slip_angle.mp4")
# plt.show()




