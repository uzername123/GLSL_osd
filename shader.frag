//#version 330 core
#version 100
#ifdef GL_ES
precision mediump float;
#endif
#extension GL_ARB_shading_language_420pack: enable


uniform sampler2D inputTexture; // The input black and white texture
uniform sampler2D paletteTexture; // The palette texture

varying vec2 v_texcoord;
uniform sampler2D tex;
uniform float time;
uniform float width;
uniform float height;

//in vec2 TexCoords;
//out vec4 FragColor;

void main()
{
   gl_FragColor = texture2D( tex, v_texcoord );
    vec2 uv = v_texcoord.xy / (1.0,1.0);

    // Sample the grayscale value from the input texture
    float grayValue = texture(tex, v_texcoord).r;

    // Sample the color from the palette texture
    vec3 color = texture(paletteTexture, vec2(grayValue, 0.5)).rgb;

    // Output the color
    FragColor = vec4(color, 1.0);
//    gl_FragColor = texture2D( tex, uv );
}



//void main () {
//   gl_FragColor = texture2D( tex, v_texcoord );
//    vec2 uv = v_texcoord.xy / (1.0,1.0);
//    float zoom = (0.5 + 0.2 * sin(time));
//    float zoom = 0.25;
//    vec2 scaleCenter = vec2(0.5);
//    uv = (uv - scaleCenter) * zoom + scaleCenter;
   gl_FragColor = texture2D( tex, uv );

}

