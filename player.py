import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        image_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.images = [image_1, image_2]
        self.index = 0
        self.jump_image = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.images[self.index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.images): self.player_index = 0
            self.image = self.images[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()