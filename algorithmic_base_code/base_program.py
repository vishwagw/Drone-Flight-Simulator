# basic test program:
mport numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Drone simulation class:
class Dronesim:
    def __init__(self):
        # Initial state [x, y, z, vx, vy, vz]
        self.state = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # Physical parameters
        self.mass = 1.0  # kg
        self.g = 9.81    # m/s^2
        self.dt = 0.01   # simulation timestep
        
        # Control limits
        self.max_thrust = 20.0  # Newtons
        self.max_tilt = np.pi/4  # 45 degrees
        
        # History for plotting
        self.position_history = []
        self.time_history = []

    def dynamics(self, control_input):

        # control_input = [thrust, roll_angle, pitch_angle]
        thrust = np.clip(control_input[0], 0, self.max_thrust)
        roll = np.clip(control_input[1], -self.max_tilt, self.max_tilt)
        pitch = np.clip(control_input[2], -self.max_tilt, self.max_tilt)

        # Current state
        x, y, z, vx, vy, vz = self.state
        
        # Calculate accelerations
        ax = (thrust/self.mass) * np.sin(pitch)
        ay = (thrust/self.mass) * np.sin(roll)
        az = (thrust/self.mass) * np.cos(roll) * np.cos(pitch) - self.g
        
        # State derivatives
        derivatives = np.array([vx, vy, vz, ax, ay, az])
        return derivatives
    
    def update(self, control_input):

        k1 = self.dynamics(control_input)
        k2 = self.dynamics(control_input) * self.dt/2 + k1
        k3 = self.dynamics(control_input) * self.dt/2 + k2
        k4 = self.dynamics(control_input) * self.dt + k3
        
        self.state += (self.dt/6.0) * (k1 + 2*k2 + 2*k3 + k4)

        # Store history
        self.position_history.append(self.state[:3].copy())
        self.time_history.append(len(self.time_history) * self.dt)

    # getting the position of UAV
    def get_position(self):
        return self.state[:3]
    
    # getting the velocity of UAV
    def get_velocity(self):
        return self.state[:3]
    
# Flight controller class:
class FlightController:
    def __init__(self):
        # PID controller gains
        self.kp = 2.0
        self.ki = 0.1
        self.kd = 0.5

        # Error accumulation for integral term
        self.error_integral = np.zeros(3)

    # controller function:
    def control(self, current_pos, target_pos, current_vel):
        """Simple PID controller for position control"""
        error = target_pos - current_pos
        
        # Update integral term
        self.error_integral += error
        
        # Derivative term
        error_derivative = -current_vel
        
        # Calculate control output
        control = (self.kp * error + 
                  self.ki * self.error_integral + 
                  self.kd * error_derivative)
        
        # Convert to thrust and angles
        thrust = np.clip(np.linalg.norm(control) + 9.81, 0, 20.0)
        if thrust > 0:
            pitch = np.arctan2(control[0], control[2])
            roll = np.arctan2(control[1], control[2])
        else:
            pitch = 0.0
            roll = 0.0
            
        return np.array([thrust, roll, pitch])
    
# function for running simulation:
def run_simulation():
    # Initialize simulator and controller
    drone = Dronesim()
    controller = FlightController()

    # Target position
    target = np.array([5.0, 5.0, 10.0])  # x, y, z in meters
    
    # Simulation parameters
    sim_time = 10.0  # seconds
    steps = int(sim_time / drone.dt)
    
    # Run simulation
    for _ in range(steps):
        current_pos = drone.get_position()
        current_vel = drone.get_velocity()
        
        # Get control input from controller
        control_input = controller.control(current_pos, target, current_vel)
        
        # Update simulation
        drone.update(control_input)
    
    # Plot results
    plot_trajectory(drone.position_history, target)

# function for plotting the drone trajectory:
def plot_trajectory(position_history, target):
    positions = np.array(position_history)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot trajectory
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'b-', label='Flight Path')
    
    # Plot target
    ax.scatter(target[0], target[1], target[2], c='r', marker='o', label='Target')
    
    # Plot starting point
    ax.scatter(0, 0, 0, c='g', marker='o', label='Start')
    
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_zlabel('Z (m)')
    ax.set_title('Drone Flight Trajectory')
    ax.legend()
    
    plt.show()

# running the entire program:
if __name__ == "__main__":
    run_simulation()
