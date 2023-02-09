from vicon_projector_server import Projection_Server, Projection_Item
from PIL import Image
import numpy as np

if __name__ == "__main__":

    # Create a Projection Server with config file
    projection_server = Projection_Server(config_file = "../sample_config.json")

    # Open the circle image as np array
    spot = Image.open("circle.png")
    spot.load()
    spot = np.asarray(spot)

    
    # Create a new Image Item
    # Set an Initial Position
    # Name needs to be unique
    img_obj1 = Projection_Item.image_item(name = "spot1",
                                        image = spot,
                                        position = [5,5],
                                        width = 1,
                                        height = 1)

    # Add new image item to the projection server
    projection_server.add_new_item(item=img_obj1)

    # Start the projection server
    projection_server.run()