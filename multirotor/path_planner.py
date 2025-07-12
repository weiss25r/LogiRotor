from dijkstar import *
from multirotor import *
import math

class NavigationNode():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_coordinates(self):
        return (self.x, self.y)
    
    def distance(self, node2):
        return math.sqrt((self.x - node2.x)**2 + (self.y - node2.y)**2)
    
    #tostring
    def __str__(self):
        return f"({self.x}, {self.y})"

class PathPlanner():
    
    def __init__(self, coordinates, edges):
        self.nodes = []
        self.graph = Graph()
        
        for coordinate in coordinates:
            self.nodes.append(NavigationNode(coordinate[1], coordinate[0])) #si scambiano x e z a causa del ref. frame di godot
            
        for edge in edges:
            node_one = self.nodes[edge[0]]
            node_two = self.nodes[edge[1]]
            self.graph.add_edge(node_one, node_two, node_one.distance(node_two))
            
    def create_path(self, robot, start, end):
        path = find_path(self.graph, self.nodes[start], self.nodes[end])
        coordinates = [node.get_coordinates() for node in path.nodes]
        
        movements = [XYMovement(robot, coord[0], coord[1]) for coord in coordinates]
        return movements
    
    