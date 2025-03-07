# use this code for multiple trails:
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