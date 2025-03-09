# Example of adding your own control method
def your_autonomous_routine(self):
    # Your custom logic here
    if condition:
        self.thrust = your_value
        self.velocity_x = your_speed

# testing different scenarios:
# Example of adding a test sequence
def test_sequence(self):
    if self.state == "IDLE":
        self.takeoff(300)
    elif self.state == "HOVER" and HEIGHT - self.y > 290:
        self.move_to(400)
    # Add more conditions as needed