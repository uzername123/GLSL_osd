#!/usr/bin/python3.9

# Import necessary libraries
import signal
import gi
import sys

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
#with open("shader_canny_v02.frag", "r") as f:
#    fragment_shader_src = '"\n' + f.read() + '"'
#print (fragment_shader_src)

frag_shader_text = '''
"
#version 100
#ifdef GL_ES
precision mediump float;
#endif


varying vec2 v_texcoord;
//uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;
uniform float scale;
uniform int A;
uniform int B;
uniform int C;

uniform sampler2D tex;
uniform vec2 texSize;
uniform float lowThreshold;
uniform float highThreshold;

const float PI = 3.14159265359;

void main() {
    
    vec2 texCoord = v_texcoord;
//   tex = tex;
//    texSize=vec2(width/1.0, height/1.0);
    // Sample surrounding pixels
    vec2 texSize = vec2(width,height);
    vec3 topLeft = texture2D(tex, texCoord + vec2(-1.0 / texSize.x, -1.0 / texSize.y)).rgb;
    vec3 top = texture2D(tex, texCoord + vec2(0.0, -1.0 / texSize.y)).rgb;
    vec3 topRight = texture2D(tex, texCoord + vec2(1.0 / texSize.x, -1.0 / texSize.y)).rgb;
    vec3 left = texture2D(tex, texCoord + vec2(-1.0 / texSize.x, 0.0)).rgb;
    vec3 center = texture2D(tex, texCoord).rgb;
    vec3 right = texture2D(tex, texCoord + vec2(1.0 / texSize.x, 0.0)).rgb;
    vec3 bottomLeft = texture2D(tex, texCoord + vec2(-1.0 / texSize.x, 1.0 / texSize.y)).rgb;
    vec3 bottom = texture2D(tex, texCoord + vec2(0.0, 1.0 / texSize.y)).rgb;
    vec3 bottomRight = texture2D(tex, texCoord + vec2(1.0 / texSize.x, 1.0 / texSize.y)).rgb;

    // Apply Sobel operator
    float sobelX = topLeft.r + 2.0 * left.r + bottomLeft.r - topRight.r - 2.0 * right.r - bottomRight.r;
    float sobelY = topLeft.r + 2.0 * top.r + topRight.r - bottomLeft.r - 2.0 * bottom.r - bottomRight.r;

    // Compute gradient magnitude and direction
    float magnitude = sqrt(sobelX * sobelX + sobelY * sobelY);
    float direction = atan(sobelY, sobelX);

    // Apply non-maximum suppression
    float edgeValue = 0.0;
    if (direction > -PI / 8.0 && direction <= PI / 8.0) {
        edgeValue = (magnitude > center.r && magnitude > right.r) ? 1.0 : 0.0;
    } else if (direction > PI / 8.0 && direction <= 3.0 * PI / 8.0) {
        edgeValue = (magnitude > center.r && magnitude > topRight.r) ? 1.0 : 0.0;
    } else if (direction > 3.0 * PI / 8.0 || direction <= -3.0 * PI / 8.0) {
        edgeValue = (magnitude > center.r && magnitude > top.r) ? 1.0 : 0.0;
    } else if (direction > -3.0 * PI / 8.0 && direction <= -PI / 8.0) {
        edgeValue = (magnitude > center.r && magnitude > topLeft.r) ? 1.0 : 0.0;
    }

    // Apply hysteresis thresholding
    if (edgeValue > .1 && edgeValue < 8.1) {
    gl_FragColor = vec4(edgeValue,edgeValue,edgeValue,1);
    } else {
    gl_FragColor = texture2D(tex,v_texcoord);
    }
}
"
'''

#fragment_shader = fragment_shader_src

fragment_shader = frag_shader_text


if len(sys.argv) > 1:
    viddev="/dev/video"+ str(sys.argv[1])
    width = str(sys.argv[2])
    height = str(sys.argv[3])
else:
    viddev = "/dev/video0"
    width = str(640)
    height = str(480)

#pipeline_str = "v4l2src ! video/x-raw,width=640,height=480 ! videoconvert ! glupload ! glcolorconvert ! gleffects_laplacian ! gleffects_heat ! gldownload ! videoconvert ! autovideosink"

#pipeline_str = "v4l2src device=" + viddev + " ! video/x-raw,width=640,height=480 ! videoconvert ! glupload ! glcolorconvert ! glshader name=shadder fragment= " + fragment_shader + " ! gldownload ! videoconvert ! autovideosink"


pipeline_str = "v4l2src device=" + viddev + " ! video/x-raw,width=" + width +",height=" + height + " ! videoconvert ! glupload ! glcolorconvert ! glshader name=shadder fragment= " + fragment_shader + " ! gldownload ! videoconvert ! autovideosink"

#pipeline_str = "v4l2src latency=100 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! glupload ! glcolorconvert ! glshader name=shadder fragment= " + fragment_shader + " ! gldownload ! videoconvert ! autovideosink"

pipeline = Gst.parse_launch(pipeline_str)
pipeline.set_state(Gst.State.PLAYING)
#print (pipeline_str)

# Run the GStreamer main loop
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)
