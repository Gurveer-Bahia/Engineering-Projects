import numpy as np
import matplotlib.pyplot as plt
from Python_Aerodynamics_Sim import Car

# Wing angles for simulation
wing_angles = np.linspace(0, 15, 30)

# Realistic F1 corner radius in meters
radius = 1000000000

# Create F1 Car with realistic parameters: mass 700kg, frontal area 1.5m², engine power 750 kW
car = Car("F1 Concept", 700, 1.7, 750_000)

top_speeds = []
corner_speeds = []

for angle in wing_angles:
    # Straight-line top speed using proper power-based formula
    C_d, _ = car.aerodynamic_coefficients(angle)
    v_top = ((2 * car.engine_power) / (car.rho * C_d * car.A))**(1/3)  # m/s
    top_speeds.append(v_top)

    # Cornering speed using physics-based method
    v_corner = car.cornering_speed(radius, angle)
    corner_speeds.append(v_corner)

# Convert to km/h for plotting
top_speeds_kmh = np.array(top_speeds) * 3.6
corner_speeds_kmh = np.array(corner_speeds) * 3.6

# Graph 1: Top Speed
plt.figure(figsize=(10,6))
plt.plot(wing_angles, top_speeds_kmh, marker='o', color='blue', label='Top Speed')
plt.xlabel("Wing Angle (degrees)")
plt.ylabel("Top Speed (km/h)")
plt.title(f"{car.name} - Straight Line Top Speed vs Wing Angle")
plt.grid(True)
plt.legend()
plt.show()

# Graph 2: Cornering Speed
plt.figure(figsize=(10,6))
plt.plot(wing_angles, corner_speeds_kmh, marker='o', color='red', label='Cornering Speed')
plt.xlabel("Wing Angle (degrees)")
plt.ylabel("Cornering Speed (km/h)")
plt.title(f"{car.name} - Cornering Speed vs Wing Angle")
plt.grid(True)
plt.legend()
plt.show()

# Dual-axis comparison
fig, ax1 = plt.subplots(figsize=(10,6))
ax1.set_xlabel("Wing Angle (degrees)")
ax1.set_ylabel("Top Speed (km/h)", color='blue')
ax1.plot(wing_angles, top_speeds_kmh, marker='o', color='blue', label='Top Speed')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.set_ylabel("Cornering Speed (km/h)", color='red')
ax2.plot(wing_angles, corner_speeds_kmh, marker='o', color='red', label='Cornering Speed')
ax2.tick_params(axis='y', labelcolor='red')
ax2.legend(loc='upper right')

plt.title(f"{car.name} - Straight vs Cornering Speed Comparison")
plt.grid(True)
plt.show()