import numpy as np
import matplotlib.pyplot as plt


class Car:
    def __init__(self, name, mass, frontal_area, engine_power):
        self.name = name
        self.mass = mass
        self.A = frontal_area
        self.engine_power = engine_power  # in Watts
        self.rho = 1.225             # air density (kg/m^3)

    def aerodynamic_coefficients(self, wing_angle):
        """
        Simple linear model for drag and lift coefficients.
        In reality these would be nonlinear and CFD-derived.
        """
        C_d = 0.70 + 0.02 * wing_angle
        C_L = 0.50 + 0.05 * wing_angle
        return C_d, C_L

    def simulate(self, wing_angles):
        top_speeds = []
        downforces = []
        drags = []

        for angle in wing_angles:
            C_d, C_L = self.aerodynamic_coefficients(angle)

            # Top speed approximation using power balance (drag-limited)
            v = ((2 * self.engine_power) / (self.rho * C_d * self.A))**(1/3)

            # Convert to km/h for realistic graph display
            v = v * 3.6

            drag = 0.5 * self.rho * C_d * self.A * (v/3.6)**2
            downforce = 0.5 * self.rho * C_L * self.A * (v/3.6)**2

            top_speeds.append(v)
            drags.append(drag)
            downforces.append(downforce)

        return np.array(top_speeds), np.array(downforces), np.array(drags)
    
    def downforce(self, velocity, wing_angle):
        C_d, C_L = self.aerodynamic_coefficients(wing_angle)
        return 0.5 * self.rho * C_L * self.A * velocity**2
    
    def drag(self, velocity, wing_angle):
        C_d, C_L = self.aerodynamic_coefficients(wing_angle)
        return 0.5 * self.rho * C_d * self.A * velocity**2
    
    def cornering_speed(self, radius, wing_angle, mu=1.7):
        """
        Calculates the maximum cornering speed with proper physics.
        - For normal/tight corners: uses iterative solver with downforce and friction.
        - For extremely large radii: approximates straight-line top speed (drag-limited).
        """
        g = 9.81
        C_d, C_L = self.aerodynamic_coefficients(wing_angle)

        # Stress check: extremely large radius
        if radius > 1e4:  # threshold for "very gentle corner"
            # Return drag-limited straight-line top speed
            return ((2 * self.engine_power) / (self.rho * C_d * self.A))**(1/3)
        
        # Iterative solver for normal corners
        v = 5.0  # initial guess m/s

        for _ in range(100):
            F_down = 0.5 * self.rho * C_L * self.A * v**2
            normal_force = self.mass * g + F_down
            max_lat_force = mu * normal_force
            v_new = np.sqrt(max_lat_force * radius / self.mass)

            v_new = max(v_new, 0.1)  # prevent zero/negative

            if abs(v_new - v) < 1e-4:
                break
            v = v_new

        return v

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
        plt.ylabel("Top Speed (km/h)")
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

    car1 = Car("Formula Student", 300, 1.2, 5000)
    car2 = Car("F1 Concept", 700, 1.0, 7000)

    sim = Simulation(wing_angles)
    sim.add_car(car1)
    sim.add_car(car2)

    sim.run()