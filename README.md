TL;DR
Two servos aim a TF-Mini S LiDAR around a room. Arduino reads distance, converts spherical → Cartesian, and ships (x, y, z) over USB. 
A Python script catches the stream and draws the point cloud in Open3D.

3D LiDAR Scanner

A DIY spherical-coordinate LiDAR scanner built with an Arduino, two servos, and a TF-Mini S sensor. The device sweeps through θ (theta) and φ (phi) angles, measures distance at each point, converts the readings to 3D Cartesian coordinates, and streams them over serial to a Python host program. The host renders the resulting point cloud in real time using Open3D.

## How It Works

The scanner uses a two-axis gimbal made from servos. One servo controls the horizontal sweep (θ), the other controls the vertical tilt (φ). At each angular position, the TF-Mini S measures the distance `r` to the nearest surface. The Arduino converts the spherical coordinates `(r, θ, φ)` into Cartesian `(x, y, z)`:

```
x = r * sin(φ) * cos(θ)
y = r * sin(φ) * sin(θ)
z = r * cos(φ)
```

Each point is sent over the serial bus as a comma-separated triple. The Python script reads the stream, appends points to a buffer, and visualizes the cloud with Open3D.

## Hardware

- Arduino (Uno / Nano / Mega)
- TF-Mini S LiDAR sensor
- 2x servo motors (one for θ, one for φ)
- External 5V power supply for the servos (recommended — the Arduino's onboard regulator can't reliably power both servos plus the LiDAR)
- Mounting bracket / gimbal frame
- Jumper wires

### Wiring

| Component | Arduino Pin |
|-----------|-------------|
| TF-Mini S TX | RX (pin 0 or SoftwareSerial pin) |
| TF-Mini S RX | TX (pin 1 or SoftwareSerial pin) |
| TF-Mini S VCC | 5V |
| TF-Mini S GND | GND |
| θ Servo signal | D9 |
| φ Servo signal | D10 |
| Servo VCC | External 5V |
| Servo GND | GND (shared with Arduino) |

> Note: Using pins 0/1 instead of importing a serial library yields wayyy better results.

## Usage

1. Power up the scanner and connect it to your computer via USB.
2. Identify the serial port:
   - **Windows**: `COM3`, `COM4`, etc.
3. Update the serial port in the Python script (or pass it as an argument, if your script supports it).
4. Run the host program:
   ```bash
   python scanner.py
   ```
5. The Open3D viewer will open and populate with points as the scan progresses.

