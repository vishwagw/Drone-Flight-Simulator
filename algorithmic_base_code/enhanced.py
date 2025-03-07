# controlling  with enhanced mode:
class DroneSimulator:
    def __init__(self):
        # ... existing code ...
        self.energy_used = 0.0
        self.error_history = []

    def update(self, control_input):
        # ... existing code ...
        self.energy_used += control_input[0] * self.dt  # Simple energy model
        if hasattr(self, 'target'):
            self.error_history.append(np.linalg.norm(self.state[:3] - self.target))

def run_simulation(controller, target=None, waypoints=None):
    drone = DroneSimulator()
    drone.target = target if target is not None else waypoints[-1]
    # ... existing code ...
    
    print(f"Total Energy Used: {drone.energy_used:.2f} Joules")
    print(f"Average Position Error: {np.mean(drone.error_history):.2f} meters")

# adding environmental factors:
class DroneSimulator:
    def dynamics(self, control_input):
        derivatives = # ... existing code ...
        wind = np.random.normal(0, 0.1, 3)  # Random wind gusts
        derivatives[3:] += wind
        return derivatives
