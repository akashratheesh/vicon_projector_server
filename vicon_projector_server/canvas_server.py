from PyQt6 import QtWidgets
from vicon_projector_server import Vicon_Canvas
from vicon_projector_server import rpc_server
import sys
import os
import json

from pyqtgraph.Qt import QtGui, QtCore

from threading import Thread

class Projection_Server:
    
    def __init__(self, config_file: str):

        self.app = QtWidgets.QApplication([])
        self.load_config_data(config_file = config_file)
        self.canvas = Vicon_Canvas(self.config_data)
        self.plot_handle = self.canvas.window

        self.managed_threads = {}
        self.rpc_server = rpc_server.JSON_RPC_Server(projection_server = self,
                                                    hostname=self.config_data.get("hostname"),
                                                    port = self.config_data.get("port"))

        
        # Plot Items
        self.all_plot_items = {}

    def test_connection(self):
        '''
        Method to JSON-RPC client can call to test connection to server

        Returns:
            dict: Return payload. Check for `connection` key in payload

        '''
        payload = {
            "connection": True
        }
        return payload
    
    def vicon_loop(self):
        ''' Loop through all tracked item and run vrpn mainloop
        '''
        while True:
            for item in self.all_plot_items:
                if self.all_plot_items[item].is_vicon_tracked:
                    self.all_plot_items[item].vicon_tracker.mainloop()
    
    def position_update(self):
        
        
        for item in self.all_plot_items:
            self.all_plot_items[item].position_updater()

        self.app.processEvents()

    def run_canvas(self)->None:
        '''
        Method to start canvas(PyQTGraph). Do not call directly

        Returns:
            None:
        '''
        self.canvas.showFullScreen()
        #sys.exit(self.app.exec())

        timer = QtCore.QTimer() # to create a thread that calls a function at intervals
        timer.timeout.connect(self.position_update)
        timer.start(self.config_data.get("update_ms",25))

        QtGui.QGuiApplication.instance().exec()
        #sys.exit(self.app.exec())

    def run(self) -> None:
        '''
        Method to start projection server.

            * Starts RPC Server in a new thread.
            * Starts canvas in the main thread.
        
        Returns:
            None:

        '''
        self.managed_threads["JSON_RPC"] = Thread(target=self.rpc_server.run)
        self.managed_threads["JSON_RPC"].start()

        self.managed_threads["VICON_LOOP"] = Thread(target=self.vicon_loop)
        self.managed_threads["VICON_LOOP"].start()
        

        self.run_canvas()

        for thread in self.managed_threads:
            
            self.managed_threads[thread].join()

    def get_all_plot_items(self) -> dict:
        _payload = {}
        for plot_item in self.all_plot_items.keys():
            _payload[plot_item] = {}
            _payload[plot_item]["name"] = plot_item
            _payload[plot_item]["type"] = str(self.all_plot_items[plot_item].__class__.__name__)
            
        return _payload

    def get_canvas(self) -> 'Vicon_Canvas':
        '''Returns canvas object handle

        Returns:
            Vicon_Canvas: Vicon canvas handle 
        '''
        return self.canvas
    
    def get_plot_handle(self) -> 'Vicon_Canvas.window':
        '''Return Plot handle (:obj:`PyQtGraph.PlotWidget`)

        Returns:
            Vicon_Canvas.window: Plot handle.
        '''
        return self.plot_handle
    
    def load_config_data(self,config_file: str) -> None:
        ''' Load configuration data from file. Do not call directly.

            * Called in constructor
        
        Returns:
            None:
        '''
        assert os.path.isfile(config_file), "File does not exist." 
        
        _f = open(config_file)
        self.config_data = json.load(_f)

    # Add plot item
    def add_new_item(self, item) -> None:
        ''' Add new item to the canvas.

        Returns:
            None:
        '''
        
        # Check if name already exist
        if item.name in self.all_plot_items.keys():
            raise NameError(f"Item with same name ('{item.name}') already exist.'")

        self.all_plot_items[item.name] = item
        self.plot_handle.addItem(item.handle)
    
    # Remove Item
    def remove_item(self,name:str = None):

        ''' Remove item from canvas.

        Attributes:
            name(str): Name of the item.

        Returns:
            bool: Return True if success. Raises NameError if the name/item is not found.
        '''
  
        try:
            # Remove from canvas
            self.canvas.window.removeItem(self.all_plot_items[name].handle)
            
            # Delete from list
            del self.all_plot_items[name]

            return True
        except:
            raise NameError(f"Item (Name: '{name}') does not exist")
    
    # Hide Item
    def hide_item(self,name:str,hide=True):
        ''' Hide item from canvas.

        Attributes:
            name(str): Name of the item.
            hide(bool): Default: True. Set to False to show the item.

        Returns:
            bool: Return True if success. Raises Error if the name/item is not found.
        '''
        
        if hide:
            self.all_plot_items[name].handle.hide()
        else:
            self.all_plot_items[name].handle.show()
        
        return True

           
