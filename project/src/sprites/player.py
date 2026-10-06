import pygame
from settings import vector, SPEED, JUMP_STRENGTH, GRAVITY


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # visual settings
        self.image = pygame.Surface((18, 24))
        self.image.fill("dodgerblue")
        self.rect = self.image.get_rect(topleft=pos)

        # for resetting player
        self.originalPos = pos

        # for tracking player trajectory
        self.trajectory = []
        self.record_trajectory = False  # set to True when the player jumps

        # physics
        self.direction = vector(0, 0)
        self.speed = SPEED
        self.gravity = GRAVITY
        self.jump_strength = JUMP_STRENGTH
        self.on_ground = False

        # attack
        self.facing = 1
        self.attacking = False
        self.attack_held = False
        self.attack_cooldown = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        # clearing jump trajectory
        if keys[pygame.K_c]:
            self.trajectory.clear()

        # resetting player position
        if keys[pygame.K_p]:
            self.rect.x = self.originalPos[0]
            self.rect.y = self.originalPos[1]

        # moving right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 1

        # moving left
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = -1

        # not moving
        else:
            self.direction.x = 0

        # jumping
        if (
            keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        ) and self.on_ground:
            self.direction.y = self.jump_strength
            # self.rect.y += self.direction.y
            self.on_ground = False
            # trajectory tracking
            # self.trajectory.clear()  # erasing previous jump trajectory
            self.record_trajectory = True

        # attacking
        if keys[pygame.K_f]:
            if not self.attack_held and self.attack_cooldown == 0:
                self.attacking = True
                self.attack_cooldown = 14
            self.attack_held = True

        else:
            self.attack_held = False

    # def jump(self):
    #  if self.on_ground:
    #   print("JUMP")
    #   self.direction.y = self.jump_strength
    #   self.on_ground = False

    def move_x(self):
        self.rect.x += self.direction.x * self.speed
        # print(f"Player is at ({self.rect.x}, {self.rect.y})")

    def apply_gravity(self):
        self.direction.y += self.gravity

        if self.direction.y < -12:
            self.direction.y = -12

        self.rect.y += self.direction.y

    def start_attack(self):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_cooldown = 14

    def update_attack(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        else:
            self.attacking = False

    def create_attack_hitbox(self):
        offset_x = 18 if self.facing == 1 else -34
        hitbox_pos = (self.rect.centerx + offset_x, self.rect.centery - 12)
        hitbox_size = (18, 18)
        return hitbox_pos, hitbox_size

    def draw_trajectory(self, screen):
        for pos in self.trajectory:
            pygame.draw.circle(screen, (255, 255, 0), pos, 1)
