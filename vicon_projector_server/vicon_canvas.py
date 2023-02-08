from PyQt6 import QtWidgets, QtGui
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import os
import json
import numpy as np

class vicon_canvas(QtWidgets.QMainWindow):
    
    def __init__(self, config_data:dict, *args, **kwargs):
        super(vicon_canvas, self).__init__(*args, **kwargs)

        self.config_data = config_data

        self.xmin = config_data["x"][0]
        self.xmax = config_data["x"][1]

        self.ymin = config_data["y"][0]
        self.ymax = config_data["y"][1]

        self._bg = None               

        self.create_canvas()



    def create_canvas(self):
        ''' Create Canvas
        
            * Hide axis
            * Set Axis Range
            * Disable Mouse interaction
            * Move the canvas to preferred monitor/projector
        '''
        self.window = pg.PlotWidget()
        self.setCentralWidget(self.window)
        self.hide_axis()
        
        self.set_axis_range()

        self.window.setMouseEnabled(x=False, y=False)           # Prevent Mouse interactions (panning/zooming)

        monitors = QtGui.QScreen.virtualSiblings(self.screen())
        
        if "display_monitor" in self.config_data.keys():
            self.monitor = monitors[self.config_data["display_monitor"]].availableGeometry()
        else:
            self.monitor = monitors[0].availableGeometry()

        self.move(self.monitor.left(), self.monitor.top())

    def set_axis_range(self):
        ''' Set Axis Range
        '''
        self.window.setXRange(self.xmin, self.xmax, padding=0)  # Set X Range
        self.window.setYRange(self.ymin, self.ymax, padding=0)  # Set Y Range

    def hide_axis(self):
        ''' Hide Axis
        '''
        self.window.getPlotItem().hideAxis('top')
        self.window.getPlotItem().hideAxis('bottom')
        self.window.getPlotItem().hideAxis('left')
        self.window.getPlotItem().hideAxis('right')

    def show_axis(self):
        '''Show Axis
        '''
        self.window.getPlotItem().showAxis('bottom')
        self.window.getPlotItem().showAxis('left')

    def set_background(self,color: tuple = None,
                            image: np.ndarray = None):
        '''Set Canvas Background

        Parameters:
            color(tuple): RGB/RGBA Tuple of the background color
            image(np.ndarray): Image array
        '''
        if self._bg:
            print("yess")

        if color is not None:
            assert image is None, "Cannot specify background image along with background color"
            self.window.setBackground(color)
        
        if image is not None:
            assert color is None, "Cannot specify background color along with background image"

            
            # Image Item
            self._bg = pg.ImageItem(image=image)
            self._bg.setRect(self.xmin,             # x
                        self.ymin,                  # y
                        self.xmax-self.xmin,        # width
                        self.ymax-self.ymin)        # height

            self._bg.setZValue(-100)                # Setting as bottom layer
            self.window.addItem(self._bg)
            
        



