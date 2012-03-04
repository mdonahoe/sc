import math
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import os
import Image
import pygame
import random
import sys
import time


class Renderer(object):
    def __init__(self):
        self.vertex_shader_prog = """
            varying vec4 v;
            varying vec3 N;
            varying vec2 texcoord;

            uniform vec2 textureOffset;

            void main(void)
            {

               v = gl_ModelViewMatrix * gl_Vertex;
               N = gl_NormalMatrix * gl_Normal;

               gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
               texcoord = (gl_MultiTexCoord0.xy + textureOffset) / 16.0;


            }
        """

        self.fragment_shader_prog = """
            uniform sampler2D atlas;
            varying vec3 N;
            varying vec4 v;
            varying vec2 texcoord;

            void main(void)
            {
               vec4 L4 = gl_LightSource[0].position.xyzz-v;
               vec3 L = L4.xyz;

               // "Lambert's law"? (see notes)
               // Rather: faces will appear dimmer when struck in an acute angle
               // distance attenuation

               float Idiff = max(dot(normalize(L),N),0.0)*pow(length(L),-2.0);

               gl_FragColor = texture2D(atlas, texcoord) +
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
        self.blocktexture = loadImage('terrain.png')
        self.textureOffset = glGetUniformLocation(program, "textureOffset") #make the uniform name
        # textureOffset lets us use the single terrain images for all our blocks
        # the shader calculates the texture coordinates based on the offset

        # try to activate/enable shader program
        # handle errors wisely

        self.init_block_list()
        try:
            glUseProgram(program)
        except OpenGL.error.GLError:
            print glGetProgramInfoLog(program)

    def init_block_list(self):
        self.block_list = self.next_list
        self.next_list += 1
        # load a block into a display list

        glNewList(self.block_list, GL_COMPILE)

        glBegin(GL_QUADS)

        glColor3f(1,1,0)

        glNormal3f(0, 0, 1)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);

        glNormal3f(-1, 0, 0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);

        glNormal3f(0, 1, 0)
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);

        glNormal3f(0, 0, -1)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);

        glNormal3f(1, 0, 0)
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);

        glNormal(0, -1, 0)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);

        glEnd()
        glEndList()

    def render(self, player, blocks, players):
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
        #glLightfv(GL_LIGHT0, GL_POSITION, [-1*i for i in player.pos]);
        glLightfv(GL_LIGHT0, GL_POSITION, [ld[0], ld[1], ld[2]]);

        # fallback

        # move the camera
        glLoadIdentity()
        glRotatef(-player.phi, 1, 0, 0)
        glRotatef(-player.theta, 0, 1, 0)
        glTranslatef(-player.pos[0], -player.pos[1], -player.pos[2])

        # render a pretty range of blocks
        #blocks = [(1, 2, 3), (1, 1, 2), (1, 2, 2), (-1, -1, -1), (-5, 0, 0)]


        setupTexture(self.blocktexture)
        glUniform2fv(self.textureOffset, 1, [2,15])
        for block in blocks:
            glPushMatrix()
            glTranslate(block[0], block[1], block[2])
            glScalef(0.5, 0.5, 0.5)
            glCallList(self.block_list)
            glPopMatrix()

        glUniform2fv(self.textureOffset, 1, [2,12])
        for other in players:
            if player == other: continue
            glPushMatrix()
            draw_player_model(other)
            glPopMatrix()
        glDisable(GL_TEXTURE_2D)

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

def draw_player_model(player):
    x,y,z = player.pos
    glTranslate(x,y,z)
    glRotate(player.phi, 1, 0, 0)
    glRotate(player.theta, 0, 1, 0)
    drawCube()

def loadImage(imageName = "nehe_wall.bmp" ):
    """Load an image file as a 2D texture using PIL

    This method combines all of the functionality required to
    load the image with PIL, convert it to a format compatible
    with PyOpenGL, generate the texture ID, and store the image
    data under that texture ID.

    Note: only the ID is returned, no reference to the image object
    or the string data is stored in user space, the data is only
    present within the OpenGL engine after this call exits.
    """
    im = Image.open(imageName)
    try:
        # get image meta-data (dimensions) and data
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
    except SystemError:
        # has no alpha channel, synthesize one, see the
        # texture module for more realistic handling
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
    # generate a texture ID
    ID = glGenTextures(1)
    # make it current
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    # copy the texture into the current texture ID
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    # return the ID for use
    return ID

def drawCube():
    """Draw a cube with texture coordinates"""
    # do something different than a block to differentiate players from blocks
    glBegin(GL_QUADS);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);

    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);

    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);

    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);

    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);

    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
    glEnd()

def setupTexture(imageID):
    """Render-time texture environment setup

    This method encapsulates the functions required to set up
    for textured rendering.  The original tutorial made these
    calls once for the entire program.  This organization makes
    more sense if you are likely to have multiple textures.
    """
    # texture-mode setup, was global in original
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    # re-select our texture, could use other generated textures
    # if we had generated them earlier...
    glBindTexture(GL_TEXTURE_2D, imageID)
