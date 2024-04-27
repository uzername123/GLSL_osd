#!/usr/bin/python3

import signal
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

Gst.init(None)

#pipeline_str = "videotestsrc ! videoconvert ! videocrop ! videoconvert ! autovideosink"
pipeline_str = "v4l2src ! video/x-raw, width=640,height=480 ! glupload ! glcolorconvert ! gltransformation name=zoom ! gleffects_heat name=colorz ! gldownload ! glimagesink"
pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)

zoomlevel = [ 0, 0.2, 0.33, 0.4, 0.43, 0.45]
zoomindex = 0
zoom = pipeline.get_by_name("zoom")

# Function to set the zoom level
def set_zoom_level(level):
    zoom.set_property("translation-z",level)

# Signal handler to handle SIGUSR1
def sigusr1_handler(signum, frame):
    global zoomindex
    # Adjust the zoom level here, for example:
    zoomindex = 0 if zoomindex > 4 else zoomindex + 1
    print("Received SIGPOLL, zoom is: ", zoomindex + 1 , "x")
    set_zoom_level( zoomlevel[zoomindex] )  # 2x zoom

# Register the signal handler
signal.signal(signal.SIGPOLL, sigusr1_handler)

# Run an infinite loop to keep the script running
try:
    print("Running. Press Ctrl+C to exit.")
    while True:
        signal.pause()  # Wait for signals
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)
