import csv
import os
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        for row in csv.reader(level_map, delimiter=','):
            terrain_map.append(list(row))
    return terrain_map


def import_folder(path):
    surf_list = []
    for _, _, img_files in os.walk(path):
        for img in img_files:
            surf_list.append(pygame.image.load(os.path.join(path, img)).convert_alpha())
    return surf_list