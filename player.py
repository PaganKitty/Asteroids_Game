import pygame
import constants
from circleshape import CircleShape
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, constants.PLAYER_RADIUS)
        self.rotation = 0
        self.CD_TIMER = 0.0
        
    def rotate(self, dt, direction: int):
        self.rotation += direction * constants.PLAYER_TURN_SPD * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(dt)
        elif keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
           self.rotate(dt, 1)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.CD_TIMER > 0:
            self.CD_TIMER -= dt
            if self.CD_TIMER < 0:
                self.CD_TIMER = 0
            
           
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * constants.PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
        
    def shoot(self):
        if self.CD_TIMER > 0:
            return False
        else:
            self.CD_TIMER = constants.PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * constants.PLAYER_SHOOT_SPEED
        
            