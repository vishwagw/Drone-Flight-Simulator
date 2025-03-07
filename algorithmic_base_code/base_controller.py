# using the simulator without a physical drone:

# libs:
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from abc import ABC, abstractmethod

# class for simulator:
class BaseController(ABC):
    @abstractmethod
    def control(self, current_pos, target_pos, current_vel):
        """Returns control input [thrust, roll, pitch]"""
        pass
