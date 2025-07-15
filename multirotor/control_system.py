from multirotor import *
from path_planner import *

class ControlSystem:
    def __init__(self, x_origin=0, y_origin=0, z_origin=0, start_package = 1):
        self.robot = Multirotor(x_origin = x_origin, y_origin=y_origin, z_origin=z_origin)
        self.path_planner = PathPlanner()
        self.move_list = []
        self.start_package = start_package
    
    def create_graph(self, coordinates_path, edges_path):
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
        
        self.move_list = self.path_planner.create_path(self.robot, 0, self.start_package)
    
    def start(self, start, end):
        start_to_end = self.path_planner.create_path(self.robot, start, end)
        
        self.move_list = self.move_list + start_to_end
    