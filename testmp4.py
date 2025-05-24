import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
line, = ax.plot([], [])
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

def animate(frame):
    line.set_data([0, 10], [0, 0.1*frame])
    return line,

ani = animation.FuncAnimation(fig, animate, frames=100)
ani.save('test.mp4', writer='ffmpeg', fps=30)