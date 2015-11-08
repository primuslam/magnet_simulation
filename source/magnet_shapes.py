import math

import numpy as np
from magnet_define import *

#Constants for accuracy and runtime parameters


class MagnetRing(Magnet):
    def __init__(self, center, r1, r2, b, density=5, **kwargs):
        Magnet.__init__(self, np.array([]), **kwargs)
        theta = 2*math.pi/density
        area = math.pi*(r1**2 - r2**2)/density
        magnitude = b*area
        r_prime = 0.5*(r1+r2)
        for i in range(density):
            coordinate = center + np.array([r_prime*math.cos(i*theta), r_prime*math.sin(i*theta), 0])
            self.charges = np.append(self.charges, MagneticCharge(coordinate, magnitude))

class MagnetDisk(Magnet):
    def __init__(self, center, r1, r2, b, density=5, **kwargs):
        Magnet.__init__(self, np.array([]), **kwargs)
        thickness = (r2-r1)/density
        for i in range(density):
            self.charges = np.append(self.charges, MagnetRing(center, r1+i*thickness, r1+(i+1)*thickness, b, int(math.sqrt(density))*(i+1)).charges)

class MagnetCylinder(Magnet):
    def __init__(self, center, radius, h, b, density=5, **kwargs):
        Magnet.__init__(self, np.array([]), **kwargs)
        top = MagnetDisk(center, 0, radius, b, density)
        bot = MagnetDisk(center + [0, 0, -h], 0, radius, -b, density)
        mag = top + bot
        self.charges = mag.charges
        
class MagnetRectangle(Magnet):
    def __init__(self, b, corner, width, length, DENSITY=5, **kwargs):
        Magnet.__init__(self, np.array([]), **kwargs)
        x = width/(4*DENSITY)
        y = length/(4*DENSITY)
        area = x*y
        magnitude = b*area
        for i in range(4*DENSITY):
            for j in range(4*DENSITY):
                coordinate = corner + np.array([x/2 + i*x, y/2 + j*y, 0])
                self.charges = np.append(self.charges, MagneticCharge(coordinate, magnitude)) 