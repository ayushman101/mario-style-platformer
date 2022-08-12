import pygame

class UI:
    def __init__(self,surface):
        self.display_surface=surface

        #health_bar
        self.health_bar_surface=pygame.image.load('graphics/gui/4 - gui/graphics/ui/health_bar.png')
        self.health_bar_rect=self.health_bar_surface.get_rect(topleft=(30,10))

        self.max_health_width=152
        self.health_height=4

        self.health_bar_topleft=((64,39))

        #coins
        self.coin_image=pygame.image.load('graphics/gui/4 - gui/graphics/ui/coin.png')
        self.coin_rect=self.coin_image.get_rect(topleft=(30,80))    

        self.text_font=pygame.font.Font('graphics/gui/4 - gui/graphics/ui/ARCADEPI.TTF',30)
        
    def show_health(self,current,full):
        self.display_surface.blit(self.health_bar_surface,self.health_bar_rect)
        health_ratio=current/full
        current_health_width=self.max_health_width*health_ratio

        current_health_rect=pygame.Rect(self.health_bar_topleft,(current_health_width,self.health_height))
        pygame.draw.rect(self.display_surface,'red',current_health_rect)


    def show_coins(self,amount):
        self.display_surface.blit(self.coin_image,self.coin_rect)
        coin_amount_surface=self.text_font.render(str(amount),False,'Black')
        self.display_surface.blit(coin_amount_surface,(self.coin_rect.right+4,self.coin_rect.top))