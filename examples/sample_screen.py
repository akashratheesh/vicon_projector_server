from PyQt6 import QtWidgets
from vicon_projector_server import Vicon_Canvas, Projection_Server, Projection_Item
import sys
from PIL import Image

import numpy as np
import copy
import time


projection_server = Projection_Server(config_file = "/home/akashratheesh/Work/CU/vicon_projector/examples/sample_server/sample_calib.json")

canvas = projection_server.get_canvas()
plot_handle = projection_server.get_plot_handle()

bg_img = Image.open("/home/akashratheesh/Work/CU/vicon_projector/examples/sample_server/sample_bg.jpeg")
bg_img.load()
bg_img = np.asarray(bg_img,dtype="int32")


robot_img = Image.open("/home/akashratheesh/Work/CU/vicon_projector/examples/sample_server/sample_agent.png").rotate(-90)
robot_img.load()
robot_img = np.asarray(robot_img,dtype="int32")


img_obj1 = Projection_Item.image_item(name = "robot1",
                                    image = robot_img,
                                    position = [0,0],
                                    width = 100,
                                    height = 100)


canvas.set_background(image = bg_img)


projection_server.add_new_item(img_obj1)


projection_server.run()

