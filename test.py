#!/usr/bin/python3.9

# Import necessary libraries
import signal
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject
from OpenGL.GL import *
import numpy as np
from PIL import Image


Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

# Initialize GStreamer
Gst.init(None)


# Read shader fragment from file
with open("shader_all.frag", "r") as f:
    fragment_shader_src = '"\n' + f.read() + '"'
#print (fragment_shader_src)

fragment_shader = fragment_shader_src

fragment_shader = fragment_shader.replace( "ZOOM", "1.0" )

fragment_shader = fragment_shader.replace( "PALETTE", "3, 3, 3" )

#rint (fragment_shader)
#uniforms = Gst.Structure.new_empty("uniforms")
zoom_var = 1.0

# Construct the GStreamer pipeline with the glshader plugin
pipeline_str = "v4l2src ! video/x-raw,width=640,height=480 ! videoconvert ! glupload ! glcolorconvert ! glshader name=shadder fragment= " + fragment_shader + " ! gldownload ! videoconvert ! autovideosink"
#pipeline_str = "v4l2src device=/dev/video2 ! video/x-raw,width=256,height=196 ! videoconvert ! glupload ! glcolorconvert ! glshader fragment= " + fragment_shader + " name=shadder ! gldownload ! glimagesink"

#print (pipeline_str)

pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)
print (pipeline_str)

zoom = pipeline.get_by_name("shadder")
zoomlevel = [ 1.0, 0.5, 0.33, 0.25, 0.2 ]
zoomindex = 0
palette_num = [(3,3,3), (7,5,15), (4,5,6), (23,28,3), (21,22,23), (30,31,32), (33,13,10), (34,35,36)]
palette_idx=0

uniforms = Gst.Structure.new_empty("uniforms")
scale = GObject.Value(GObject.TYPE_FLOAT)
A = GObject.Value(GObject.TYPE_INT)
B = GObject.Value(GObject.TYPE_INT)
C = GObject.Value(GObject.TYPE_INT)
scale.set_float(1.0)
A.set_int(3)
B.set_int(3)
C.set_int(3)
uniforms.set_value("scale", scale)
uniforms.set_value("A", A)
uniforms.set_value("B", B)
uniforms.set_value("C", C)
zoom.set_property("uniforms", uniforms)
#uniforms.free()



# Function to set the zoom level
def set_zoom_level(level):
    print ("level=", level)
    scale.set_float(level)
    uniforms.set_value("scale", scale)
    zoom.set_property("uniforms", uniforms)

# Function to set the colorz
def set_palette(palette):
    print ("palette #=", palette)
    A.set_int(palette[0])
    B.set_int(palette[1])
    C.set_int(palette[2])
    uniforms.set_value("A", A)
    uniforms.set_value("B", B)
    uniforms.set_value("C", C)
    zoom.set_property("uniforms", uniforms)

# Signal handler to handle SIGUSR1
def sigzoom_handler(signum, frame):
    global zoomindex
    # Adjust the zoom level here, for example:
    zoomindex = 0 if zoomindex > 3 else zoomindex + 1
    print("Received SIGPOLL, zoom is: ", zoomindex + 1 , "x")
    set_zoom_level( zoomlevel[zoomindex] )  # 2x zoom

def sigpalette_handler(signum, frame):
    global palette_idx
    palette_idx = 0 if palette_idx > 6 else palette_idx + 1
    print("Received SIGPWR, palette # is: ", palette_idx , "colour")
    set_palette( palette_num[palette_idx] )  #

# Register the signal handler
signal.signal(signal.SIGPOLL, sigzoom_handler)
signal.signal(signal.SIGPWR, sigpalette_handler)

# Run the GStreamer main loop
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)
