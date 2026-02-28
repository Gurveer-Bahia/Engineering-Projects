import numpy as np
import matplotlib.pyplot as plt


class Car:
    def __init__(self, name, frontal_area, engine_force):
        self.name = name
        self.A = frontal_area          # m^2
        self.engine_force = engine_force  # N
        self.rho = 1.225               # air density (kg/m^3)

    def aerodynamic_coefficients(self, wing_angle):
        """
        Simple linear model for drag and lift coefficients.
        In reality these would be nonlinear and CFD-derived.
        """
        C_d = 0.30 + 0.02 * wing_angle
        C_L = 0.50 + 0.05 * wing_angle
        return C_d, C_L

    def simulate(self, wing_angles):
        top_speeds = []
        downforces = []
        drags = []

        for angle in wing_angles:
            C_d, C_L = self.aerodynamic_coefficients(angle)

            # Top speed approximation (engine force balances drag)
            v = np.sqrt((2 * self.engine_force) / (self.rho * C_d * self.A))

            drag = 0.5 * self.rho * C_d * self.A * v**2
            downforce = 0.5 * self.rho * C_L * self.A * v**2

            top_speeds.append(v)
            drags.append(drag)
            downforces.append(downforce)

        return np.array(top_speeds), np.array(downforces), np.array(drags)


class Simulation:
    def __init__(self, wing_angles):
        self.wing_angles = wing_angles
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def run(self):
        plt.figure(figsize=(10, 6))

        for car in self.cars:
            speeds, downforces, drags = car.simulate(self.wing_angles)

            plt.plot(self.wing_angles, speeds, label=f"{car.name} Speed")

        plt.xlabel("Rear Wing Angle (degrees)")
        plt.ylabel("Top Speed (m/s)")
        plt.title("Effect of Wing Angle on Top Speed")
        plt.legend()
        plt.grid(True)
        plt.show()

        plt.figure(figsize=(10, 6))

        for car in self.cars:
            speeds, downforces, drags = car.simulate(self.wing_angles)
            plt.plot(self.wing_angles, downforces, label=f"{car.name} Downforce")

        plt.xlabel("Rear Wing Angle (degrees)")
        plt.ylabel("Downforce (N)")
        plt.title("Effect of Wing Angle on Downforce")
        plt.legend()
        plt.grid(True)
        plt.show()


# -------------------------
# Run Simulation
# -------------------------

if __name__ == "__main__":
    wing_angles = np.linspace(0, 15, 30)

    car1 = Car("Formula Student", frontal_area=1.2, engine_force=5000)
    car2 = Car("F1 Concept", frontal_area=1.0, engine_force=7000)

    sim = Simulation(wing_angles)
    sim.add_car(car1)
    sim.add_car(car2)

    sim.run()