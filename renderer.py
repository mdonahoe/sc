import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import pygame
import random
import sys
import time


class Renderer(object):
    def __init__(self):
        self.vertex_shader_prog = """
            varying vec4 v;
            varying vec3 N;

            void main(void)
            {

               v = gl_ModelViewMatrix * gl_Vertex;
               N = gl_NormalMatrix * gl_Normal;

               gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;

            }
        """
        self.fragment_shader_prog = """
            varying vec3 N;
            varying vec4 v;

            void main(void)
            {
               vec4 L4 = gl_LightSource[0].position.xyzz-v;
               vec3 L = L4.xyz;

               // "Lambert's law"? (see notes)
               // Rather: faces will appear dimmer when struck in an acute angle
               // distance attenuation

               float Idiff = max(dot(normalize(L),N),0.0)*pow(length(L),-2.0);

               gl_FragColor = vec4(0.5,0,0.0,1.0)+ // purple
                              vec4(1.0,1.0,1.0,1.0)*Idiff; // diffuse reflection
            }
        """
        self.block_list = 0
        self.next_list = 1
        self.t = 0

    def init(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 200)
        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        glEnable(GL_DEPTH_TEST)

        # Create and Compile fragment and vertex shaders
        # Transfer data from fragment to vertex shader
        vertex_shader = create_and_compile_shader(GL_VERTEX_SHADER, self.vertex_shader_prog)

        fragment_shader = create_and_compile_shader(GL_FRAGMENT_SHADER, self.fragment_shader_prog)

        # build shader program
        program = glCreateProgram()
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)

        # try to activate/enable shader program
        # handle errors wisely
        try:
            glUseProgram(program)
        except OpenGL.error.GLError:
            print glGetProgramInfoLog(program)

        self.init_block_list()

    def init_block_list(self):
        self.block_list = self.next_list
        self.next_list += 1
        # load a block into a display list

        glNewList(self.block_list, GL_COMPILE)

        glBegin(GL_QUADS)

        glColor3f(1,1,1)

        glNormal3f(0, 0, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f(-1,  1, -1)

        glNormal3f(0, 0, 1)
        glVertex3f(-1, -1,  1)
        glVertex3f( 1, -1,  1)
        glVertex3f( 1,  1,  1)
        glVertex3f(-1,  1,  1)

        glNormal3f(0, -1, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1, -1,  1)
        glVertex3f(-1, -1,  1)

        glNormal3f(0, 1, 0)
        glVertex3f(-1,  1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f( 1,  1,  1)
        glVertex3f(-1,  1,  1)

        glNormal3f(-1, 0, 0)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1,  1, -1)
        glVertex3f(-1,  1,  1)
        glVertex3f(-1, -1,  1)

        glNormal3f(1, 0, 0)
        glVertex3f( 1, -1, -1)
        glVertex3f( 1,  1, -1)
        glVertex3f( 1,  1,  1)
        glVertex3f( 1, -1,  1)

        glEnd()
        glEndList()

    def render(self, player, world):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1, 0.01, 1000)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)

        # calculate light source position
        self.t += 1
        ld = [math.sin(self.t / 16.0) * 4.0,
              math.sin(self.t / 20.0) * 4.0,
              math.cos(self.t / 16.0) * 4.0]

        # pass data to fragment shader
        glLightfv(GL_LIGHT0, GL_POSITION, [ld[0], ld[1], ld[2]]);

        # fallback
        glColor3f(1, 1, 1)

        # move the camera
        glLoadIdentity()
        glRotatef(-player.phi, 1, 0, 0)
        glRotatef(-player.theta, 0, 1, 0)
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])

        # render a pretty range of blocks
        #blocks = [(1, 2, 3), (1, 1, 2), (1, 2, 2), (-1, -1, -1), (-5, 0, 0)]
        for block in world:
            glPushMatrix()
            glTranslate(block[0], block[1], block[2])
            glCallList(self.block_list)
            glPopMatrix()

        pygame.display.flip()

# Create and Compile a shader
# but fail with a meaningful message if something goes wrong
def create_and_compile_shader(type,source):
    shader = glCreateShader(type)
    glShaderSource(shader,source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with
    # an exception in case of syntax errors

    result = glGetShaderiv(shader,GL_COMPILE_STATUS)

    if (result != 1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n" +
                        glGetShaderInfoLog(shader))
    return shader


