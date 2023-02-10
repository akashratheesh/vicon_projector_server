from .base import tracked_item
import numpy as np
import pyqtgraph as pg

class image_item(tracked_item):
    '''

    Attributes:
        name(str): Unique name to identify items on the canvas/projection server.
        image(numpy.ndarray): Image RGB array. Use :obj:`np.asarray(Image.open("IMAGE_NAME").load())`.
        position(numpy.ndarray = [x,y]): Position of the item. Sets ``handle.position``, if available.
        width(float): Width of the image.
        height(float): Height of the image.
        zValue(float): Z-Value of the item. Determines how items are stacked. `Relative` (Higher Z-Value = Top).
        tracking_offset (list[float]): Defines how posiiton is offset from vicon/ros position. Check more info at `tracked_item.tracking_offset`
        **kwargs: Additional Keyword arguments. Will be passed on to the actual pyqtgraph graphic item handle
    '''
    def __init__(self,
                name: str,
                image: np.ndarray,
                position: np.ndarray,
                width: float,
                height: float,
                zValue:float = None,
                tracking_offset: 'list[float]' = [0.0,0.0],
                **kwargs):

        self.height = height
        self.width = width

        # Create a new pyqtgraph image item
        self.handle = pg.ImageItem(image=image,**kwargs)

        # Set Initial Position
        self.handle.setRect(position[0]-width/2,      # Origin at Center of image
                        position[1]-height/2,         # Origin at Center of image
                        width,
                        height)
        

        super().__init__(name=name,
                        handle = self.handle,
                        position=position,
                        zValue=zValue,
                        tracking_offset = tracking_offset)


        
    def position_updater(self):


        self.handle.setRect(self.position[0]-self.width/2,      # Origin at Center of image
                    self.position[1]-self.height/2,             # Origin at Center of image
                    self.width,
                    self.height)
        
