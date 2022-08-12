import pygame,sys
from game_world import *

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,color):
        super().__init__()
        self.image=pygame.Surface((150,100))
        self.image.fill(color)
        self.rect=self.image.get_rect(center=pos)


class icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect=self.image.get_rect(center=pos)

class Overworld:
    def __init__(self,surface,max_level,start_level,create_level,unlock_level):
        self.display_surface=surface

        #unlock levels
        self.unlock_levels=unlock_level

        self.node_sprites=pygame.sprite.Group()

        self.max_level=max_level
        self.current_level=start_level

        self.create_node_sprites()
        self.icon_sprite=pygame.sprite.GroupSingle()
        
        icon_sprite=icon((100,100))
        
        self.icon_sprite.add(icon_sprite)

        # self.game_status='Menu'

        self.create_level=create_level

    def create_node_sprites(self):
        for index,level in enumerate(levels.values()):
            if index <= self.max_level:
                sprite=Node(level['node_pos'],'red')
            else: 
                sprite=Node(level['node_pos'],'grey')
            self.node_sprites.add(sprite)

    def get_input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.current_level > 0:
            self.current_level-=1
        elif keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.current_level+=1
        elif keys[pygame.K_RETURN] and self.current_level <=self.max_level:
            # print(self.current_level)
            self.create_level(self.current_level,self.unlock_levels)

            # self.game_status='play'
        self.change_level()
        pygame.time.delay(50)


    def change_level(self):
        self.icon_sprite.sprite.rect.center=self.node_sprites.sprites()[self.current_level].rect.center


    def run(self):
            self.get_input()
            self.node_sprites.draw(self.display_surface)
            self.icon_sprite.draw(self.display_surface)


        
