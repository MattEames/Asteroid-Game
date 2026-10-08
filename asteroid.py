import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def split(self):
        for _ in range(5):
            particle_vel = pygame.Vector2(random.uniform(-100,100), random.uniform(-100,100))
            Particle(self.position.x, self.position.y,particle_vel)
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        random_angle = random.uniform(20,50)

        vel1 = self.velocity.rotate(random_angle)
        vel2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = vel1 * 1.2
        asteroid2.velocity = vel2 * 1.2

    def draw(self,screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self,dt):
        self.position += (self.velocity * dt)
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT

class Particle(CircleShape):
    def __init__(self, x, y, velocity):
        super().__init__(x, y, radius = 2)
        self.velocity = velocity
        self.lifespan = 0.5

    def draw(self,screen):
        pygame.draw.circle(screen, "red", self.position, self.radius)

    def update(self,dt):
        self.position += self.velocity * dt
        self.lifespan -= dt
        if self.lifespan <= 0:
            self.kill()
