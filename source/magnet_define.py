import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

'''
A single point magnetic charge is defined by a coordinate and a magnitude. 
It induces field according to the inverse square law on distance from it.
'''
class magnetic_charge:
    mu_naught = 4*math.pi*10**-7
    multiplier = 1/(4*math.pi*mu_naught)
    def __init__(self, coordinate, magnitude):
        self.c = coordinate
        self.m = magnitude
    
    # returns a vector corresponding to the magnetic field at x, y
    def field_at(self, coordinate):
        # print("The charge is ", self, ", the target location is", "({}, {})".format(x, y))
        dc = coordinate - self.c
        r = np.linalg.norm(dc)
        return dc*self.m*self.multiplier/r**3
        
    def __str__(self):
        return "{} at {}".format(self.m, self.c)
    def __repr__(self):
        return "magnetic_charge({}, {})".format(self.c, self.m)
    
'''        
A distribution of magnetic charges which are fixed in relative position is referred to as a magnet.
Ideally, the net magnitude of positive and negative charges within a magnet is zero, as there are no
magnetic monopoles. 
'''
class magnet:
    def __init__(self, charges, color = 'b'):
        self.charges = np.array([])
        self.color = color
        for charge in charges:
            self.charges = np.append(self.charges, charge)
            
    # returns a vector corresponding to the superimposed magnetic field at x, y
    def field_at(self, coordinate):
        output = np.array([0, 0, 0])
        for charge in self.charges:
            output = output + charge.field_at(coordinate)
        return output
        
    # returns a vector corresponding to the sum of the vector forces on another magnet 
    # by summing the forces on each of its charges
    def force_on(self, other):
        output = np.array([0, 0, 0])
        for charge in other.charges:
            output = output + charge.m*self.field_at(charge.c)
        return output
        
    def __add__(self, other):
        return magnet(np.append(self.charges, other.charges))
    def __str__(self):
        return str(self.charges)

'''
Helper method uses MatPlotLib and Axes3D to visualize the distribution of charges in 3d space. 
'''      
def plot_magnet(magnets, max_range = .03):
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