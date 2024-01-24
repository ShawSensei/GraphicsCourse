from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_points(x, y):
  glPointSize(5) #pixel size. by default 1 thake
  glBegin(GL_POINTS)
  glVertex2f(x,y) #jekhane show korbe pixel
  glEnd()

def find_zone(dx, dy):
  if (dx >= 0 and dy >= 0):
      if (abs(dx) >= abs(dy)):
          return 0
      else:
          return 1

  elif (dx < 0 and dy >= 0):
      if (abs(dx) < abs(dy)):
          return 2
      else:
          return 3

  elif (dx < 0 and dy < 0):
      if (abs(dx) >= abs(dy)):
          return 4
      else:
          return 5

  else:
      if abs(dx) < abs(dy):
          return 6
      else:
          return 7

def convert_to_zone0(x1, y1, x2, y2, zone):
  a = 0
  b = 0
  c = 0
  d = 0

  if zone == 0:
      a = x1
      b = y1
      c = x2
      d = y2

  elif zone == 1:
      a = y1
      b = x1
      c = y2
      d = x2

  elif zone == 2:
      a = y1
      b = -x1
      c = y2
      d = -x2

  elif zone == 3:
      a = -x1
      b = y1
      c = -x2
      d = y2

  elif zone == 4:
      a = -x1
      b = -y1
      c = -x2
      d = -y2

  elif zone == 5:
      a = -y1
      b = -x1
      c = -y2
      d = -x2

  elif zone == 6:
      a = -y1
      b = x1
      c = -y2
      d = x2

  elif zone == 7:
      a = x1
      b = -y1
      c = x2
      d = -y2

  return a, b, c, d

def midpoint(x1, y1, x2, y2):
  dx = x2 - x1
  dy = y2 - y1
  zone = find_zone(dx, dy)

  x1, y1, x2, y2 = convert_to_zone0(x1, y1, x2, y2, zone)

  dx = x2 - x1
  dy = y2 - y1
  D = 2 * dy - dx
  dNE = 2 * (dy - dx)
  dE = 2 * dy

  x = x1
  y = y1
  while x <= x2:
      a = x
      b = y
      a, b = convert_to_origin_zone(a, b, zone)
      draw_points(a, b)

      x = x + 1
      if D > 0:
          D = D + dNE
          y = y + 1
      else:
          D = D + dE

def convert_to_origin_zone(x, y, zone):
  if zone == 0:
      return x, y

  if zone == 1:
      return y, x

  if zone == 2:
      return -y, x

  if zone == 3:
      return -x, y

  if zone == 4:
      return -x, -y

  if zone == 5:
      return -y, -x

  if zone == 6:
      return y, -x

  if zone == 7:
      return x, -y


def iterate():
  glViewport(0, 0, 500, 500)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
  glMatrixMode (GL_MODELVIEW)
  glLoadIdentity()

def showScreen():
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
  glLoadIdentity()
  iterate()
  #glColor3f(0.0, 102/255, 51/255) #konokichur color set (RGB)
  #call the draw methods here

  #Chrismas tree
  glColor3f(102/255, 51/255, 0)
  midpoint(200, 150, 200, 50)
  glColor3f(0.0, 102 / 255, 51 / 255)
  for i in range(0,100):
      midpoint(100+i, 200+i, 200, 400-i)
      midpoint(200,400-i,300-i,200+i)
      midpoint(300-i,200+i,100+i,200+i)
  for i in range(0,100):
      midpoint(100+i, 150+i, 200, 300-i)
      midpoint(200,300-i,300-i,150+i)
      midpoint(300-i,150+i,100+i,150+i)
  glColor3f(1,1,1)


  for i in range(0,20):
      midpoint(100-i,200,200,400+i)
      midpoint(200,400+i,300+i,200)

      #midpoint()
  glutSwapBuffers()




glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()