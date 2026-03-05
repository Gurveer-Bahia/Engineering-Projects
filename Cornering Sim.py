# cornering.py
from Python_Aerodynamics_Sim import Car
import numpy as np
import matplotlib.pyplot as plt

def max_cornering_speed(car, wing_angles, turn_radius, mu=1.6):
    """
    Compute max cornering speed for a range of wing angles
    car: Car object from simulation.py
    wing_angles: array of wing angles in degrees
    turn_radius: radius of the corner in meters
    mu: tire friction coefficient
    """
    speeds = []
    for angle in wing_angles:
        # Use car's own cornering speed as initial guess for faster convergence
        try:
            v = car.cornering_speed(turn_radius, angle)
        except:
            v = 10.0  # fallback if not available

        converged = False
        for i in range(100):
            F_down = car.downforce(v, angle)
            v_new = np.sqrt(mu * (car.mass * 9.81 + F_down) * turn_radius / car.mass)
            if abs(v_new - v) < 1e-3:
                converged = True
                break
            v = v_new

        if not converged:
            print(f"Warning: max_cornering_speed did not converge for {car.name} at wing angle {angle}")

        speeds.append(v_new)

    return np.array(speeds)

if __name__ == "__main__":
    wing_angles = np.linspace(0, 15, 30)  # degrees
    turn_radius = 50  # meters, can generalize for different corners

    car1 = Car("Formula Student", 300, 1.2, 550000)
    car2 = Car("F1 Concept", 795, 1.5, 300000)

    cars = [car1, car2]

    plt.figure(figsize=(10,6))
    for car in cars:
        speeds = max_cornering_speed(car, wing_angles, turn_radius)
        plt.plot(wing_angles, speeds * 3.6, label=f"{car.name} Max Cornering Speed")

    plt.xlabel("Wing Angle (degrees)")
    plt.ylabel("Max Cornering Speed (km/h)")
    plt.title("Effect of Wing Angle on Cornering Speed")
    plt.grid(True)
    plt.legend()
    plt.show()