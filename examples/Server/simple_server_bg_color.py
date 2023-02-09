from vicon_projector_server import Projection_Server
from PIL import Image
import numpy as np

if __name__ == "__main__":

    # Create a Projection Server with config file
    projection_server = Projection_Server(config_file = "sample_config.json")

    # Open Image as an np array
    bg_img = Image.open("bg.jpeg")
    bg_img.load()
    bg_img = np.asarray(bg_img)

    # Set Background Color (Either RGB or RBA)
    canvas = projection_server.get_canvas()
    canvas.set_background(color=(255,0,0))

    # Start the projection server
    projection_server.run()