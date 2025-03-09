import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Flight Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrust = 0
        self.mass = 1.0
        self.size = 20
        self.target_altitude = None
        self.target_x = None
        self.is_landed = True
        
    def update(self, dt):
        gravity = 9.81
        
        # Apply physics
        if not self.is_landed:
            # Vertical movement
            acceleration_y = (self.thrust - (self.mass * gravity)) / self.mass
            self.velocity_y += acceleration_y * dt
            self.y += self.velocity_y * dt
            
            # Horizontal movement
            self.x += self.velocity_x * dt
            
            # Ground collision
            if self.y >= HEIGHT - self.size:
                self.y = HEIGHT - self.size
                self.velocity_y = 0
                self.is_landed = True
                self.thrust = 0
            
            # Screen boundaries
            self.x = max(0, min(self.x, WIDTH - self.size))
        
    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (int(self.x), int(self.y), self.size, self.size))
        
    def takeoff(self):
        print("Taking off...")
        self.is_landed = False
        self.target_altitude = HEIGHT - 200  # Target 200 pixels up
        self.thrust = 15.0  # More than gravity*mass (9.81)
        
    def hover(self):
        if self.target_altitude is not None:
            error = self.target_altitude - self.y
            self.thrust = (self.mass * 9.81) + (error * 0.5)  # Basic P control
            self.velocity_x = 0
            print(f"Hovering: thrust={self.thrust:.2f}, y={self.y:.2f}")
            
    def move_to(self, x_target):
        self.target_x = x_target
        error = x_target - self.x
        self.velocity_x = error * 0.2  # Increased gain
        print(f"Moving: vx={self.velocity_x:.2f}, x={self.x:.2f}")
        
    def land(self):
        self.target_altitude = HEIGHT - self.size
        self.thrust = 5.0  # Less than gravity for descent
        self.velocity_x = 0
        print("Landing...")

class FlightSimulator:
    def __init__(self):
        self.drone = Drone(WIDTH//2, HEIGHT-20)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "IDLE"
        
    def update_drone_state(self):
        if self.state == "TAKEOFF":
            self.drone.takeoff()
            if abs(self.drone.y - self.drone.target_altitude) < 5:
                self.state = "HOVER"
                
        elif self.state == "HOVER":
            self.drone.hover()
            
        elif self.state == "MOVING":
            self.drone.move_to(self.drone.target_x)
            self.drone.hover()  # Maintain altitude
            if abs(self.drone.x - self.drone.target_x) < 5:
                self.state = "HOVER"
                
        elif self.state == "LANDING":
            self.drone.land()
            if self.drone.is_landed:
                self.state = "IDLE"
                
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t and self.state == "IDLE":
                        self.state = "TAKEOFF"
                    elif event.key == pygame.K_h and self.state != "IDLE":
                        self.state = "HOVER"
                    elif event.key == pygame.K_m and self.state != "IDLE":
                        self.state = "MOVING"
                        self.drone.target_x = 600
                    elif event.key == pygame.K_l and self.state != "IDLE":
                        self.state = "LANDING"
            
            # Update drone state and physics
            self.update_drone_state()
            self.drone.update(dt)
            
            # Draw
            screen.fill(WHITE)
            pygame.draw.line(screen, BLACK, (0, HEIGHT-2), (WIDTH, HEIGHT-2), 2)
            self.drone.draw(screen)
            
            # Display info
            font = pygame.font.Font(None, 36)
            text = font.render(f"State: {self.state}", True, BLACK)
            screen.blit(text, (10, 10))
            text = font.render(f"Alt: {HEIGHT - self.drone.y:.1f}", True, BLACK)
            screen.blit(text, (10, 50))
            text = font.render(f"X: {self.drone.x:.1f}", True, BLACK)
            screen.blit(text, (10, 90))
            text = font.render(f"Thrust: {self.drone.thrust:.1f}", True, BLACK)
            screen.blit(text, (10, 130))
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    sim = FlightSimulator()
    sim.run()