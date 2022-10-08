import pygame

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_image_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_image_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_image_1, fly_image_2]
            y_pos = 210
        elif type == 'snail':
            snail_image_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_image_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_image_1, snail_image_2]
            y_pos = 300
        else:
            raise Exception('Obstacle type not supported.')

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()