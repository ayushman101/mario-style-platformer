import pygame
from tile import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,'graphics/enemy/run')
        self.rect.y+= size - self.image.get_size()[1]
        self.speed=3

    def move(self):
        self.rect.x+=self.speed

    def enemy_image_flip(self):
        if self.speed > 0:
            self.image=pygame.transform.flip(self.image,True,False)

    def enemy_speed_reverse(self):
        self.speed*=-1

    def update(self,world_shift):
        self.rect.x+=world_shift
        self.move()
        self.animate()
        self.enemy_image_flip()