from csv import reader
from os import walk
from settings import tilesize
import pygame



def import_folder(path):
    
    frame_list=[]

    for _,__,image_list in walk(path):
        for image_path in image_list:
            full_path=path + '/' + image_path
            frame=pygame.image.load(full_path).convert_alpha()
            frame_list.append(frame)
    
    return frame_list

def import_csv_layout(path):
    terrain_layout=[]
    
    with open(path) as map:
        level=reader(map, delimiter=',')
        for row in level:
            terrain_layout.append(list(row))
        return terrain_layout


def import_cut_graphics(path):

    cut_list=[]

    path_image=pygame.image.load(path)

    x_tile_num=int(path_image.get_size()[0]/tilesize)
    y_tile_num=int(path_image.get_size()[1]/tilesize)

    for row in range(y_tile_num):
        for col in range(x_tile_num):
            l=col*tilesize
            t=row*tilesize

            new_image=pygame.Surface((tilesize,tilesize),flags=pygame.SRCALPHA)
            new_image.blit(path_image,(0,0),pygame.Rect(l,t,tilesize,tilesize))

            cut_list.append(new_image)

    return cut_list