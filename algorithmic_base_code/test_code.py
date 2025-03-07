import numpy as np
import matplotlib.pyplot as plt
import time
from mpl_toolkits.mplot3d import Axes3D
from abc import ABC, abstractmethod

# base controller class:
class BaseController(ABC):
    @abstractmethod
    def control(self, current_pos, target_pos, current_vel):
        """Returns control input [thrust, roll, pitch]"""
        pass

# tor running multiple algorithms:
def compare_algorithms():
    controllers = {
        "PID": PIDController(),
        "Waypoint": WaypointController(waypoints)
    }
    target = np.array([5.0, 5.0, 10.0])
    
    for name, controller in controllers.items():
        print(f"\nTesting {name} Controller...")
        run_simulation(controller, target=target if name == "PID" else None, 
                      waypoints=waypoints if name == "Waypoint" else None)
        
# PID controller testing algorithm:
class PIDController(BaseController):
    def __init__(self):
        self.kp = 2.0
        self.ki = 0.1
        self.kd = 0.5
        self.error_integral = np.zeros(3)

    def control(self, current_pos, target_pos, current_vel):
        error = target_pos - current_pos
        self.error_integral += error
        error_derivative = -current_vel
        
        control = (self.kp * error + 
                  self.ki * self.error_integral + 
                  self.kd * error_derivative)
        
        thrust = np.clip(np.linalg.norm(control) + 9.81, 0, 20.0)
        pitch = np.arctan2(control[0], control[2]) if thrust > 0 else 0.0
        roll = np.arctan2(control[1], control[2]) if thrust > 0 else 0.0
        return np.array([thrust, roll, pitch])
    
