
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
