from random import randint
from secrets import choice
import pygame
from game_mode import import_folder
from settings import tilesize,screen_width,verticle_tile_number

class Tile(pygame.sprite.Sprite):
    def __init__(self, size,x,y):
        super().__init__()
        self.image=pygame.Surface((size,size),flags=pygame.SRCALPHA)
        self.rect=self.image.get_rect(topleft=(x,y))
        

class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image=surface
    def update(self,world_shift):
        self.rect.x+=world_shift

class AnimatedTile(Tile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frame_index=0
        self.frame_list=import_folder(path)
        self.image=self.frame_list[int(self.frame_index)]
    
    def animate(self):
        self.frame_index+=0.1
        if self.frame_index >= len(self.frame_list):
            self.frame_index=0
        self.image=self.frame_list[int(self.frame_index)]
    
    def update(self,world_shift):
        self.rect.x+=world_shift
        self.animate()


class level_end(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('graphics\level_end\level_end.png')
        self.rect=self.image.get_rect(topleft=(x,0))
    def update(self,world_shift):
        self.rect.x+=world_shift

class Palms(AnimatedTile):
    def __init__(self,size,x,y,path,type):
        super().__init__(size,x,y,path)
        # offset_y=y
        if type=='large':
            offset_y=y-tilesize
        elif type=='small':
            offset_y=y-(tilesize/2)
        elif type=='bg_palms':
            offset_y=y-(tilesize/1.25)
        self.rect=self.image.get_rect(topleft=(x,offset_y))

class Water(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)        
        self.image=pygame.Surface((192,size),flags=pygame.SRCALPHA)


class sky:
    def __init__(self,horizon):
        
        self.horizon=horizon
        self.top=pygame.image.load('graphics\decoration\sky\sky_top.png').convert()
        self.bottom=pygame.image.load('graphics\decoration\sky\sky_bottom.png').convert()
        self.middle=pygame.image.load('graphics\decoration\sky\sky_middle.png').convert()


        #stretching images
        self.top=pygame.transform.scale(self.top,(screen_width,tilesize))
        self.bottom=pygame.transform.scale(self.bottom,(screen_width,tilesize))
        self.middle=pygame.transform.scale(self.middle,(screen_width,tilesize))

    def draw(self,surface):

        for row in range(verticle_tile_number):
            y=row*tilesize
            if row < self.horizon:
                surface.blit(self.top,(0,y))
            elif row==self.horizon:
                surface.blit(self.middle,(0,y))
            else:
                surface.blit(self.bottom,(0,y))
            
class clouds:
    def __init__(self,horizon,level_width,cloud_number):
        cloud_surface_list=import_folder('graphics\decoration\clouds')        
        min_x=-screen_width
        max_x=screen_width + level_width
        min_y=0
        max_y=horizon
        self.cloud_sprites=pygame.sprite.Group()

        for cloud in range(cloud_number):
            x=randint(min_x,max_x)
            y=randint(min_y,max_y)
            cloud_image=choice(cloud_surface_list)
            sprite=StaticTile(0,x,y,cloud_image)
            self.cloud_sprites.add(sprite)


    def draw(self,surface):
        self.cloud_sprites.draw(surface)
