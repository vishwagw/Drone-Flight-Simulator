import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class DroneSimulator:
    def __init__(self):
        # Physical parameters
        self.mass = 1.0  # kg
        self.gravity = 9.81  # m/s^2
        self.max_thrust = 25.0  # N
        self.dt = 0.01  # simulation time step (s)
        
        # Initial state
        self.height = 0.0  # m
        self.velocity = 0.0  # m/s
        self.acceleration = 0.0  # m/s^2
        self.time = 0.0
        
        # Control parameters
        self.target_height = 5.0  # m
        self.hover_duration = 5.0  # s
        self.state = "takeoff"  # takeoff, hover, landing
        
        # Data logging
        self.time_history = []
        self.height_history = []
        self.thrust_history = []

    def pid_controller(self, target, current, velocity, kp=2.0, ki=0.1, kd=0.5):
        """Simple PID controller for height control"""
        error = target - current
        self.integral = getattr(self, 'integral', 0) + error * self.dt
        derivative = -velocity  # velocity is already the derivative of position
        thrust = kp * error + ki * self.integral + kd * derivative
        # Add weight compensation
        thrust += self.mass * self.gravity
        return np.clip(thrust, 0, self.max_thrust)

    def update_physics(self, thrust):
        """Update drone physics based on thrust input"""
        # Calculate net force
        net_force = thrust - (self.mass * self.gravity)
        self.acceleration = net_force / self.mass
        
        # Update velocity and position
        self.velocity += self.acceleration * self.dt
        self.height += self.velocity * self.dt
        
        # Prevent drone from going below ground
        if self.height < 0:
            self.height = 0
            self.velocity = 0 if self.velocity < 0 else self.velocity
            
        self.time += self.dt

    def control_logic(self):
        """Autonomous flight control logic"""
        if self.state == "takeoff":
            thrust = self.pid_controller(self.target_height, self.height, self.velocity)
            if abs(self.target_height - self.height) < 0.1 and abs(self.velocity) < 0.1:
                self.state = "hover"
                self.hover_start = self.time
                
        elif self.state == "hover":
            thrust = self.pid_controller(self.target_height, self.height, self.velocity)
            if self.time - self.hover_start >= self.hover_duration:
                self.state = "landing"
                
        elif self.state == "landing":
            thrust = self.pid_controller(0, self.height, self.velocity)
            if self.height < 0.1 and abs(self.velocity) < 0.1:
                thrust = 0
                
        return thrust

    def simulate(self):
        """Run the simulation"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        def animate(frame):
            # Clear previous frame
            ax1.cla()
            ax2.cla()
            
            # Calculate control input
            thrust = self.control_logic()
            
            # Update physics
            self.update_physics(thrust)
            
            # Log data
            self.time_history.append(self.time)
            self.height_history.append(self.height)
            self.thrust_history.append(thrust)
            
            # Plot height
            ax1.plot(self.time_history, self.height_history, 'b-', label='Height')
            ax1.set_ylabel('Height (m)')
            ax1.set_title(f'Drone State: {self.state}')
            ax1.grid(True)
            ax1.set_ylim(0, self.target_height * 1.5)
            ax1.legend()
            
            # Plot thrust
            ax2.plot(self.time_history, self.thrust_history, 'r-', label='Thrust')
            ax2.set_xlabel('Time (s)')
            ax2.set_ylabel('Thrust (N)')
            ax2.grid(True)
            ax2.set_ylim(0, self.max_thrust * 1.2)
            ax2.legend()
            
            # Stop simulation when landing is complete
            if self.state == "landing" and self.height < 0.1 and abs(self.velocity) < 0.1:
                ani.event_source.stop()

        # Create animation
        ani = FuncAnimation(fig, animate, frames=None, interval=10, repeat=False)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    drone = DroneSimulator()
    drone.simulate()