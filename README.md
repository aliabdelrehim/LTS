# F1 Fastest Lap 

A Python-based Formula 1 telemetry analysis and visualisation project using FastF1.

This project retrieves Formula 1 telemetry data and visualises the fastest qualifying lap of Max Verstappen at the 2025 Italian Grand Prix at Monza.

It was produced as a preliminary step to create a lap-time simulation LTS.

## Preview

![Verstappen Fastest Lap](Verstappen_Fastest_Lap_2025.gif)

## Selecting a Different F1 Session

The default configuration in `FastestLap.py` analyses Max Verstappen's fastest qualifying lap at the 2025 Italian Grand Prix.

The session can be changed by modifying the following variables in `FastestLap.py`:

```python
year = 2025
gp = 'Monza'
event = 'Q'
driver = 'VER'
```

Please refer to the documentation on how to choose your desired session: https://docs.fastf1.dev/

## Requirements

- Python 3.9 or later
- FastF1==3.8.3
- NumPy==2.5.2
- Matplotlib==3.11.1

## How to Run

Clone the repository:

```bash
git clone https://github.com/aliabdelrehim/LTS.git
```

Navigate to the project directory:

```bash
cd LTS
```

Install the required packages using:

```bash
pip install -r requirements.txt
```

Run the fastest lap analysis:

```bash
python FastestLap.py
```

## Performance Note

Generating the GIF animation can take some time.

If you only want to run the telemetry analysis and visualisation without saving the animation, comment out the following line in `FastestLap.py`:

```python
animation.save("Verstappen_Fastest_Lap_2025.gif")
```
