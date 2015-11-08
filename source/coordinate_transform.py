import math
import numpy as np

"""
A basic set of functions for applying coordinate transformations on points and vectors in 3-space
"""
PI = math.pi

def coor(*args):
    return np.array([x for x in args])
    
def translate(P, v):
    """ Translates a point P by a vector v

    >>> P = coor(1.0, 2.0, 3.0)
    >>> v = coor(-1.0, -1.0, -3.0)
    >>> translate(P, v)
    array([ 0.,  1.,  0.])
    """
    
    return P + v
    
def scale(v, c):
    """ Scales a vector v by a constant c
    
    >>> v = coor(1.0, -3.0, 5.0)
    >>> scale(v, 2)
    array([  2.,  -6.,  10.])
    """
    return c*v
    
def rotate_z(v, cos=1, sin=0, theta=None):
    """ Rotates a vector around the Z axis counterclockwise according to the angle provided
    
    >>> v = coor(2.0, 1.0, 5.0)
    >>> rotate_z(v, math.cos(PI/2), math.sin(PI/2))
    array([-1.,  2.,  5.])
    >>> rotate_z(v, math.cos(-PI/2), math.sin(-PI/2))
    array([ 1., -2.,  5.])
    >>> rotate_z(v, theta=PI/2)
    array([-1.,  2.,  5.])
    """
    if theta is not None:
        cos = math.cos(theta)
        sin = math.sin(theta)
    M = np.array([[cos, -sin, 0], [sin, cos, 0] , [0, 0, 1]])
    return M.dot(v)
    
def rotate_y(v, cos=1, sin=0, theta=None):
    """ Rotates a vector around the Y axis counterclockwise according to the angle provided
    
    >>> v = coor(2.0, 1.0, 5.0)
    >>> rotate_y(v, math.cos(PI/2), math.sin(PI/2))
    array([ 5.,  1., -2.])
    >>> rotate_y(v, math.cos(-PI/2), math.sin(-PI/2))
    array([-5.,  1.,  2.])
    >>> rotate_y(v, theta=PI/2)
    array([ 5.,  1., -2.])
    """
    if theta is not None:
        cos = math.cos(theta)
        sin = math.sin(theta)
    M = np.array([[cos, 0, sin], [0, 1, 0] , [-sin, 0, cos]])
    return M.dot(v)
    
def rotate_x(v, cos=1, sin=0, theta=None):
    """ Rotates a vector around the X axis counterclockwise according to the angle provided
    
    >>> v = coor(2.0, 1.0, 5.0)
    >>> rotate_x(v, math.cos(PI/2), math.sin(PI/2))
    array([ 2., -5.,  1.])
    >>> rotate_x(v, math.cos(-PI/2), math.sin(-PI/2))
    array([ 2.,  5., -1.])
    >>> rotate_x(v, theta=PI/2)
    array([ 2., -5.,  1.])
    """
    if theta is not None:
        cos = math.cos(theta)
        sin = math.sin(theta)
    M = np.array([[1, 0, 0], [0, cos, -sin] , [0, sin, cos]])
    return M.dot(v)