import serial
import numpy as np
import open3d as o3d
import time

PORT = "COM3"      # change this
BAUD = 115200

# If your Arduino sends cm, set this to 0.01 to convert to meters
SCALE = 0.01

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # let Arduino reset

points = []

pcd = o3d.geometry.PointCloud()
vis = o3d.visualization.Visualizer()
vis.create_window("Live Point Cloud")

added = False
last_update = time.time()

try:
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue

        try:
            x_str, y_str, z_str = line.split(",")
            x, y, z = float(x_str)*SCALE, float(y_str)*SCALE, float(z_str)*SCALE
        except ValueError:
            continue

        # Optional: ignore zero/garbage points
        if x == 0 and y == 0 and z == 0:
            continue

        points.append([x, y, z])

        # Update visualization ~10 times/sec (not every point)
        if time.time() - last_update > 0.1 and len(points) > 10:
            pts = np.array(points, dtype=np.float64)
            pcd.points = o3d.utility.Vector3dVector(pts)

            if not added:
                vis.add_geometry(pcd)
                added = True
            else:
                vis.update_geometry(pcd)

            vis.poll_events()
            vis.update_renderer()
            last_update = time.time()

except KeyboardInterrupt:
    pass
finally:
    ser.close()
    vis.destroy_window()

# Save at end
o3d.io.write_point_cloud("scan.ply", pcd)
print("Saved scan.ply")

