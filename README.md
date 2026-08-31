# F1 Fastest Lap Analysis

A Python-based Formula 1 telemetry analysis and visualisation project using FastF1.

This project retrieves Formula 1 telemetry data and visualises the fastest qualifying lap of Max Verstappen at the 2025 Italian Grand Prix at Monza.

## Preview

![Verstappen Fastest Lap](Verstappen_Fastest_Lap_2025.gif)

## Requirements

- Python 3.9 or later
- FastF1
- NumPy
- Matplotlib

Install the required packages using:

```bash
pip install -r requirements.txt
```
## Performance Note

Generating the GIF animation can take some time.

If you only want to run the telemetry analysis and visualisation without saving the animation, comment out the following line in `FastestLap.py`:

```python
animation.save("Verstappen_Fastest_Lap_2025.gif")
```
