from PyQt6 import QtWidgets
from vicon_projector_server import vicon_canvas, Projection_Server, projection_item
import sys
from PIL import Image

import numpy as np
import copy
import time


project_server = Projection_Server(config_file = "projection_config.json")

canvas = project_server.get_canvas()
plot_handle = project_server.get_plot_handle()

bg_img = Image.open("sample_bg.jpeg")
bg_img.load()
bg_img = np.asarray(bg_img,dtype="int32")


robot_img = Image.open("sample_agent.png").rotate(-90)
robot_img.load()
robot_img = np.asarray(robot_img,dtype="int32")


img_obj1 = projection_item.image_item(name = "robot1",
                                    image = robot_img,
                                    position = [0,0],
                                    width = 100,
                                    height = 100)

img_obj2 = projection_item.image_item(name = "robot2",
                                    image = robot_img,
                                    position = [100,100],
                                    width = 100,
                                    height = 100)





canvas.set_background(image = bg_img)

project_server.add_new_item(img_obj1)

project_server.add_new_item(img_obj2)



project_server.run()

