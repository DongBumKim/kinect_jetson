# RTSP streaming using GStreamer
https://github.com/prabhakar-sivanesan/OpenCV-rtsp-server 


Python implementation to stream camera feed from OpenCV videoCapture via RTSP server using GStreamer 1.0.

## Installation

This implementation has been developed and tested on Ubuntu 16.04 and 18.04. So the installation steps are specific to debian based linux distros.

### Step-1 Install GStreamer-1.0 and related plugins
    sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
### Step-2 Install RTSP server
    sudo apt-get install libglib2.0-dev libgstrtspserver-1.0-dev gstreamer1.0-rtsp
### Requirement
- Python 3.x
- Opencv 3.x or above ( pip install opencv-python )

## Pull pyKinectAzure

    git clone https://github.com/HJSIFEN/kinect-rtp.git
    cd kinect-rtp
    git clone https://github.com/ibaiGorordo/pyKinectAzure

## Azure Kinect Installation

### CPU : ARM
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/multiarch/prod
    sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/multiarch/prod
    sudo apt-get update
    sudo apt install libk4a1.4-dev libk4a1.4 k4a-tools

### CPU : AMD
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
    sudo apt-get update
    sudo apt install libk4a1.4-dev libk4a1.4 k4a-tools

## Python Requirements
    python3 -m pip install ctypes numpy python-opencv


# https://github.com/microsoft/Azure-Kinect-Sensor-SDK/blob/develop/docs/usage.md#linux-device-setup

### Usage
> Run stream.py with required arguments to start the rtsp server
##### Sample 
    python stream_depth.py --fps 30 --image_width 640 --image_height 480 --port 8554 
    python3 stream_depth.py --fps 30 --image_width 640 --image_height 480 --port 8554 

    python3 stream.py --fps 15 --image_width 1024 --image_height 1024 --port 8554
### 환경변수 설정 : illegal instruction error && display error
    vi ~/.bashrc

> add two lines below
    export OPENBLAS_CORETYPE=ARMV8 python
    export DISPLAY=:0

    source ~/.bashrc

>  Warning : Power Jetson Nano without a connected monitor(display)


### Visualization

Use 'open-rtsp.py' in order to decode depth information.

e.g: `rtsp://192.168.1.12:8554/rgb, or depth, or ir`

You can either use any video player which supports rtsp streaming like VLC player or you can use the `open-rtsp.py` script to view the video feed.


https://copycoding.tistory.com/154