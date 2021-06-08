import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from ctypes import sizeof, c_float, c_void_p


tex_vao, tex_vbo = 0, 0
menu_vao, menu_vbo = 0, 0

tex_shader_program = None
menu_shader_program = None


def init():
    global tex_vao, tex_vbo, menu_vbo, menu_vao
    global tex_shader_program, menu_shader_program
    tex_vertex_shader = shaders.compileShader("""
               #version 330
               layout(location = 0) in vec2 pos;
               layout(location = 1) in vec2 uvIn;
               out vec2 uv;
               void main() {
                   gl_Position = vec4(pos, 0, 1);
                   uv = uvIn;
               }
               """, GL_VERTEX_SHADER)

    tex_fragment_shader = shaders.compileShader("""
               #version 330
               out vec4 fragColor;
               in vec2 uv;
               uniform sampler2D tex;
               void main() {
                   fragColor = texture(tex, uv);
               }
           """, GL_FRAGMENT_SHADER)

    menu_vertex_shader = shaders.compileShader("""
               #version 330
               layout(location = 0) in vec2 pos;
               void main() {
                   gl_Position = vec4(pos, 0, 1);
               }
               """, GL_VERTEX_SHADER)

    menu_fragment_shader = shaders.compileShader("""
               #version 330
               out vec3 fragColor;
               void main() {
                   fragColor = vec3(0, 0, 0);
               }
           """, GL_FRAGMENT_SHADER)

    tex_shader_program = shaders.compileProgram(tex_vertex_shader, tex_fragment_shader)
    menu_shader_program = shaders.compileProgram(menu_vertex_shader, menu_fragment_shader)
    glEnableClientState(GL_VERTEX_ARRAY)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    tex_vao = glGenVertexArrays(1)
    tex_vbo = glGenBuffers(1)

    glBindVertexArray(tex_vao)
    glBindBuffer(GL_ARRAY_BUFFER, tex_vbo)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 4, c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sizeof(c_float) * 4, c_void_p(2 * sizeof(c_float)))
    glEnableVertexAttribArray(1)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    vertex_data = np.array([
        -1, -1,
        1, -1,
        1, 1,
        -1, 1,
    ], np.float32)

    menu_vao = glGenVertexArrays(1)
    menu_vbo = glGenBuffers(1)

    glBindVertexArray(menu_vao)
    glBindBuffer(GL_ARRAY_BUFFER, menu_vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
