import fastf1 as ff1
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# We choose the session and load it
year = 2025
gp = 'Monza'
event = 'Q'
driver = 'VER'

session = ff1.get_session(year, gp, event)
session.load()

#Getting Circuit info ex. circuit name, length, corner count
circuit_info = session.get_circuit_info()

#Choosing a specific driver with his fastest lap in the session
fastest_driver_lap = session.laps.pick_driver(driver).pick_fastest()

# Get telemetry data - use the same source for both position and speed
telemetry = fastest_driver_lap.get_telemetry().add_distance()  # This contains both position and speed

#matrix rotation function as circuit are 90 degrees offset from normal view
def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

# convert the track angle from degrees to rotation - circuit_info.rotation The original rotation angle of the track (in degrees).
# *(Example: Monza's track might be rotated 15° to align with real-world compass directions.)*
track_angle = np.radians(circuit_info.rotation)

#return car position data ex. X-Y Coordinates - lap time 
pos_data = telemetry[['X', 'Y']].to_numpy()

# Get speed data
t = telemetry['Time'].dt.total_seconds().to_numpy()  # Convert to seconds

#calling the function of rotated track 
rotated_track = rotate(pos_data, angle=track_angle)

#split graph into 2/3 ratio for track/plot
fig = plt.figure(figsize=(19.2, 10.8), dpi=100)

ax_track = fig.add_subplot(1, 1, 1)

#plotting the track (driver pencil) line
ax_track.plot(rotated_track[:, 0], rotated_track[:, 1], color ='black')    

#animated variables
time_text = ax_track.text(0.05, 0.95, '', transform=ax_track.transAxes, fontsize=10,
                         bbox=dict(facecolor='white', alpha=0.8))
car_point, = ax_track.plot([], [], 'ro', color = 'blue', markersize=10)

def update(frame):

    # Update time text
    total_seconds = t[frame]
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    time_text.set_text(f"Time: {minutes}:{seconds:06.3f}")

    x, y = rotated_track[frame, 0], rotated_track[frame, 1]
    car_point.set_data([x], [y])
    

    return time_text, car_point

animation = FuncAnimation(
                fig=fig,
                func=update,
                frames=len(telemetry),
                interval=20,
                blit=True,
                repeat=True,
                cache_frame_data=False
)

ax_track.set_title('Verstappen 2025 Monza Qualifying Lap', color='black', fontsize = 16)

#hide x-axis and y-axis limits
ax_track.set_xticks([])
ax_track.set_yticks([])
ax_track.axis('equal')

## save animation into mp4 and gif video and plot
animation.save("Verstappen_Fastest_Lap_2025.gif")
plt.tight_layout()
plt.show()


