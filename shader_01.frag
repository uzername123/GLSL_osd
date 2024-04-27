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

