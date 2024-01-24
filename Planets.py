import math
import random
import time
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.raw.GLU import gluPerspective


def draw_points():
    glPointSize(5)  # pixel size, by default 1
    glBegin(GL_POINTS)
    glColor3f(245 / 255, 135 / 255, 66 / 255)
    glVertex2f(420, 250)
    glEnd()


# -----------------------------------------------------------
def draw_quads():
    glBegin(GL_QUADS)
    glColor3f(50 / 255, 129 / 255, 168 / 255)
    glVertex2f(100, 200)
    glVertex2f(250, 200)
    glVertex2f(250, 100)
    glVertex2f(100, 100)

    sc = 50
    s = np.array([[sc, 0, 0], [0, sc, 0], [0, 0, 1]])

    v1 = np.array([[100], [200], [1]])
    v2 = np.array([[250], [200], [1]])
    v3 = np.array([[250], [100], [1]])
    v4 = np.array([[100], [100], [1]])

    v11 = np.matmul(s, v1)
    v22 = np.matmul(s, v2)
    v33 = np.matmul(s, v3)
    v44 = np.matmul(s, v4)

    glBegin(GL_QUADS)
    glVertex2f(v11[0][0], v11[1][0])
    glVertex2f(v22[0][0], v22[1][0])
    glVertex2f(v33[0][0], v33[1][0])
    glVertex2f(v44[0][0], v44[1][0])
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

draw_quads()
# def showScreen():
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#
#     glLoadIdentity()
#     iterate()
#     glColor3f(1.0, 1.0, 0.0)
#
    # draw_quads()
#
    # draw_points()
#     glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)  # window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")  # window name
glutDisplayFunc(draw_quads)

glutMainLoop()
