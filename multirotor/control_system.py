from multirotor import *
from path_planner import *

class ControlSystem:
    def __init__(self, x_origin=0, y_origin=0, z_origin=0):
        self.robot = Multirotor(x_origin = x_origin, y_origin=y_origin, z_origin=z_origin)
        self.path_planner = PathPlanner()
        self.move_list = []
    
    def create_graph(self, coordinates_path, edges_path):
        coords = pd.read_csv(coordinates_path, sep=';')
        edges = pd.read_csv(edges_path, sep=' ')
        
        coords.apply(
            func = lambda node: self.path_planner.add_node(NavigationNode(node['X'], node['Y'], node['Z'], node['TYPE'])), 
            axis=1
        )
        
        edges.apply(
            func = lambda edge: self.path_planner.add_edge(edge['FROM'], edge['TO']),
            axis=1
        )
        pass
    
    def start(self, start, end):
        self.move_list = self.path_planner.create_path(self.robot, start, end)
    