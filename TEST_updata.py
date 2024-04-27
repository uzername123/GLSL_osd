#!/usr/bin/python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib


Gst.debug_set_active(True)
Gst.debug_set_default_threshold(3)

# Initialize GStreamer
Gst.init(None)

# Create a GStreamer pipeline
pipeline = Gst.parse_launch("videotestsrc ! glupload ! glshader update-shader=True name=glshader ! glimagesink")

# Get the glshader element from the pipeline
glshader = pipeline.get_by_name("glshader")

# Set the initial GLSL shader source code
initial_shader_code = """
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
//   gl_FragColor = texture2D( tex, v_texcoord );
    vec2 uv = v_texcoord.xy / (1.0,1.0);
    float zoom = (0.5 + 0.3 * sin(time));
//    float zoom = 0.25;
    vec2 scaleCenter = vec2(0.5);
    uv = (uv - scaleCenter) * zoom + scaleCenter;
   gl_FragColor = texture2D( tex, uv );
}
"""
glshader.set_property("fragment", initial_shader_code)
print("Orig")

# Start the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Define a function to update the shader
def update_shader():
    updated_shader_code = """

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
   gl_FragColor = texture2D( tex, v_texcoord );
}

"""
    print("Updata")
    glshader.set_property("fragment", updated_shader_code)
    glshader.set_property("uniforms", time=1)
    glshader.set_property("update-shader", True)
#   pipeline.set_state(Gst.State.PLAYING)

    # Return False to stop the timer after updating the shader
    return False

# Schedule the shader update after 5 seconds
GLib.timeout_add_seconds(5, update_shader)

# Run the GLib main loop
main_loop = GLib.MainLoop()
main_loop.run()

# Stop the pipeline
pipeline.set_state(Gst.State.NULL)
