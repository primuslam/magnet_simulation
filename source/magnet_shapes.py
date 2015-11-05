import math
import numpy as np
from magnet_define import *

#Constants for accuracy and runtime parameters
DENSITY = 4
SLICES = 5


class ring_magnet(magnet):
    def __init__(self, center, r1, r2, m, b, **kwargs):
        magnet.__init__(self, np.array([]), **kwargs)
        theta = 2*math.pi/m
        area = math.pi*(r1**2 - r2**2)/m
        magnitude = b*area
        r_prime = 0.5*(r1+r2)
        for i in range(m):
            coordinate = center + np.array([r_prime*math.cos(i*theta), r_prime*math.sin(i*theta), 0])
            self.charges = np.append(self.charges, magnetic_charge(coordinate, magnitude))

class disk_magnet(magnet):
    def __init__(self, center, r1, r2, n, b, **kwargs):
        magnet.__init__(self, np.array([]), **kwargs)
        thickness = (r2-r1)/n
        for i in range(n):
            self.charges = np.append(self.charges, ring_magnet(center, r1+i*thickness, r1+(i+1)*thickness, DENSITY*(i+4), b).charges)

class cylinder_magnet(magnet):
    def __init__(self, center, radius, h, b, **kwargs):
        magnet.__init__(self, np.array([]), **kwargs)
        top = disk_magnet(center, 0, radius, SLICES, b)
        bot = disk_magnet(center + [0, 0, -h], 0, radius, SLICES, -b)
        mag = top + bot
        self.charges = mag.charges
        
class rectangle_magnet(magnet):
    def __init__(self, b, corner, width, length, **kwargs):
        magnet.__init__(self, np.array([]), **kwargs)
        x = width/(4*DENSITY)
        y = length/(4*DENSITY)
        area = x*y
        magnitude = b*area
        for i in range(4*DENSITY):
            for j in range(4*DENSITY):
                coordinate = corner + np.array([x/2 + i*x, y/2 + j*y, 0])
                self.charges = np.append(self.charges, magnetic_charge(coordinate, magnitude)) 