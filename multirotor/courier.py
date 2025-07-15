from control_system import *
from lib.dds.dds import *
from lib.data.dataplot import *

class Courier():
    
    def __init__(self, x_origin, y_origin, z_origin, coordinates_path, edges_path, package_order, package_map):
        self.robot = Multirotor(x_origin = x_origin, y_origin=y_origin, z_origin=z_origin)
        self.control_system = ControlSystem(self.robot, coordinates_path, edges_path)
        self.control_system.start(package_order, package_map)
    
    def start_loop(self):
        
        self.time_axis = []
        self.x_movements = []
        self.y_movements = []
        self.z_movements = []
        
        self.vx_axis = []
        self.vy_axis = []
        self.vz_axis = []
        
        dds = DDS()
        dds.start()
        
        
        move_list = self.control_system.move_list
        
        move_command = move_list.pop(0)
        move_command.start()
        
        dds.subscribe(['start','tick', 'X', 'Y', 'Z', 'TX', 'TY', 'TZ', 'VX', 'VY', 'VZ', 'WX', 'WY', 'WZ'])

        t = Time(use_fake_time=False)
        t.start()

        while True:
            dds.wait('tick')
            delta_t = t.elapsed()
            
            z = dds.read('Z')
            vz = dds.read('VZ')
            
            x = dds.read('X')
            vx = dds.read('VX')
            
            y = dds.read('Y')
            vy = dds.read('VY')
            
            roll = dds.read('TX')
            roll_rate = dds.read('WX')
            
            pitch = dds.read('TY')
            pitch_rate = dds.read('WY')
            
            if type(move_command) == AttachMovement:
                dds.publish('attached', move_command.evaluate(delta_t), DDS.DDS_TYPE_INT)
                
                if move_list == []:
                    break
                    
                move_command = move_list.pop(0)
                move_command.start()

            else:  
                (f1, f2, f3, f4) = self.robot.evaluate(delta_t, z, vz, x, vx, y, vy, roll, roll_rate, pitch, pitch_rate)
                move_command.evaluate(delta_t)
                
                if move_command.movement_done():
                    print("FINITO MOVIMENTO")
                    
                    if move_list == []:
                        print("FINITO")
                        break
                        
                    move_command = move_list.pop(0)
                    move_command.start()

            dds.publish('f1', f1, DDS.DDS_TYPE_FLOAT)
            dds.publish('f2', f2, DDS.DDS_TYPE_FLOAT)
            dds.publish('f3', f3, DDS.DDS_TYPE_FLOAT)
            dds.publish('f4', f4, DDS.DDS_TYPE_FLOAT)

            self.time_axis.append(t.get())
            self.vx_axis.append((vx, self.robot.vx_target))
            self.vy_axis.append((vy, self.robot.vy_target))
            self.vz_axis.append((vz, self.robot.vz_target))
            self.x_movements.append((x, self.robot.x_target))
            self.y_movements.append((y, self.robot.y_target))
            self.z_movements.append((z, self.robot.z_target))
            
        dds.publish('f1', 0, DDS.DDS_TYPE_FLOAT)
        dds.publish('f2', 0, DDS.DDS_TYPE_FLOAT)
        dds.publish('f3', 0, DDS.DDS_TYPE_FLOAT)
        dds.publish('f4', 0, DDS.DDS_TYPE_FLOAT)

        dds.stop()

    def plot_graph(self):
        dpx = DataPlotter()
        dpx.set_x("time (seconds)")
        dpx.add_y("target_x", "target_x")
        dpx.add_y("current_x", "current_x")
        
        dpvx = DataPlotter()
        dpvx.set_x("time (seconds)")
        dpvx.add_y("target_vx", "target_vx")
        dpvx.add_y("current_vx", "current_vx")
        
        dpy = DataPlotter()
        dpy.set_x("time (seconds)")
        dpy.add_y("target_y", "target_y")
        dpy.add_y("current_y", "current_y")
        
        dpvy = DataPlotter()
        dpvy.set_x("time (seconds)")
        dpvy.add_y("target_vy", "target_vy")
        dpvy.add_y("current_vy", "current_vy")

        dpz = DataPlotter()
        dpz.set_x("time (seconds)")
        dpz.add_y("target_z", "target_z")
        dpz.add_y("current_z", "current_z")
        
        dpvz = DataPlotter()
        dpvz.set_x("time (seconds)")
        dpvz.add_y("target_vz", "target_vz")
        dpvz.add_y("current_vz", "current_vz")
        
        for i in range(0, len(self.time_axis)):
            dpvy.append_x(self.time_axis[i])
            dpvy.append_y("target_vy", self.vy_axis[i][1])
            dpvy.append_y("current_vy", self.vy_axis[i][0])
            
            dpy.append_x(self.time_axis[i])
            dpy.append_y("target_y", self.y_movements[i][1])
            dpy.append_y("current_y", self.y_movements[i][0])
            
            dpvx.append_x(self.time_axis[i])
            dpvx.append_y("target_vx", self.vx_axis[i][1])
            dpvx.append_y("current_vx", self.vx_axis[i][0])
            
            dpx.append_x(self.time_axis[i])
            dpx.append_y("target_x", self.x_movements[i][1])
            dpx.append_y("current_x", self.x_movements[i][0])
            
            dpvz.append_x(self.time_axis[i])
            dpvz.append_y("target_vz", self.vz_axis[i][1])
            dpvz.append_y("current_vz", self.vz_axis[i][0])

            dpz.append_x(self.time_axis[i])
            dpz.append_y("target_z", self.z_movements[i][1])
            dpz.append_y("current_z", self.z_movements[i][0])
            
        plot_multiple([dpvy, dpy, dpvx, dpx, dpvz, dpz])