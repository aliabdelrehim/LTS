import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
distance = [-0.02769001998697629, 0.6749176908838481, 9.74333333333333, 20.09413327976363, 31.009999999999998, 39.62584963359234, 52.343333333333334, 59.20152919361336, 73.74333333333334, 78.83599961323193] 
slip_angle = [3.1957987068484917, 2.6132207702027275, -0.8257000476216073, 1.8279299673920055, 5.7882350246592065, 5.9002091496289575, 1.5251639350227058, -1.1276291815672637, 0.4154265951637204, 0.7031204775825364]

fig, ax = plt.subplots()

line2 = ax.plot(distance[0], slip_angle[0], label=f'a7a2')

print(line2)
line2 = line2[0]
print(line2)

ax.set(xlim=[0, 100], ylim=[-10, 10], xlabel='distance [m]', ylabel='Angle [deg]')
ax.legend()


def update(frame):
    # for each frame, update the data stored on each artist.
    # update the line plot:
    line2.set_xdata(distance[:frame])
    line2.set_ydata(slip_angle[:frame])
    return (line2)

ani = animation.FuncAnimation(fig=fig, func=update, frames=10, interval=0.0001)
plt.show()