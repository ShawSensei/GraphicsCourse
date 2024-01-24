import math
import random
import time
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.raw.GLU import gluPerspective

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
RAIN_PARTICLES = 1500
GRAVITY = -0.1


class Raindrop:


    def __init__(self):
        self.x = random.uniform(-1, 1)
        self.y = random.uniform(1, 2)
        self.z = random.uniform(-1, 1)
        self.velocity = random.uniform(0.01, 0.05)
        self.length = random.uniform(0.0075, 0.0015)

    def fall(self):
        self.y += GRAVITY * self.velocity
        if self.y < -1:
            self.y = random.uniform(1, 2)

    def draw(self):
        glBegin(GL_LINES)
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x, self.y + self.length, self.z)
        glEnd()

def myTranslate(x, y, z):
    matrix = np.identity(4)
    matrix[0][3] = x
    matrix[1][3] = y
    matrix[2][3] = z
    glMatrixMode(GL_MODELVIEW)
    glMultMatrixf(matrix)

def glScale(x, y, z):
    scale_matrix = np.array([[x, 0, 0, 0],
                             [0, y, 0, 0],
                             [0, 0, z, 0],
                             [0, 0, 0, 1]])
    glMultMatrixf(scale_matrix)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for raindrop in raindrops:
        raindrop.fall()
        raindrop.draw()

    glutSwapBuffers()

def idle():
    glutPostRedisplay()
    time.sleep(0.01)




# pygame.init()
# display = (800, 600)
# pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
#
# gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)


def addPixel(a, b):
    glPointSize(3)
    glBegin(GL_POINTS)
    glColor3f(1, 1, 1)
    glVertex2f(a / (800 / 2), b / (600 / 2))
    # gl.glVertex2f( a, b)
    glEnd()


glTranslatef(0.0, 0.0, -1)


def draw_points_line(x, y):
    addPixel(x, y)


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy <= 0:
            return 4
        elif dx > 0 and dy <= 0:
            return 7

    else:
        if dx >= 0 and dy > 0:
            return 1
        elif dx <= 0 and dy < 0:
            return 5
        elif dx <= 0 and dy > 0:
            return 2
        elif dx >= 0 and dy < 0:
            return 6


def c_to_Zero(x1, y1, x2, y2, zone):
    if zone == 0:

        return x1, y1, x2, y2

    elif zone == 1:

        return y1, x1, y2, x2

    elif zone == 2:

        return y1, -x1, y2, -x2
    elif zone == 3:

        return -x1, y1, -x2, y2
    elif zone == 4:

        return -x1, -y1, -x2, -y2
    elif zone == 5:

        return -y1, -x1, -y2, -x2
    elif zone == 6:

        return -y1, x1, -y2, x2
    elif zone == 7:

        return x1, -y1, x2, -y2


def zero_to_original(x1, y1, z):
    if z == 0:
        return x1, y1
    elif z == 1:
        return y1, x1
    elif z == 2:
        return -y1, x1

    elif z == 3:
        return -x1, y1
    elif z == 4:
        return -x1, -y1

    elif z == 5:
        return -y1, -x1

    elif z == 6:
        return y1, -x1

    elif z == 7:
        return x1, -y1


def mid_point_algo(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    x1, y1, x2, y2 = c_to_Zero(x1, y1, x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x = x1
    y = y1
    while (x <= x2):
        x_1, y_1 = zero_to_original(x, y, zone)
        draw_points_line(x_1, y_1)
        if (d > 0):
            d = d + incNE
            x = x + 1
            y = y + 1
        else:
            d = d + incE
            x = x + 1


def quad_maker(np_array):  # draws a quad
    s = len(np_array)
    for i in range(len(np_array)):
        inc = (i + 1) % s
        mid_point_algo(np_array[i][0], np_array[i][1], np_array[inc][0], np_array[inc][1])


def midpoint_maker(test_box):
    x = 0
    y = 0
    for i in range(len(test_box)):
        x += test_box[i][0]
        y += test_box[i][1]
    x = x / len(test_box)
    y = y / len(test_box)
    return np.array([[x, y, 1]])


def translation(midpoint, new_x, new_y):
    t_x = new_x - midpoint[0][0]
    t_y = new_y - midpoint[0][1]
    translation_mat = np.empty((0, 3), float)
    # print(midpoint,True)
    translation_mat = np.append(translation_mat, np.array([[1, 0, t_x]]), axis=0)
    translation_mat = np.append(translation_mat, np.array([[0, 1, t_y]]), axis=0)
    translation_mat = np.append(translation_mat, np.array([[0, 0, 1]]), axis=0)
    # print(translation_mat)
    return translation_mat


def new_quad(old_quad, transfomation_mat):
    empt_array = np.empty((0, 2), float)
    for i in old_quad:
        mew_arr = np.empty((0, 1), float)
        mew_arr = np.append(mew_arr, np.array([[i[0]]]), axis=0)
        mew_arr = np.append(mew_arr, np.array([[i[1]]]), axis=0)
        mew_arr = np.append(mew_arr, np.array([[1]]), axis=0)
        resultant = np.matmul(transfomation_mat, mew_arr)
        # print(resultant[0][0],"Alhamdulillah")
        empt_array = np.append(empt_array, [[resultant[0][0], resultant[1][0]]], axis=0)
    return empt_array


def execute_translation(test_box, x, y):
    test_box_mid_point = midpoint_maker(test_box)
    c = translation(test_box_mid_point, x, y)
    transformed_test_box = new_quad(test_box, c)
    return transformed_test_box


def scale(sc):
    s = np.array([[sc, 0, 0],
                  [0, sc, 0],
                  [0, 0, 1]])

    return s


def execute_scaling(test_box, sc):
    test_box_mid_point = midpoint_maker(test_box)
    c = translation(test_box_mid_point, 0, 0)  # translate to 0,0
    r = scale(sc)
    r_c = np.matmul(r, c)
    re_sc = translation(np.array([[0, 0]]), test_box_mid_point[0][0], test_box_mid_point[0][1])  # back translate
    r_crc = np.matmul(re_sc, r_c)
    transformed_test_box = new_quad(test_box, r_crc)
    return transformed_test_box


# def movingBoat(translated1,y):


test_box = np.array(
    [[-15, 0], [15, 0], [20, 10], [8, 10], [13, 13], [6, 17], [6, 10], [0, 10], [0, 25], [-9, 17], [-5, 10], [-20, 10]])
scaled_1 = execute_scaling(test_box, .7)
scaled_2 = execute_scaling(test_box, 1.5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # translated1=execute_translation(test_box,-200,-50)
    # quad_maker(translated1)
    # addPixel(2200,1230)
    # addPixel(200,100)
    # addPixel(0,0)
    # movingBoat(test_box,-50)
    # quad_maker(np.array([[-300,0],[300,0]]))
    for i in range(-200, 200, 5):
        quad_maker(np.array([[-300, 0], [300, 0]]))
        quad_maker(execute_translation(scaled_1, i + 20, -20))
        quad_maker(execute_translation(scaled_2, i, -50))
        pygame.display.flip()
        pygame.time.wait(40)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # pygame.display.flip()
    # pygame.time.wait(100)
    # glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Rain Animation")

glClearColor(0.0, 0.0, 0.0, 0.0)
glEnable(GL_DEPTH_TEST)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(60.0, float(WINDOW_WIDTH) / WINDOW_HEIGHT, 0.1, 100.0)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
myTranslate(0.0, 0.0, -5.0)
print("Please enter the scaling amount")
x=input("x=")

y=input("y=")

glScale(x, y, 1.0)  # Scale the object by 2 along the x-axis, 1.5 along the y-axis

raindrops = [Raindrop() for i in range(RAIN_PARTICLES)]

glutDisplayFunc(display)
glutIdleFunc(idle)

glutMainLoop()