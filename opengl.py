import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from ctypes import sizeof, c_float, c_void_p


vao, vbo = 0, 0
shader_program = None


def init():
    global vao, vbo
    global shader_program
    vertex_shader = shaders.compileShader("""
               #version 330
               layout(location = 0) in vec2 pos;
               layout(location = 1) in vec2 uvIn;
               out vec2 uv;
               void main() {
                   gl_Position = vec4(pos, 0, 1);
                   uv = uvIn;
               }
               """, GL_VERTEX_SHADER)

    fragment_shader = shaders.compileShader("""
               #version 330
               out vec4 fragColor;
               in vec2 uv;
               uniform sampler2D tex;
               void main() {
                   fragColor = texture(tex, uv);
               }
           """, GL_FRAGMENT_SHADER)

    shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
    glEnableClientState(GL_VERTEX_ARRAY)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 4, c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 4, c_void_p(2 * sizeof(c_float)))
    glEnableVertexAttribArray(1)

    glUseProgram(shader_program)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)


