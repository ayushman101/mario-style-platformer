from numpy import tile
import pygame
from game_mode import import_csv_layout, import_cut_graphics
from settings import tilesize
from tile import *
from enemy import Enemy
from player import Player
from support import *
# from game_world import *


class Level:
    def __init__(self,current_level,surface,coin_amount_change,change_health,change_status,incr_max_unlock_level) :

        self.display_surface=surface
        self.world_shift=-8
        
        self.current_level=current_level

        #max unlocked levels
        self.incr_unlock_level=incr_max_unlock_level

        # print(level_data['terrain'])
        self.change_status=change_status
        
        level_data=levels[self.current_level]


        #water setup
        water_layout=import_csv_layout(level_data['water'])
        self.water_sprites=self.create_sprite_groups(water_layout,'water')

        #terrain setup
        terrain_layout=import_csv_layout(level_data['terrain'])
        self.terrain_sprite=self.create_sprite_groups(terrain_layout,'terrain')

        #crate setup
        crate_layout=import_csv_layout(level_data['crate'])
        self.crate_sprite=self.create_sprite_groups(crate_layout,'crate')

        #  coin setup
        coin_layout=import_csv_layout(level_data['coins'])
        self.coins_sprite=self.create_sprite_groups(coin_layout,'coins')

        #fg palms
        fg_palms_layout=import_csv_layout(level_data['fg_palms'])
        self.fg_palms_sprite=self.create_sprite_groups(fg_palms_layout,'fg_palms')

        #bg_palms
        bg_palms_layout=import_csv_layout(level_data['bg_palms'])
        self.bg_palms_sprite=self.create_sprite_groups(bg_palms_layout,'bg_palms')
        
        #enemy sprites
        enemy_layout=import_csv_layout(level_data['enemy_layer'])
        self.enemy_sprite=self.create_sprite_groups(enemy_layout,'enemy')

        #constraints sprites
        constraints_layout=import_csv_layout(level_data['constraints'])
        self.constraints_sprites=self.create_sprite_groups(constraints_layout,'constraints')

        #sky
        self.Sky=sky(8)

        #level_end_constraint setup
        level_end_constraint_layout=import_csv_layout(level_data['end'])
        self.level_end_sprite=self.create_sprite_groups(level_end_constraint_layout,'level_end')

        #player setup
        player_sprite=Player((30,40),self.change_status)
        self.player=pygame.sprite.GroupSingle()
        self.player.add(player_sprite)


        level_width=len(terrain_layout[0]) * tilesize
        self.cloud=clouds(7,level_width,20)

        #coin_change_function
        self.coin_change=coin_amount_change


        #health change function
        self.change_health=change_health
        self.invinciblity=False
        self.invinciblity_duration=400
        self.hurt_time=0

    def create_sprite_groups(self,layout,type):

        sprite_group=pygame.sprite.Group()
    
        for row_index,row in enumerate(layout):
            for col_index,val in enumerate(row):
                if val !='-1':
                    x=col_index*tilesize
                    y=row_index*tilesize

                    if type=='terrain':

                        terrain_list=import_cut_graphics('graphics/terrain/terrain_tiles.png')
                        sprite=StaticTile(tilesize,x,y,terrain_list[int(val)])
                    
                    if type=='coins':
                        # coin_list=import_cut_graphics('graphics/coins/coin_tiles.png')
                        if val=='0':
                            sprite=AnimatedTile(tilesize,x,y,'graphics/coins/gold')
                        elif val=='1':
                            sprite=AnimatedTile(tilesize,x,y,'graphics/coins/silver')
                            

                    if type=='crate':
                        crate_image=pygame.image.load('graphics/terrain/crate.png')
                        crate_surface=pygame.Surface((tilesize,tilesize),flags=pygame.SRCALPHA)
                        crate_surface.blit(crate_image,(0,22))
                        sprite=StaticTile(tilesize,x,y,crate_surface)
                    
                    if type=='fg_palms':
                        if val=='0':
                            sprite=Palms(tilesize,x,y,'graphics/terrain/palm_large','large')
                        elif val=='2':
                            sprite=Palms(tilesize,x,y,'graphics/terrain/palm_small','small')

                    if type=='bg_palms':
                        sprite=Palms(tilesize,x,y,'graphics/terrain/palm_bg','bg_palms')

                    if type=='enemy':
                        sprite=Enemy(tilesize,x,y)

                    if type=='constraints':
                        constr_image=pygame.image.load('graphics\enemy\constraint.png')
                        sprite=StaticTile(tilesize,x,y,constr_image)

                    if type=='water':
                        sprite=AnimatedTile(192,x,y,'graphics\decoration\water')

                    if type=='level_end':
                        # level_end_image=pygame.image.load('graphics\enemy\constraint.png')
                        # sprite=StaticTile(tilesize,x,y,level_end_image)
                        sprite=level_end(x,y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision(self):
        for enemy in self.enemy_sprite.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraints_sprites,False):
                enemy.enemy_speed_reverse()

    def horizontal_collision(self):
        player=self.player.sprite
        player.rect.x+=player.direction.x * player.speed
        for sprite in self.terrain_sprite.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right=sprite.rect.left
                elif player.direction.x < 0:
                    player.rect.left=sprite.rect.right
    
    def vertical_collision(self):
        player=self.player.sprite
        player.direction.y+=1
        player.rect.y+=player.direction.y
        for sprite in self.terrain_sprite.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y=0
                    player.on_ground=True

                elif player.direction.y < 0:
                    player.rect.top=sprite.rect.bottom 
                    player.direction.y=0

        if player.on_ground and player.direction.y < 0  or player.direction.y > 1:
            player.on_ground=False 

    def coin_collision(self):
        collided_sprite=pygame.sprite.spritecollide(self.player.sprite,self.coins_sprite,True)
        if collided_sprite:
            for sprite in collided_sprite:
                self.coin_change(2)

    def enemy_player_collision(self):
        enemy_sprite=pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprite,False)
        if enemy_sprite:
            for enemy in enemy_sprite:
                if enemy.rect.top < self.player.sprite.rect.bottom < enemy.rect.centery and self.player.sprite.direction.y >=0:
                    enemy.kill()
                    self.player.sprite.direction.y=-13
                else:
                    if not self.invinciblity:
                        self.change_health(-10)
                        self.invinciblity=True
                        self.hurt_time=pygame.time.get_ticks()


    def change_invinciblity(self):

        invincibility_time=pygame.time.get_ticks()
        if invincibility_time - self.hurt_time > self.invinciblity_duration:
            self.invinciblity=False

    def player_level_end(self):
        for level_end in self.level_end_sprite.sprites():
            if pygame.sprite.spritecollide(level_end,self.player,False):
                self.incr_unlock_level(self.current_level)
                self.change_status()

    def scroll_x(self):
        player=self.player.sprite
        player_x=player.rect.centerx
        direction_x=player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift=8
            player.speed=0
        
        elif player_x > screen_width - (screen_width/4) and direction_x>0:
            self.world_shift=-8
            player.speed=0
        else:
            self.world_shift=0
            player.speed=8 

    def run(self):
        
        self.scroll_x()


        #checking coin collisions
        self.coin_collision()
        self.enemy_player_collision()
        self.change_invinciblity()

        #sky draw 
        self.Sky.draw(self.display_surface)

        self.cloud.draw(self.display_surface)

        #bg_palms draw
        self.bg_palms_sprite.update(self.world_shift)
        self.bg_palms_sprite.draw(self.display_surface)

        #terrain draw
        self.terrain_sprite.update(self.world_shift)
        self.terrain_sprite.draw(self.display_surface)
        
        #player draw 
        self.player.update()
        self.horizontal_collision()
        self.vertical_collision()
        self.player.draw(self.display_surface)

        #enemy draw
        self.enemy_sprite.update(self.world_shift)
        self.enemy_sprite.draw(self.display_surface)
        self.enemy_collision()
        #crate draw
        self.crate_sprite.update(self.world_shift)
        self.crate_sprite.draw(self.display_surface)

        #constraints
        self.constraints_sprites.update(self.world_shift)
        # self.constraints_sprites.draw(self.display_surface)

        # coins draw
        self.coins_sprite.update(self.world_shift)
        self.coins_sprite.draw(self.display_surface)

        #foreground palms
        self.fg_palms_sprite.update(self.world_shift)
        self.fg_palms_sprite.draw(self.display_surface)

        #water draw
        self.water_sprites.update(self.world_shift)
        self.water_sprites.draw(self.display_surface)

        #level_end
        # self.level_end_sprite.update(self.world_shift)
        self.level_end_sprite.draw(self.display_surface)
        self.level_end_sprite.update(self.world_shift)
        self.player_level_end()

