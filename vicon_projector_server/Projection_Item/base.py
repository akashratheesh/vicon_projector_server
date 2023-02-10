import numpy as np
from typing import Callable
import vrpn

class tracked_item:
    '''Base Item

    Attributes:
        name(str): Unique name to identify items on the canvas/projection server.
        position(numpy.ndarray = [x,y]): Position of the item. Sets ``handle.position``, if available.
        zValue(float): Z-Value of the item. Determines how items are stacked. `Relative` (Higher Z-Value = Top).
        tracking_offset (list[float]): Defines how posiiton is offset from vicon/ros position. Check the attritube description for more info.        
    '''
    def __init__(self,
                name: str,
                handle:'pyqtgraph.GraphicsObject',
                position: np.ndarray,
                zValue: float = None,
                tracking_offset: 'list[int]' = [0.0,0.0]):

        self.name = name

        self.position = position

        self.handle = handle

        self.is_vicon_tracked = False

        if zValue is not None:
            self.zValue = zValue
        
        self.tracking_offset = tracking_offset
    
    def set_vicon_tracker(self, tracker_name:str,
                        enable_position:bool = True,
                        enable_velocity:bool = False,
                        position_callback:Callable = None,
                        velocity_callback:Callable = None):
        '''Setup Vicon tracker

        Parameters:
            tracker_name(str): Name of the tracker. Eg: tracker@ip_address
            enable_position(bool): Enable callback function for position data. Default: True
            enable_velocity(bool): Enable callback function for velocity data. Default: False
            position_callback(function): Overrides default vicon_position_callback function. 
                                        Function format: fn(obj,position_data)
            velocity_callback(function): Overrides default vicon_velocity_callback function. 
                                        Function format: fn(obj,velocity_data)

        '''
        self.vicon_tracker = vrpn.receiver.Tracker(tracker_name)

        if enable_position:
            if position_callback:
                _position_fn = position_callback
            else:
                _position_fn = self.vicon_position_callback
            
            # Set callback handler
            self.vicon_tracker.register_change_handler(None,_position_fn,"position")
            self.is_vicon_tracked = True
            self.vicon_position = []
        
        if enable_velocity:
            if velocity_callback:
                _velocity_fn = velocity_callback
            else:
                _velocity_fn = self.vicon_velocity_callback
            
            # Set callback handler
            self.vicon_tracker.register_change_handler(None,_velocity_fn,"velocity")
            self.is_vicon_tracked = True
            self.vicon_velocity = []
    

    def ros_callback(self,**kwargs):
        '''Ros Callback

        Callback function for ROS Topic

        '''
        return NotImplementedError()

    def vicon_position_callback(self, custom_data, data):
        '''Vicon Callback

        Position Callback function for VRPN. Override to use custom method.

        Parameters:
            data(dict): Vicon Data

        '''
        self.vicon_position = [data['position'][0] + self.tracking_offset[0],
                            data['position'][1] + self.tracking_offset[1]]
        self.position = self.vicon_position
    
    def vicon_velocity_callback(self, custom_data, data):
        '''Vicon Callback

        Velocity Callback function for VRPN. Override to use custom method.

        Parameters:
            data(dict): Vicon Data

        '''
        self.vicon_velocity = [data['velocity'][0], data['velocity'][1]]
        
    def position_updater(self):
        ''' Defines how graphic item's position is updated.
        Should use ``position`` attribute to get updated position

        '''
        raise NotImplementedError()

    @property
    def name(self):
        '''str: Unique name to identify items on the canvas/projection server.
        
        '''
        return self._name
    
    @name.setter
    def name(self,value):
        self._name = value

    @property
    def handle(self):
        '''pyqtgraph.GraphicsObject: PyQtGraph Graphics object handle.
        '''
        return self._handle
    
    @handle.setter
    def handle(self,value):
        self._handle = value


    @property
    def position(self):
        '''numpy.ndarray = [x,y]: Position of the item. Sets ``handle.position``, if available.
    
        '''
        return self._position

    @position.setter
    def position(self,value: np.ndarray):
        self._position = value

    @property
    def tracking_offset(self):
        '''numpy.ndarray: Position offset for ROS and Vicon callback.

        Sets:
            ``position = ros_position + tracking_offset`` 
            
            or

            ``position = vicon_position + tracking_offset``

        '''
        return self._tracking_offset
    
    @tracking_offset.setter
    def tracking_offset(self,value: np.ndarray):
        self._tracking_offset = value

    @property
    def zValue(self):
        '''float: Z-Value of the item

        Determines how items are stacked. `Relative` (Higher Z-Value = Top). 
        
        '''
        return self.handle.zValue
    
    @zValue.setter
    def zValue(self,value):
        self.handle.setZValue(value) 
