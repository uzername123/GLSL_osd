#version 100
#ifdef GL_ES
precision mediump float;
#endif

varying vec2 v_texcoord;
uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;

vec4 palette[5] = {
    vec4 (1.0, 0.0, 0.0, 1.0), // Red
    vec4 (0.0, 1.0, 0.0, 1.0), // Green
    vec4 (0.0, 0.0, 1.0, 1.0), // Blue
    vec4 (1.0, 1.0, 0.0, 1.0), // Yellow
    vec4 (0.0, 1.0, 1.0, 1.0)  // Cyan
};

//uniform sampler2D tex; // Input texture
//uniform vec4 palette[5]; // Custom color palette

//in vec2 texcoord;
//out vec4 outColor;

void main() {
    vec4 originalColor = texture2D(tex, v_texcoord);
    // Map the original color to a color from the custom palette
    // Example: Map red to the first color in the palette
    if (originalColor.r > 0.5) {
        gl_FragColor = texture2D(palette[0],v_texcoord);
    } else {
        gl_FragColor = texture2D(originalColor, v_texcoord);
    }
}