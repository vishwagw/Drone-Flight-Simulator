# running the simulation:
def run_simulation(controller, target=None, waypoints=None):
    drone = DroneSimulator()
    
    # Use waypoints if provided, otherwise use single target
    sim_time = 15.0
    steps = int(sim_time / drone.dt)
    
    for _ in range(steps):
        current_pos = drone.get_position()
        current_vel = drone.get_velocity()
        
        # Pass appropriate target to controller
        if waypoints is not None:
            control_input = controller.control(current_pos, None, current_vel)
        else:
            control_input = controller.control(current_pos, target, current_vel)
        
        drone.update(control_input)
    
    plot_trajectory(drone.position_history, target if target is not None else waypoints[-1])
