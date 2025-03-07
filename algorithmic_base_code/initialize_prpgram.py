# initializing the entire program:
# can test different algorithms:
# 
if __name__ == "__main__":
    # Test PID Controller
    pid_controller = PIDController()
    target = np.array([5.0, 5.0, 10.0])
    print("Testing PID Controller...")
    run_simulation(pid_controller, target=target)
    
    # Test Waypoint Controller
    waypoints = np.array([
        [2.0, 2.0, 5.0],
        [5.0, 5.0, 10.0],
        [3.0, 7.0, 8.0]
    ])
    waypoint_controller = WaypointController(waypoints)
    print("Testing Waypoint Controller...")
    run_simulation(waypoint_controller, waypoints=waypoints)