import pygame
import time
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UAV Simulator-Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Drone parameters
class Drone:
    def __init__(self):
        self.mass = 1.0  # kg
        self.pos_y = HEIGHT - 50  # Starting on ground (pixels)
        self.velocity = 0.0  # m/s
        self.thrust = 0.0  # N
        self.gravity = 9.81  # m/s^2
        self.width = 40
        self.height = 20
        self.target_altitude = 300  # pixels (approx 10m if 1px = 0.033m)
        self.landed = True

    def apply_physics(self, dt):
        # Net force = Thrust - Weight
        net_force = self.thrust - (self.mass * self.gravity)
        # Acceleration = F/m
        acceleration = net_force / self.mass
        # Update velocity
        self.velocity += acceleration * dt
        # Update position (inverted because Pygame y-axis goes down)
        self.pos_y -= self.velocity * dt * 30  # Scale factor for visibility
        
        # Ground collision
        if self.pos_y >= HEIGHT - self.height:
            self.pos_y = HEIGHT - self.height
            self.velocity = 0
            self.landed = True
        else:
            self.landed = False

    def autonomous_takeoff(self):
        # Simple PID-like control for takeoff
        error = self.target_altitude - self.pos_y
        if error > 0 and self.landed:
            # Initial thrust to overcome gravity plus extra for lift
            self.thrust = (self.mass * self.gravity) + min(error * 0.1, 10)
        elif abs(error) < 10:
            # Hover when close to target
            self.thrust = self.mass * self.gravity
        else:
            # Reduce thrust if overshooting
            self.thrust = max((self.mass * self.gravity) - (error * 0.05), 0)

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, 
                        (WIDTH//2 - self.width//2, 
                         int(self.pos_y), 
                         self.width, 
                         self.height))
        # Draw target altitude line
        pygame.draw.line(screen, RED, (0, self.target_altitude), 
                        (WIDTH, self.target_altitude), 2)

# Simulation parameters
drone = Drone()
clock = pygame.time.Clock()
running = True
dt = 0.1  # Time step in seconds

# Main simulation loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and drone.landed:
                drone.landed = False  # Trigger takeoff

    # Clear screen
    screen.fill(WHITE)

    # Update drone
    drone.autonomous_takeoff()
    drone.apply_physics(dt)

    # Draw elements
    drone.draw(screen)
    
    # Draw ground
    pygame.draw.rect(screen, BLACK, (0, HEIGHT-30, WIDTH, 30))
    
    # Display info
    font = pygame.font.Font(None, 36)
    altitude_text = font.render(f"Altitude: {HEIGHT - drone.pos_y:.1f}px", 
                              True, BLACK)
    velocity_text = font.render(f"Velocity: {drone.velocity:.2f}m/s", 
                              True, BLACK)
    thrust_text = font.render(f"Thrust: {drone.thrust:.2f}N", 
                            True, BLACK)
    screen.blit(altitude_text, (10, 10))
    screen.blit(velocity_text, (10, 50))
    screen.blit(thrust_text, (10, 90))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # 60 FPS

pygame.quit()