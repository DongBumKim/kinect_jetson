#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  20 02:07:13 2019

@author: prabhakar
"""
import sys
#print(sys.path)
sys.path.insert(1, './pyKinectAzure/')
#sys.path.append("/usr/lib/aarch64-linux-gnu/libk4a/")
#print(sys.path)
# import necessary argumnets 
import gi
import cv2
import argparse
import cv2
import pykinect_azure as pykinect


# import required library like Gstreamer and GstreamerRtspServer
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject

pykinect.initialize_libraries()
#pykinect.initialize_libraries(track_body=True)
# Modify camera configuration
device_config = pykinect.default_configuration
device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
#device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
#device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_UNBINNED
##Depth_mode WFOV_unbinned supports only up to 15 fps
device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30
#device_config.depth_mode =     pykinect.K4A_DEPTH_MODE_OFF

# Start device
device = pykinect.start_device(config=device_config)
print("start device")

# Sensor Factory class which inherits the GstRtspServer base class and add
# properties to it.
class SensorFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, vtype, **properties):
        super(SensorFactory, self).__init__(**properties)
        #self.cap = cv2.VideoCapture(opt.device_id)
        # Initialize the library, if the library is not found, add the library path as argument
        self.vtype = vtype
        self.number_frames = 0
        self.fps = opt.fps
        self.duration = 1 / self.fps * Gst.SECOND  # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width={},height={},framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96' \
                             .format(opt.image_width, opt.image_height, self.fps)
    # method to capture the video feed from the camera and push it to the
    # streaming buffer.
    def on_need_data(self, src, length):
        if True:
            capture = device.update()
            if self.vtype == 'depth':
                ret, image = capture.get_colored_depth_image()
                #ret, image = capture.get_depth_image()
            elif self.vtype == 'rgb':
                ret, image = capture.get_color_image()
            elif self.vtype == 'ir':
                ret, image = capture.get_colored_ir_image()
                
            if ret:
                # It is better to change the resolution of the camera 
                # instead of changing the image shape as it affects the image quality.
                frame = cv2.resize(image, (opt.image_width, opt.image_height), \
                    interpolation = cv2.INTER_LINEAR)
                data = frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.number_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.number_frames += 1
                retval = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.number_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if retval != Gst.FlowReturn.OK:
                    print(retval)
                    
    # attach the launch string to the override method
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    # attaching the source element to the rtsp media
    def do_configure(self, rtsp_media):
        self.number_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)

# Rtsp server implementation where we attach the factory sensor with the stream uri
class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory_rgb = SensorFactory(vtype='rgb')
        self.factory_depth = SensorFactory(vtype='depth')
        self.factory_ir = SensorFactory(vtype='ir')
        
        self.factory_rgb.set_shared(True)
        self.factory_depth.set_shared(True)
        self.factory_ir.set_shared(True)
        
        self.set_service(str(opt.port))
        
        self.get_mount_points().add_factory('/rgb', self.factory_rgb)
        self.get_mount_points().add_factory('/depth', self.factory_depth)
        self.get_mount_points().add_factory('/ir', self.factory_ir)
        self.attach(None)

# getting the required information from the user 
parser = argparse.ArgumentParser()
parser.add_argument("--fps", required=True, help="fps of the camera", type = int)
parser.add_argument("--image_width", required=True, help="video frame width", type = int)
parser.add_argument("--image_height", required=True, help="video frame height", type = int)
parser.add_argument("--port", default=8554, help="port to stream video", type = int)
parser.add_argument("--stream_uri", default = "/video_stream", help="rtsp video stream uri")
opt = parser.parse_args()



# initializing the threads and running the stream on loop.
GObject.threads_init()
Gst.init(None)
server = GstServer()
loop = GObject.MainLoop()
loop.run()
