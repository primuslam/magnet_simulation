import unittest

import numpy as np

from coordinate_transform import *
from magnet_define import *
from magnet_shapes import *


class TestMagneticCharge(unittest.TestCase):
   
    def test_field(self):
        A = MagneticCharge(coor(0, 0, 0), 1)
        B = MagneticCharge(coor(1, 0, 0), 1)
        self.assertEqual(np.linalg.norm(A.field_at(coor(0, 0, 1))), np.linalg.norm(B.field_at(coor(1, 0, 1))))


if __name__ == '__main__':
    unittest.main()