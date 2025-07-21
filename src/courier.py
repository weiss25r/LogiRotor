import json
from src.control_system import *

class Courier():
    
    """
    Classe che rappresenta il drone corriere su Godot
    """
    
    def __init__(self, 
                 settings_file_path = 'config/settings.json',
                 coordinates_file_path = 'config/coordinates.csv',
                 edges_file_path = 'config/edges.txt'):
        
        """
        Costruttore della classe Courier, che inizializza i parametri 
        del robot e del control system.
        
        :param settings_file_path: path del file json contenente i parametri
        :param coordinates_file_path: path del file csv contenente le coordinate
        :param edges_file_path: path del file txt contenente gli archi tra i nodi
        """
        
        with open(settings_file_path, "r") as f:
            params = json.load(f)
            
        params["package_map"] = {int(k): v for k, v in params["package_map"].items()}
        
        self.robot = Multirotor(
            x_origin=params["x_origin"], 
            y_origin=params["y_origin"],
            z_origin=params["z_origin"],
        )
        
        self.save = params["save_graphs"]
        self.save_path = params["graphs_save_path"]
        
        self.control_system = ControlSystem(self.robot, coordinates_file_path, edges_file_path)
        self.control_system.start(package_order=params["package_order"], package_map=params["package_map"])
    
    def run_simulation(self):
        """
        Esegue la simulazione su Godot e ne salva o visualizza i grafici di posizione e velocità rispetto al tempo
        
        :return: None
        """
        self.control_system.run()
        self.control_system.plot_graph(self.save, self.save_path)