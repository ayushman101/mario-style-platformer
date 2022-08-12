
import pygame, sys
from settings import *
from level import Level
from support import level_0
from ui import UI
from overworld import Overworld

class Game:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((screen_width,screen_height))
        self.clock=pygame.time.Clock()
        pygame.display.set_caption('Runner')
        self.max_level=2
        self.max_unlocked_level=1
        self.status='overworld'
        self.overworld=Overworld(self.screen,self.max_unlocked_level,0,self.create_level,self.incr_max_unlocked_level)



        #Gui setup 
        self.ui=UI(self.screen)
        self.coin_amount=0
        self.current_health=100

    def create_level(self,current_level,unlock_level):
        self.level=Level(current_level,self.screen,self.change_coin_amount,self.change_health,self.change_status,unlock_level) 
        self.status='play'

    
    
    def incr_max_unlocked_level(self,current_level):
        if self.max_unlocked_level<self.max_level  and self.max_unlocked_level==current_level:
            
            self.max_unlocked_level+=1
            
            self.overworld.max_level=self.max_unlocked_level

            self.overworld.node_sprites.empty()

            self.overworld.create_node_sprites()
            
            print(self.max_unlocked_level)





    def change_coin_amount(self,amount):
        self.coin_amount+=amount
        
    def change_status(self):
        if self.status=='overworld':
            self.status='play'
        else:
            self.status='overworld'

    def change_health(self,amount):
        self.current_health+=amount
    
    def run(self):

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            if self.current_health < 10:
                pygame.quit()
                sys.exit()
            self.screen.fill('grey')

            if self.status=='overworld':
                self.overworld.run()
            elif self.status=='play':
                self.level.run()
                self.ui.show_health(self.current_health,100)
                self.ui.show_coins(self.coin_amount)

            pygame.display.update()
           
            self.clock.tick(fps)


if __name__=='__main__':
    game=Game()
    game.run()