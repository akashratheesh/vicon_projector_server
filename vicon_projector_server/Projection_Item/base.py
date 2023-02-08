import numpy as np

class tracked_item:
    '''Base Item
        
    '''
    def __init__(self,
                name: str,
                handle:'pyqtgraph.GraphicsObject',
                position: np.ndarray,
                zValue: float = None):

        self.name = name

        self.position = position

        self.handle = handle

        if zValue is not None:
            self.zValue = zValue
    
    

    def ros_callback(self,**kwargs):
        '''Ros Callback

        Callback function for ROS Topic

        '''
        return NotImplementedError()

    def vicon_callback(self, **kwargs):
        '''Vicon Callback

        Callback function for Vicon Datastream. Generally updates position.

        Override to use custom method.

        '''
        return NotImplementedError()

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
