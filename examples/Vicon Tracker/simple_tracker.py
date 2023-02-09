from PyQt6 import QtWidgets
from vicon_projector_server import Vicon_Canvas, Projection_Server, Projection_Item
import sys
from PIL import Image

import numpy as np
import copy
import time


# Create a new projection Server
projection_server = Projection_Server(config_file = "../sample_config.json")

# Open the circle image
spot = Image.open("circle.png")
spot.load()
spot = np.asarray(spot,dtype="int32")   # Load as an np array


# Create a new Image Item
# Set an Initial Position
# Name needs to be unique
spot = Projection_Item.image_item(name = "spot1",
                                    image = spot,
                                    position = [5,5],
                                    width = 1,
                                    height = 1)

# Setup Vicon Tracker
spot.set_vicon_tracker('tracker@localhost')

# Add new image item to the projection server
projection_server.add_new_item(spot)

# Start the projection server
projection_server.run()
