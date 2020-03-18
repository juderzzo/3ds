from display import *
from matrix import *
from math import *


def add_torus(coords, cx, cy, cz, r0, r1, interval):
    region = torusH(cx, cy, cz, r0, r1, interval)
    for point in region:
        x0 = point[0]
        y0 = point[1]
        z0 = point[2]
        x1 = x0 + 1
        y1 = y0
        z1 = z0
        add_edge(coords, x0, y0, z0, x1, y1, z1)

def torusH(cx, cy, cz, r0, r1, interval):
    region = []
    theta_interval = 1.0
    while theta_interval <= interval:
        phi_interval = 1.0
        theta = 2 * math.pi * (theta_interval / interval)
        while phi_interval <= interval:
            phi = 2 * math.pi * (phi_interval / interval)
            x = (((r0 * math.cos(theta)) + r1) * math.cos(phi)) + cx
            y = (r0 * math.sin(theta)) + cy
            z = (((r0 * math.cos(theta)) + r1) * -1 * math.sin(phi)) + cz
            region.append([x, y, z])
            phi_interval += 1.0
        theta_interval += 1.0
    return region

def add_box(coords, x, y, z, width, height, depth):
    ##Gotta add every single change in x and every single change in y
    add_edge(coords, x, y-height, z, x+width, y-height, z)
    add_edge(coords, x, y-height, z, x, y-height, z-depth)
    add_edge(coords, x, y, z, x+width, y, z)
    add_edge(coords, x, y, z, x, y-height, z)
    add_edge(coords, x, y, z-depth, x, y-height, z-depth)
    add_edge(coords, x, y, z-depth, x+width, y, z-depth)
    add_edge(coords, x, y, z, x, y, z-depth)
    add_edge(coords, x+width, y, z, x+width, y-height, z)
    add_edge(coords, x+width, y, z, x+width, y, z-depth)
    add_edge(coords, x+width, y-height, z, x+width, y-height, z-depth)
    add_edge(coords, x+width, y-height, z-depth, x, y-height, z-depth)
    add_edge(coords, x+width, y-height, z-depth, x+width, y, z-depth)




def add_sphere(coords, x, y, z, radius, interval ):
    region = sphereH(x, y, z, radius, interval)
    for point in region:
        x0 = point[0]
        y0 = point[1]
        z0 = point[2]
        x1 = x0 + 1
        y1 = y0
        z1 = z0
        add_edge(coords, x0, y0, z0, x1, y1, z1)


def sphereH(cx, cy, cz, radius, interval):
    region = []
    theta_interval = 1.0
    while theta_interval <= interval:
        phi_interval = 1.0
        theta = 2 * math.pi * (theta_interval / interval)
        while phi_interval <= interval:
            phi = math.pi * (phi_interval / interval)
            x = radius * math.cos(theta) + cx
            y = radius * math.sin(theta) * math.cos(phi) + cy
            z = radius * math.sin(theta) * math.sin(phi) + cz
            region.append([x, y, z])
            phi_interval += 1.0
        theta_interval += 1.0
    return region



## from b4



def add_circle(coords, cx, cy, cz, r, interval):
    x0 = r + cx
    y0 = cy
    i = 1
    while i <= interval:
        t = float(i)/interval
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;
        add_edge(coords, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( coords, x0, y0, x1, y1, x2, y2, x3, y3, interval, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= interval:
        t = float(i)/interval
        x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(coords, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1

def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print 'Need at least 2 coords to draw'
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



##line fro mb4
def draw_line( x0, y0, x1, y1, screen, color ):

    #swap coords if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
