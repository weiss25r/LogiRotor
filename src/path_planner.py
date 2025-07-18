import math
import pandas as pd
from src.multirotor import *
from dijkstar import *

class NavigationNode():
    def __init__(self, x, y ,z,  node_type):
        self.x = x
        self.y = y
        self.z = z
        self.type = node_type
    def get_coordinates(self):
        return (self.x, self.y, self.z)
    
    def distance(self, node2):
        dist_x = (self.x - node2.x)**2
        dist_y = (self.y - node2.y)**2
        
        if pd.isna(node2.z) or pd.isna(self.z):
            dist_z = 0
        else:
            dist_z = (self.z - node2.z)**2
        
        if self.type == 'END' or node2.type == 'END':
            return 10*math.sqrt(dist_x + dist_y + dist_z)
        else:
            return math.sqrt(dist_x + dist_y + dist_z)
    
    #tostring
    def __str__(self):
        return f"({self.x}, {self.y})"

class PathPlanner():
    
    def __init__(self, coordinates=[], edges=[]):
        self.nodes = []
        self.graph = Graph(undirected=True)
        
        for coordinate in coordinates:
            self.nodes.append(NavigationNode(coordinate[1], coordinate[0], coordinate[2])) #si scambiano x e z a causa del ref. frame di godot
            
        for edge in edges:
            node_one = self.nodes[edge[0]]
            node_two = self.nodes[edge[1]]
            self.graph.add_edge(node_one, node_two, node_one.distance(node_two))
            
    def add_node(self, node):
        self.nodes.append(node)
        
    def add_edge(self, index_one, index_two):
        node_one = self.nodes[index_one]
        node_two = self.nodes[index_two]
        self.graph.add_edge(node_one, node_two, node_one.distance(node_two))

    def create_path(self, robot, start, end):
        path = find_path(self.graph, self.nodes[start], self.nodes[end])
        coordinates = [node.get_coordinates() for node in path.nodes]
        move_list = []
        current_z = 0
        current_x = robot.y_target
        current_y = robot.x_target
        
        for node in path.nodes:
            coords = node.get_coordinates()
            
            if (node.type == 'MOV') and node.z != current_z:
                move_list.append(ZMovement(robot, node.z))


            if node.x != current_x or node.y != current_y:
                move_list.append(XYMovement(robot, coords[0], coords[1]))
            
            if node.type == 'START':
                move_list.append(ZMovement(robot, coords[2]))
                move_list.append(AttachMovement(1))
                move_list.append(AttachMovement(0))
            elif node.type == 'END':
                move_list.append(ZMovement(robot, coords[2]))
                move_list.append(AttachMovement(2))
                move_list.append(AttachMovement(0))
                
            current_z = node.z
            current_x = node.x
            current_y = node.y
            
        self.path = path
        return move_list