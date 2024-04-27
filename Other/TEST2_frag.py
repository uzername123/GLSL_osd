#!/usr/bin/python3


import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, GLib

Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

# Initialize GStreamer
Gst.init(None)

# Function to update the shader
#def update_shader():

new_fragment_shader =  '''
"
#version 100
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;

void main () {
    vec2 uv = v_texcoord.xy / (1.0,1.0);
    float zoom = (0.5 + 0.3 * sin(time));
//    float zoom = 0.25;
    vec2 scaleCenter = vec2(0.5);
    uv = (uv - scaleCenter) * zoom + scaleCenter;
   gl_FragColor = texture2D( tex, uv );
}
"
'''

new_vertex_shader = '''
"
#version 100
#ifdef GL_ES
precision mediump float;
#endif

    uniform mat4 u_transformation; 
    uniform float time;

    attribute vec4 a_position;
    attribute vec2 a_texcoord;
    varying vec2 v_texcoord;
    void main()
    {

    mat4 AAA = mat4(.5, .5, .5, 0.0,  // 1. column
                  0.1, 1, 0.1, 0.0,  // 2. column
                  0.2, 0.2, 1, 0.0,  // 3. column
                  0.0, 0.0, 0.0, 1.0); // 4. column
//       gl_Position = a_position;
	gl_Position = AAA * a_position;
       v_texcoord = a_texcoord ;
    };
"
'''


# Resume the pipeline


# Create a GStreamer pipeline
pipeline_str = "v4l2src ! video/x-raw,width=320,height=240 ! videoconvert ! glupload ! glcolorconvert ! glshader name=glshader fragment= " + new_fragment_shader + " vertex= " + new_vertex_shader + " ! gldownload name=gldownload ! glimagesink"
pipeline = Gst.parse_launch(pipeline_str)

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Wait for a moment to allow the pipeline to start
#GLib.timeout_add_seconds(5, update_shader)

# Run the GStreamer main loop
loop = GLib.MainLoop()
try:
    loop.run()
except KeyboardInterrupt:
    pipeline.set_state(Gst.State.NULL)

