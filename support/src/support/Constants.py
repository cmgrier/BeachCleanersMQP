#!/usr/bin/env python

TRASH_BIN_THRESHOLD = 12    # TODO: Get the actual value for this constant

STORED_MAP_SIZE = 10
SAFE_DISTANCE_BETWEEN_BOTS = 100
AVOID_DISTANCE = 30

ZONE_WIDTH = 20
LANDING_STRIP_WIDTH = 20

# ask Chris. Essentially we prioritize to avoiding robots by backing up first rather than trying to move forward
AVOID_DIRECTION_PRIORITY_LIST = [3, 4, 2, 5, 1, 6, 0, 7]

#AStar
STANDARD_MOVE_COST = 1
DIFFICULT_TERRAIN_FACTOR = 1
TURNING_FACTOR = 1

TERRAIN_TOO_DIFFICULT = 30
ZONE_TOO_DIFFICULT_PERCENT = .1

#Motors
LEFT_WHEEL_PIN= 17
RIGHT_WHEEL_PIN = 18

