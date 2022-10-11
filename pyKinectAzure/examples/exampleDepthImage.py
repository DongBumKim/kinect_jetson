import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(1, '../')
import pykinect_azure as pykinect

if __name__ == "__main__":

        # Initialize the library, if the library is not found, add the library path as argument
        pykinect.initialize_libraries()

        # Modify camera configuration
        device_config = pykinect.default_configuration
        #device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
        device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
        device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
        # Start device
        device = pykinect.start_device(config=device_config)

        cv2.namedWindow('Depth Image',cv2.WINDOW_NORMAL)
        while True:

                # Get capture
                capture = device.update()

                # Get the color depth image from the capture
                #ret, depth_image = capture.get_colored_depth_image()
                ret, depth_image = capture.get_depth_image()
                #print(depth_image.dtype)
                if not ret:
                        continue
                        
                # Plot the image
                cv2.imshow('Depth Image',depth_image)

                # Press q key to stop
                if cv2.waitKey(1) == ord('q'):  
                        break
