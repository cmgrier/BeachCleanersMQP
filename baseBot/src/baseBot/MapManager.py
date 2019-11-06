#!/usr/bin/env python
from baseBot.MapMaker import MapMaker
import math

# This class holds the current map and passes it between the other managers
from data.Zone import Zone
from support.Constants import *


class MapManager:

    def __init__(self):
        self.zones = list()
        self.mapMaker = MapMaker()
        self.landing_strip = []  # [top_left, top_right, bottom_right, bottom_left]
        self.map = self.mapMaker.get_map()  # is a map of difficulty of terrain

    # sets the current map from mapMaker and creates zones
    def update_map(self):
        self.map = self.mapMaker.get_map()
        self.divide_map()

    def divide_map(self):
        self.__create_zones()
        self.__create_landing_strip()

    # divides the map into different zones
    def __create_zones(self):
        self.zones = list()
        map_width = int(math.sqrt(len(self.map)))
        number_of_zones = int(map_width / ZONE_WIDTH)

        for i in range(0, number_of_zones - 1):
            top_left = i * ZONE_WIDTH
            top_right = top_left + ZONE_WIDTH
            bottom_left = top_left + map_width * (map_width - LANDING_STRIP_WIDTH)
            bottom_right = bottom_left + ZONE_WIDTH
            zone_corners = [top_left, top_right, bottom_right, bottom_left]
            new_zone = Zone(zone_corners, i)
            self.zones.append(new_zone)

        top_left = self.zones[len(self.zones) - 1].corners[1]
        top_right = map_width - 1
        bottom_left = self.zones[len(self.zones) - 1].corners[3]
        bottom_right = top_right + map_width * (map_width - LANDING_STRIP_WIDTH)
        new_zone = Zone([top_left, top_right, bottom_right, bottom_left], len(self.zones))
        self.zones.append(new_zone)

    def __create_landing_strip(self):
        map_width = int(math.sqrt(len(self.map)))
        top_left = map_width * (map_width - LANDING_STRIP_WIDTH)
        top_right = top_left + map_width
        bottom_right = len(self.map) - 1
        bottom_left = bottom_right - map_width
        self.landing_strip = [top_left, top_right, bottom_right, bottom_left]

    def percent_of_indexes_safe(self, index_list):
        indexes_too_difficult = 0.0
        for index in index_list:
            if self.map[index] > TERRAIN_TOO_DIFFICULT or self.map[index] == -1:
                indexes_too_difficult += 1.0

        return indexes_too_difficult / float(len(index_list))

    def point_to_index(self, position):
        return 1
