from math import hypot


class AStar:

    # given map is an array of weights
    def __init__(self, map):
        self.map = map
        self.frontier = list()
        self.investigated = list()

    # start and end are indexes on the map
    # map indexes work as follows:
    #    x ->
    # y  0  1  2  3
    # |  4  5  6  7
    # v  8  9  10 11
    #    12 13 14 15
    #       \  /
    #       robot

    # method to be called outside of AStar class to retrieve path
    def find_path(self, start, end):
        self.frontier = list()
        node = self.create_node(start, end, 0)
        self.frontier.append(node)
        while not self.frontier:
            best_node = self.get_best_node()
            if best_node.index == end:
                return self.create_path(start, best_node)
            self.investigate_point(best_node, end)
            self.investigated.append(best_node)
        return start

    # checks local points above, below, and to either side of given node
    # and adds them to the frontier
    def investigate_point(self, node, end):
        left_node = self.create_node(node.index - 1, end, node.movement_cost + 1)
        right_node = self.create_node(node.index + 1, end, node.movement_cost + 1)
        top_node = self.create_node(node.index - self.map.width, end, node.movement_cost + 1)
        bottom_node = self.create_node(node.index + self.map.width, end, node.movement_cost + 1)
        new_nodes = [left_node, right_node, top_node, bottom_node]
        for new_node in new_nodes:
            if self.is_node_in_frontier(new_node):
                self.update_node_in_frontier(new_node)
            elif self.is_node_investigated(new_node):
                self.update_node_in_investigated(new_node)
            else:
                self.frontier.append(new_node)

    def get_best_node(self):
        best_node = self.frontier[0]
        for node in self.frontier:
            if node.cost < best_node:
                best_node = node
        return best_node

    def is_node_in_frontier(self, node):
        for frontier_node in self.frontier:
            if frontier_node.index == node.index:
                return True
        return False

    def is_node_investigated(self, node):
        for investigated_node in self.investigated:
            if investigated_node.index == node.index:
                return True
        return False

    def update_node_in_investigated(self, new_node):
        for node in self.investigated:
            self.update_node_cost_in_investigated(new_node, node)

    # helper for self.update_node_in_frontier
    def update_node_cost_in_investigated(self, new_node, old_node):
        if old_node.index == new_node.index and new_node.cost < old_node.cost:
            self.investigated.remove(old_node)
            self.investigated.append(new_node)

    # helper for self.investigate_point
    def update_node_in_frontier(self, new_node):
        for node in self.frontier:
            self.update_node_cost_in_frontier(new_node, node)

    # helper for self.update_node_in_frontier
    def update_node_cost_in_frontier(self, new_node, old_node):
        if old_node.index == new_node.index and new_node.cost < old_node.cost:
            self.frontier.remove(old_node)
            self.frontier.append(new_node)

    # this creates path from the given start and end node
    def create_path(self, start_index, end):
        path = list()
        path.append(end.index)
        current_node = end.previous_point
        while current_node.index != start_index:
            path.append(current_node.index)
            current_node = current_node.previous_point
        return path

    def create_node(self, position, end, movement_cost):
        node = Node
        node.heuristic = self.get_heuristic(position, end)
        node.movement_cost = movement_cost
        node.index = position
        node.cost = node.heuristic + node.movement_cost
        return node

    def get_heuristic(self, start, end):
        start_point = self.convert_index_to_point(start)
        end_point = self.convert_index_to_point(end)
        return hypot(start_point.x - end_point.x, start_point.y - end_point.y)

    def convert_index_to_point(self, index):
        x = index % self.map.width
        y = index / self.map.width
        point = Point
        point.x = x
        point.y = y
        return point


class Node:
    cost = 0
    heuristic = 0
    movement_cost = 0
    index = 0
    previous_point = 0


# delete later once ROS is included in workspace
class Point:
    x = 0
    y = 0
