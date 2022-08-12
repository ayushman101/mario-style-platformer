import pygame
from game_mode import import_folder
from settings import tilesize
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,change_status):
        super().__init__()

        #player status
        self.state='idle'
        self.on_ground=True

        #level status
        self.level_status=change_status

        self.import_character_assets()
        self.frame_index=0
        self.animation_speed=0.15
        self.image=pygame.Surface((tilesize,tilesize))
        self.image=self.animation_list[self.state][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)
        self.speed=8
        
        #direction vector
        self.direction=pygame.math.Vector2(0,0)



    def import_character_assets(self):
        character_path='graphics/character/'
        self.animation_list={ 'idle':[],
                               'fall':[],
                               'jump':[],
                               'run':[] 
                                }

        for animations in self.animation_list.keys():
            full_path=character_path + animations
            self.animation_list[animations]=import_folder(full_path)
    
    def animate(self):
        animation=self.animation_list[self.state]
        self.frame_index+=self.animation_speed
        if self.frame_index >=  len(animation):
            self.frame_index=0
        self.image=animation[int(self.frame_index)] 

        if self.direction.x < 0: 
            self.image=pygame.transform.flip(self.image,True,False)

    def get_input(self):
        keys=pygame.key.get_pressed()
        
        
        if keys[pygame.K_RIGHT]:
            self.direction.x=1
            self.state='run'
        elif keys[pygame.K_LEFT]:
            self.direction.x=-1
            self.state='run'
        else:
            self.state='idle'
            self.direction.x=0

        if keys[pygame.K_UP] and self.on_ground :
            self.direction.y=-13
            self.state='jump'
        
        if keys[pygame.K_ESCAPE]:
            self.level_status()

    def update(self):
        self.get_input()
        if self.direction.y>0 :
            self.state='fall'
        self.animate()
        self.rect.y+=self.direction.y

