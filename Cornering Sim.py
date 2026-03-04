# cornering.py
from Python_Aerodynamics_Sim import Car
import numpy as np
import matplotlib.pyplot as plt

def max_cornering_speed(car, wing_angles, turn_radius, mu=1.2):
    """
    Compute max cornering speed for a range of wing angles
    car: Car object from simulation.py
    wing_angles: array of wing angles in degrees
    turn_radius: radius of the corner in meters
    mu: tire friction coefficient
    """
    speeds = []
    for angle in wing_angles:
        # initial guess
        v = 10
        # iterate because downforce depends on speed
        for _ in range(10):
            F_down = car.downforce(v, angle)
            v_new = np.sqrt(mu * (car.mass * 9.81 + F_down) * turn_radius)
            if abs(v_new - v) < 1e-3:
                break
            v = v_new
        speeds.append(v)
    return np.array(speeds)

if __name__ == "__main__":
    wing_angles = np.linspace(0, 15, 30)  # degrees
    turn_radius = 50  # meters

    car1 = Car("Formula Student", mass=300, frontal_area=1.2, engine_force=5000)
    car2 = Car("F1 Concept", mass=700, frontal_area=1.0, engine_force=7000)

    cars = [car1, car2]

    plt.figure(figsize=(10,6))
    for car in cars:
        speeds = max_cornering_speed(car, wing_angles, turn_radius)
        plt.plot(wing_angles, speeds, label=f"{car.name} Max Cornering Speed")

    plt.xlabel("Wing Angle (degrees)")
    plt.ylabel("Max Cornering Speed (m/s)")
    plt.title("Effect of Wing Angle on Cornering Speed")
    plt.grid(True)
    plt.legend()
    plt.show()