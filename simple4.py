# import the pygame module, so you can use it
import pygame
import random
import numpy
import glm  # pip3 install pyglm
import pyassimp # pip3 install pyassimp
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# define a main function

# initialize the pygame module
pygame.init()

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

glClearColor(0.5, 1.0, 0.5, 1.0)

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
out vec3 ourColor;
uniform mat4 superMatriz;

void main()
{
  gl_Position = superMatriz * vec4(position.x, position.y, position.z, 1.0);
  ourColor = vertexColor;
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

in vec3 ourColor;

void main()
{
   fragColor = vec4(ourColor, 1);
}
"""

shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)


vertex_data = numpy.array([
    -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
     0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
     0.0,  0.5, 0.0, 0.0, 0.0, 1.0
], dtype=numpy.float32)



vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)



vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

glVertexAttribPointer(
   0,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
   3,                  # size
   GL_FLOAT,           # type
   GL_FALSE,           # normalized?
   4 * 6,              # stride
   ctypes.c_void_p(0)  # array buffer offset
)
glEnableVertexAttribArray(0)


glVertexAttribPointer(
   1,                  # attribute 0. No particular reason for 0, but must match the layout in the shader.
   3,                  # size
   GL_FLOAT,           # type
   GL_FALSE,           # normalized?
   4 * 6,              # stride
   ctypes.c_void_p(4 * 3)  # array buffer offset
)
glEnableVertexAttribArray(1)



i = glm.mat4(1)

translate = glm.translate(i, glm.vec3(0, 0, 0))
rotate = glm.rotate(i, 0, glm.vec3(0, 1, 0))
scale = glm.scale(i, glm.vec3(1, 1, 1))

model = translate * rotate * scale
view = glm.lookAt(glm.vec3(0, 0, 2), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)

superMatriz = projection * view * model

glViewport(0, 0, 800, 600)

# define a variable to control the main loop
running = True
# main loop
counter = 0
while running:
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader)

    glUniformMatrix4fv(
      glGetUniformLocation(shader, "superMatriz"),
      1,
      GL_FALSE,
      glm.value_ptr(superMatriz)
    )

    glDrawArrays(GL_TRIANGLES, 0, 3)

    pygame.display.flip()
    clock.tick(15)
    counter+=1