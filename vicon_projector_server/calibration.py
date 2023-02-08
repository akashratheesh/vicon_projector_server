import json
import sys
import numpy as np
from tabulate import tabulate

from PyQt6 import QtWidgets
import pyqtgraph as pg

from threading import Thread

from .vicon_canvas import vicon_canvas


class Calibration_Setup:
    '''Calibration Setup to map Vicon axis to Canvas 
    plot Axis. 

    Parameters:
        tracker_name(str): Name of the calibration tracker. Eg: tracker@ip_address
        monitor_number(int): Display number of Monitor/Projector to start calibration. Default = 0

    Attributes:
        tracker_position(List[int]=>[x,y]): To store position data from vicon.
        x_multiplier(List[int]=>[x1,x2,...,x3]): List of X axis multiplier. X multiplier = vicon_x_position/screen_x_position
        y_multiplier(List[int]=>[y1,y2,...,y3]): List of Y axis multiplier. Y multiplier = vicon_y_position/screen_y_position

        x_mean(float): Mean of X Axis Multiplier
        x_std(float): Standard Deviation of X Axis Multipler

        y_mean(float): Mean of Y Axis Multiplier
        y_std(float): Standard Deviation of Y Axis Multipler
        
    '''
    def __init__(self, tracker_name:str,
                monitor_number:int = 0):
        
        self.tracker_name = tracker_name
        self.monitor_number = monitor_number

        self.tracker_position = [1,1]
        
        self.x_multiplier = []
        self.y_multiplier = []

        self.x_mean = 0
        self.x_std = 0

        self.y_mean = 0
        self.y_std = 0

        

        # QT Application
        self.app = QtWidgets.QApplication([])

        # Load Sample config data
        self.config_data = self.get_sample_config_data()
        
        # Create a new Canvas with sample config.
        # X Limit = [0, width of the monitor]
        # Y Limit = [0, height of the monitor]
        self.canvas = vicon_canvas(config_data=self.config_data)

        # Set Plot axis to monitor width and height
        self.config_data["x"] = [0, self.canvas.monitor.width()]
        self.config_data["y"] = [0, self.canvas.monitor.height()]
        self.canvas.xmin,self.canvas.xmax = self.config_data["x"]
        self.canvas.ymin,self.canvas.ymax = self.config_data["y"]
        self.canvas.set_axis_range()
    
    def calculate_statistics(self):
        ''' Calculate mean and std of X and Y axis mulitplier.

        Updates x_mean, x_std, y_mean, y_std
        '''

        if len(self.x_multiplier):
            self.x_mean = np.round(np.mean(self.x_multiplier),6)
            self.x_std = np.round(np.std(self.x_multiplier),6)

            self.y_mean = np.round(np.mean(self.y_multiplier),6)
            self.y_std = np.round(np.std(self.y_multiplier),6)
        else:
            self.x_mean = 0
            self.x_std = 0

            self.y_mean = 0
            self.y_std = 0
    
    def start(self):
        ''' Start Calibration
        '''
        
        # Start Menu in new thread
        menu_thread = Thread(target=self.menu)
        menu_thread.start()

        self.canvas.showFullScreen()
        sys.exit(self.app.exec())
    
    def get_sample_config_data(self)->dict:
        ''' Generate Sample Configuration data

        Returns:
            dict: Sample Configuration
        '''
        _config = {}

        # Display Monitor
        _config["display_monitor"] = self.monitor_number

        # X Limits
        _config["x"] = [0, 200]

        # Y Limits
        _config["y"] = [0, 200]

        # Hostname for JSON RPC
        _config["hostname"] = "0.0.0.0"

        # Port for JSON RPC
        _config["port"] =  4000

        return _config
    
    def save_config(self, filename:str):
        ''' Save current configuration to json file

        Parameters:
            filename(str): Name of the configuration file

        '''
        self.config_data["_COMMENTS_"] = "Auto-generated config file."
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=4)
    
    def add_calibration_point(self):
        ''' Add new calibration point.

        Read position from tracker data
            X multiplier = vicon_x_position/screen_x_position
            Y multiplier = vicon_y_position/screen_y_position

        '''
        

        loc = [0,0]
        loc[0] = np.random.uniform(low=self.canvas.xmin,high = self.canvas.xmax)
        loc[1] = np.random.uniform(low=self.canvas.ymin,high = self.canvas.ymax)

        loc = np.round(loc,4)
        self.plot_calib_point(loc)
        

        _user_input = input("Press y|Y to save current tracker position: ").upper()

        if _user_input == "Y":
            self.x_multiplier.append(self.tracker_position[0]/loc[0])
            self.y_multiplier.append(self.tracker_position[1]/loc[1])
            


    def delete_calibration_point(self):
        ''' Delete a calibration point from the data
        '''
        try:
            _user_input = int(input("Enter index of the calibration point to delete: "))

            del self.x_multiplier[_user_input]
            del self.y_multiplier[_user_input]


        except Exception as e:
            print(e)
            print("Unable to delete the point.")

    def confirm_and_save(self):
        try:

            # Adjust Axis Limits
            self.config_data["x"][0] *= self.x_mean
            self.config_data["x"][1] *= self.x_mean

            self.config_data["y"][0] *= self.y_mean
            self.config_data["y"][1] *= self.y_mean


            _user_input = input("Enter file name:[projection_config.json]: ")

            if _user_input:
                _filename = _user_input
            else:
                _filename = "projection_config.json"
            
            self.save_config(filename= _filename)
        
        except Exception as e:
            print("Unabled to save configuration")
        
    
    def plot_calib_point(self,loc):
        '''Plot Crosshair on canvas
        '''

        pen = pg.mkPen(color=(0, 255, 0))
        plot_handle = self.canvas.window
        plot_handle.clear()

        plot_handle.plot([loc[0],loc[0]],[0,self.canvas.ymax], pen=pen)
        plot_handle.plot([0,self.canvas.xmax],[loc[1],loc[1]], pen=pen)

        _rectangle = self._rectangle(loc)
        plot_handle.plot(_rectangle[0],_rectangle[1], pen=pen)


    
    def menu(self):
        '''Render Menu and get user input
        '''
        self.canvas.window.clear()
        print(self._menu_string())
        try:
            _user_input = int(input("Enter Option: "))

            if _user_input == 1:
                self.add_calibration_point()
            elif _user_input == 2: 
                self.delete_calibration_point()
            elif _user_input == 3:
                self.confirm_and_save()
            else:
                print("Error")

        except Exception as e:
            print(e)
            print("Invalid Option.")


        self.menu()

    def _menu_string(self):
        '''Generate Menu String

        Used by menu()
        '''
        _menu = "\n"

        if len(self.x_multiplier):
            _table = []
            self.calculate_statistics()
            for i in range(len(self.x_multiplier)):
                _row = [i, self.x_multiplier[i],
                        self.y_multiplier[i],
                        self.x_multiplier[i] - self.x_mean,
                        self.y_multiplier[i] - self.y_mean]
                _table.append(_row)
     
            _menu += tabulate(_table,headers=["Index", f"X Multiplier (Mean: {self.x_mean})",
                                            f"Y Multiplier (Mean: {self.y_mean})",
                                            f"X-X_Mean (Std: {self.x_std})",
                                            f"Y-Y_Mean (Std: {self.y_std})"])

        _menu += "\n\n1. Add new calibration point"
        _menu += "\n2. Delete calibration point"
        _menu += "\n3. Save"

        return _menu

    def _rectangle(self,loc):
        ''' Get Rectangle Lines

        Parameters:
            loc(List[int]): Center of Location of the rectangle

        '''

        # Rectangle Distance
        distance_x = 30
        distance_y = 30

        _xmin = loc[0] - distance_x/2
        _ymin = loc[1] - distance_y/2

        _xmax = loc[0] + distance_x/2
        _ymax = loc[1] + distance_y/2
        
        _rectangle = [[],[]]
        _rectangle[0] = [_xmin,_xmax,_xmax,_xmin,_xmin]
        _rectangle[1] = [_ymin,_ymin,_ymax,_ymax,_ymin]
        return _rectangle
    
    
    def vicon_position_updator(self,t):
        '''Vicon Position Callback Function
        
        Parameters:
            t: Vicon Data
        '''
        self.tracker_position = [t['position'][0], t['position'][1]]
    
    def vicon_tracker(self):
        ''' Vicon Tracker Loop.
        
        This function needs to run in a seperate thread.
        '''
        self.vicon_handle  = vrpn.receiver.Tracker(self.tracker_name)
        self.vicon_handle.register_change_handler(None,self.vicon_position_updator,'position')
        
        while True:
            self.vicon_handle.mainloop()
