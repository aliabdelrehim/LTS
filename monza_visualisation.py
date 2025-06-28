"""Draw a track map with numbered corners
=========================================

Use the position data of a single lap to draw a track map.
Then annotate the map with corner numbers.
"""
##############################################################################
# Import FastF1 and load the data. Use the telemetry from the fastest lap for
# the track map.

import matplotlib.pyplot as plt
import numpy as np
import fastf1

# Setup session (updated for FastF1 v3+)
session = fastf1.get_session(2020, 'Monza', 'Q')
session.load()

# Get circuit info and lap data
circuit_info = session.get_circuit_info()  # Now works in v3+
lap = session.laps.pick_fastest()
pos = lap.get_pos_data()
print(pos)

##############################################################################
# Rotation function for correct track orientation

def rotate(xy, *, angle):
    """Rotate coordinates around origin"""
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

##############################################################################
# Process and plot track data

# Get coordinates and rotate
track = pos.loc[:, ('X', 'Y')].to_numpy()
track_angle = np.radians(circuit_info.rotation)  # Convert to radians

rotated_track = rotate(track, angle=track_angle)
plt.plot(rotated_track[:, 0], rotated_track[:, 1], 'k-', linewidth=3)

##############################################################################
# Annotate corners with numbers

offset_vector = [300, 0]  # Adjust this for text positioning

for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    
    # Calculate text position
    offset_angle = np.radians(corner['Angle'])
    offset = rotate(offset_vector, angle=offset_angle)
    text_pos = rotate([corner['X'], corner['Y']] + offset, angle=track_angle)
    
    # Calculate track position
    track_pos = rotate([corner['X'], corner['Y']], angle=track_angle)
    
    # Plot elements
    plt.plot([track_pos[0], text_pos[0]], [track_pos[1], text_pos[1]], 'grey')
    plt.scatter(text_pos[0], text_pos[1], s=150, c='#00009b')
    plt.text(text_pos[0], text_pos[1], txt, ha='center', va='center', 
             color='white', fontsize=8)

##############################################################################
# Finalize plot

plt.title(f"{session.event['EventName']} - {session.event.year}")
plt.axis('equal')
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.show()