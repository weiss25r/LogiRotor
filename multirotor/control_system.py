from multirotor import *
from path_planner import *

class ControlSystem:
    def __init__(self, robot, coordinates_path="", edges_path=""):
        self.robot = robot
        self.path_planner = PathPlanner()
        self.move_list = []
        self.__create_graph__(coordinates_path, edges_path)
        
    def __create_graph__(self, coordinates_path, edges_path):
        coords = pd.read_csv(coordinates_path, sep=';')
        edges = pd.read_csv(edges_path, sep=' ')
        
        coords.apply(
            func = lambda node: self.path_planner.add_node(NavigationNode(x=node['Y'], y=node['X'], z=node['Z'], node_type=node['TYPE'])), 
            axis=1
        )
        
        edges.apply(
            func = lambda edge: self.path_planner.add_edge(edge['FROM'], edge['TO']),
            axis=1
        )
        
    
    def start(self, package_order, package_map):
        
        last_position = 0
        move_list = []
        
        for package in package_order:
            move_list = move_list + self.path_planner.create_path(self.robot, last_position, package)
            move_list = move_list + self.path_planner.create_path(self.robot, package, package_map[package])
            last_position = package_map[package]
        
        move_list = move_list + self.path_planner.create_path(self.robot, last_position, 0)
        move_list.append(ZMovement(self.robot, 0.060))
        self.move_list = move_list
    