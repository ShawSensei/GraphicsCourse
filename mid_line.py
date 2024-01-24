from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
def findZone(x_1, y_1, x_2, y_2):
    
    dx = x_2 - x_1
    dy = y_2 - y_1

    if abs(dx) > abs(dy):
        if (dx > 0) and (dy > 0):
            return 0
        elif (dx < 0) and (dy > 0):
            return 3
        elif (dx < 0) and (dy < 0):
            return 4
        elif (dx > 0) and (dy < 0):
            return 7
    else:
        if (dx > 0) and (dy > 0):
            return 1
        elif (dx < 0) and (dy > 0):
            return 2
        elif (dx < 0) and (dy < 0):
            return 5
        elif (dx > 0) and (dy < 0):
            return 6
    return 0


def convertToZone0(x, y, zone):
    
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def convertFromZone0(x, y, to_zone):
    

    if to_zone == 0:
        return x, y
    elif to_zone == 1:
        return y, x
    elif to_zone == 2:
        return -y, x
    elif to_zone == 3:
        return -x, y
    elif to_zone == 4:
        return -x, -y
    elif to_zone == 5:
        return -y, -x
    elif to_zone == 6:
        return -y, x
    elif to_zone == 7:
        return x, -y

def drawLine(x1, y1 ,x2, y2):
    find_zone = findZone(x1, y1 ,x2, y2)
    
    zone_x1, zone_y1 = convertToZone0(x1, y1, find_zone)
    zone_x2, zone_y2 = convertToZone0(x2, y2, find_zone)
    
    dx = zone_x2 - zone_x1
    dy = zone_y2 - zone_y1
    
    d = 2 * dy - dx
    incNE = 2 * (dy - dx)
    incE = 2 * dy
    
    x, y = zone_x1, zone_y1
    
    while (x <= zone_x2):
        
        original_zone_x, original_zone_y   = convertFromZone0(x, y, find_zone)
        WritePixel(original_zone_x, original_zone_y)
        if d<0:
            d+=incE
        else:
            d += incNE
            y += 1
           
        x += 1
def WritePixel(x, y):
    glPointSize(2) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()
   