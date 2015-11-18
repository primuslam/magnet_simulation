import math
import copy

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from coordinate_transform import *


class MagneticCharge:
    '''
    A single point magnetic charge is defined by a coordinate and a magnitude. 
    It induces field according to the inverse square law on distance from it.
    '''
    mu_naught = 4*math.pi*10**-7
    multiplier = 1/(4*math.pi*mu_naught)
    def __init__(self, coordinate, magnitude):
        self.c = coordinate
        self.m = magnitude
    
    def field_at(self, coordinate):
        dc = coordinate - self.c
        r = np.linalg.norm(dc)
        return dc*self.m*self.multiplier/r**3
        

    def rotate(self, P, V, theta):
        '''
        Returns a new magnetic charge with the same magnitude rotated around
        the axis defined by a point P and a vector V by angle theta
        '''
        C = self.c
        
        # three transformations put the axis into a convenient basis for rotation
        # (1) translate the system so that the point P is on the origin
        C = translate(C, -P)
        
        # (2) rotate the system around the Z axis so the vector of rotation lies in the XZ plane 
        rot2 = False
        if V[0] != 0 or V[1] != 0:
            rot2 = True
            denorm = np.linalg.norm(V[:2])
            cos_2 = (V/denorm)[0]
            sin_2 = -(V/denorm)[1]
            C = rotate_z(C, cos_2, sin_2)
            V = rotate_z(V, cos_2, sin_2)

        # (3) rotate the system around the Y axis so the vector of rotation is in the positive Z direction
        denorm = np.linalg.norm([V[0], V[2]])
        cos_3 = (V/denorm)[2]
        sin_3 = -(V/denorm)[0]
        C = rotate_y(C, cos_3, sin_3)
        V = rotate_y(V, cos_3, sin_3) 
        
        # now we can rotate by the given theta
        C = rotate_z(C, theta=theta)
        
        #undo each transformation 
        C = rotate_y(C, cos_3, -sin_3)
        V = rotate_y(V, cos_3, -sin_3) 
        if rot2:
            C = rotate_z(C, cos_2, -sin_2)
            V = rotate_z(V, cos_2, -sin_2)
        C = translate(C, P)

        return MagneticCharge(C, self.m)
        
    def __str__(self):
        return "{} at {}".format(self.m, self.c)
    def __repr__(self):
        return "MagneticCharge({}, {})".format(self.c, self.m)
    

class Magnet:
    '''        
    A distribution of magnetic charges which are fixed in relative position is referred to as a magnet.
    Ideally, the net magnitude of positive and negative charges within a magnet is zero, as there are no
    magnetic monopoles, but this condition is not enforced; it is up to methods in magnet_shapes, which 
    initialize specific magnet geometries, to distribute charges appropriately
    '''
    def __init__(self, charges, color='b'):
        self.charges = np.array([])
        self.color = color
        for charge in charges:
            self.charges = np.append(self.charges, charge)
            
    def copy(self):
        return Magnet(self.charges, self.color)
    
    def field_at(self, coordinate):
        output = np.array([0, 0, 0])
        for charge in self.charges:
            output = output + charge.field_at(coordinate)
        return output
        
    def force_on(self, other):
        output = np.array([0, 0, 0])
        for charge in other.charges:
            output = output + charge.m*self.field_at(charge.c)
        return output
    
    def rotate(self, P, V, theta):
        charges = np.array([]);
        for charge in self.charges:
            charges = np.append(charges, charge.rotate(P, V, theta))
        # retval = Magnet.copy(self)
        self.charges = charges
        return self
        
    def invert(self):
        for charge in self.charges:
            charge.m = -charge.m
        return self
        
    def size(self):
        return len(self.charges)
   
    def __add__(self, other):
        self.charges = np.append(self.charges, other.charges)
        return self
        
    def __str__(self):
        return str(self.charges)
    
def plot_magnet(magnets, max_range = .03):
    '''
    Helper method uses MatPlotLib and Axes3D to visualize the distribution of charges in 3d space. 
    '''   
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    n = 100
    for magnet in magnets:
        c, m = (magnet.color, 'o')
        xs = np.array([])
        ys = np.array([])
        zs = np.array([])
        for charge in magnet.charges:
            xs = np.append(xs, charge.c[0])
            ys = np.append(ys, charge.c[1])
            zs = np.append(zs, charge.c[2])
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlim(0 - max_range, 0 + max_range)
    ax.set_ylim(0 - max_range, 0 + max_range)
    ax.set_zlim(0 - max_range, 0 + max_range)
        
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')

    plt.show()
