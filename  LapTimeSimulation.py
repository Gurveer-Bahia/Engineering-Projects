import numpy as np
import matplotlib.pyplot as plt
from Python_Aerodynamics_Sim import Car


class LapTimeSimulator:
    def __init__(self, car):
        self.car = car
        self.g = 9.81
        self.C_rr = 0.015  # rolling resistance coefficient

        # Each segment: {"length": m, "radius": corner radius or None for straight}
        self.track = [
    {"length": 300, "radius": None},   # Short straight
    {"length": 150, "radius": 35},     # Tight corner
    {"length": 200, "radius": None},   # Straight
    {"length": 180, "radius": 30},     # Tight corner
    {"length": 200, "radius": None},   # Straight
    {"length": 160, "radius": 40},     # Medium corner
    {"length": 150, "radius": 25},     # Very tight corner
    {"length": 250, "radius": None},   # Final straight
]

    def straight_speed(self, wing_angle):
        C_d, _ = self.car.aerodynamic_coefficients(wing_angle)

        # We solve: P = (0.5*rho*Cd*A*v^2 + C_rr*m*g) * v
        # => P = 0.5*rho*Cd*A*v^3 + C_rr*m*g*v
        # Use Newton-Raphson for stable convergence

        rho = self.car.rho
        A = self.car.A
        m = self.car.mass
        P = self.car.engine_power
        R = self.C_rr * m * self.g

        # Initial guess (realistic straight speed ~80 m/s)
        v = 80.0

        for _ in range(50):
            f = 0.5 * rho * C_d * A * v**3 + R * v - P
            df = 1.5 * rho * C_d * A * v**2 + R

            v_new = v - f / df

            if abs(v_new - v) < 1e-6:
                break
            v = v_new

        return max(v, 1.0)

    def lap_time(self, wing_angle):
        total_time = 0

        for segment in self.track:
            length = segment["length"]
            radius = segment["radius"]

            if radius is None:
                v = self.straight_speed(wing_angle)
            else:
                v = self.car.cornering_speed(radius, wing_angle)

            total_time += length / v

        return total_time

    def run_analysis(self, wing_angles):
        lap_times = []

        for angle in wing_angles:
            lap_times.append(self.lap_time(angle))

        lap_times = np.array(lap_times)

        # Plot in seconds
        plt.figure(figsize=(10,6))
        plt.plot(wing_angles, lap_times, marker='o')
        plt.xlabel("Wing Angle (degrees)")
        plt.ylabel("Lap Time (seconds)")
        plt.title(f"{self.car.name} - Wing Angle Optimisation")
        plt.grid(True)
        plt.show()

        optimal_index = np.argmin(lap_times)
        optimal_angle = wing_angles[optimal_index]

        print(f"Optimal Wing Angle: {optimal_angle:.2f} degrees")
        print(f"Minimum Lap Time: {lap_times[optimal_index]:.2f} seconds")

        # Check lap times at specific angles for validation
        check_angles = [0, 5, 10, 15]
        print("\nLap times at selected wing angles:")
        for angle in check_angles:
            time_sec = self.lap_time(angle)
            print(f"  {angle}° -> {time_sec:.2f} seconds")


# -------------------------
# Run Example
# -------------------------

if __name__ == "__main__":
    wing_angles = np.linspace(0, 15, 30)

    car = Car("F1 Concept", 700, 1.7, 550_000)

    simulator = LapTimeSimulator(car)
    simulator.run_analysis(wing_angles)