import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Drone class to hold state and behavior
class Drone:
    def __init__(self):
        self.mass = 1.0  # kg
        self.pos = 0.0   # meters (height)
        self.vel = 0.0   # m/s
        self.acc = 0.0   # m/s^2
        self.thrust = 0.0  # Newtons
        self.gravity = -9.81  # m/s^2
        self.target_height = 10.0  # meters (for takeoff)
        self.landed = False

    def update(self, dt):
        # Net force: thrust + gravity
        net_force = self.thrust + (self.mass * self.gravity)
        self.acc = net_force / self.mass

        # Update velocity and position (Euler integration)
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        # Prevent drone from going below ground
        if self.pos <= 0:
            self.pos = 0
            self.vel = 0 if self.thrust == 0 else self.vel
            self.landed = True if self.thrust == 0 else False

    def control(self, t):
        # Simple autonomous control logic
        if t < 5:  # Takeoff phase (first 5 seconds)
            if self.pos < self.target_height:
                self.thrust = 15.0  # Enough to overcome gravity and rise
            else:
                self.thrust = -self.mass * self.gravity  # Hover (thrust = weight)
        elif t < 10:  # Hover phase
            self.thrust = -self.mass * self.gravity  # Maintain hover
        else:  # Landing phase
            if self.pos > 0:
                self.thrust = 5.0  # Reduce thrust to descend
            else:
                self.thrust = 0.0  # Landed, turn off thrust

# Simulation parameters
dt = 0.05  # Time step (seconds)
time = np.arange(0, 15, dt)  # Simulate 15 seconds
drone = Drone()
positions = []

# Run simulation
for t in time:
    drone.control(t)
    drone.update(dt)
    positions.append(drone.pos)

# Visualization
fig, ax = plt.subplots()
ax.set_xlim(0, 15)
ax.set_ylim(0, 15)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Height (m)')
ax.set_title('Drone Autonomous Takeoff and Landing')
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    x = time[:i]
    y = positions[:i]
    line.set_data(x, y)
    return line,

ani = FuncAnimation(fig, animate, init_func=init, frames=len(time), interval=20, blit=True)
plt.grid()
plt.show()