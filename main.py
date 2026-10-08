import sys
from logger import log_state, log_event
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    lives = 3
    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots,updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    pygame.font.init()
    font = pygame.font.SysFont(None,36)
    score = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                lives -= 1
                log_event("player_hit")

                if lives <= 0:
                    print("Game over!")
                    print(f"Final Score: {score}")
                    sys.exit()
                else:
                    player.position = pygame.Vector2(SCREEN_WIDTH /2, SCREEN_HEIGHT /2)
                    player.velocity = pygame.Vector2(0,0)
                    asteroid.kill()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    score += 100

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        score_text = font.render(f"Score: {score} | Lives: {lives}", True, "white")
        screen.blit(score_text, (10,10))

        pygame.display.flip()

        dt = clock.tick(60) / 1000









if __name__ == "__main__":
    main()
