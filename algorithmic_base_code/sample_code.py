# using the simulator without a physical drone:

# libs:
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from abc import ABC, abstractmethod

# base controller class for flight controller:
class BaseController(ABC):
    @abstractmethod
    def control(self, current_pos, target_pos, current_vel):
        """Returns control input [thrust, roll, pitch]"""
        pass

# algorithm 1
# class for PID controller testing:
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
    
