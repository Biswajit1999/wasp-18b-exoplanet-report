import unittest
import numpy as np
from scripts.spectral_robustness import band_contrast, window_shift_sensitivity

class TestSpectralRobustness(unittest.TestCase):
    def setUp(self):
        self.w=np.arange(8,dtype=float)
        self.y=np.array([1,1,1,1,3,3,3,3.])
        self.s=np.ones(8)
    def test_known_contrast(self):
        a,e=band_contrast(self.w,self.y,self.s,(4,8),(0,4))
        self.assertAlmostEqual(a,2)
        self.assertAlmostEqual(e,np.sqrt(.5))
    def test_shift_zero(self):
        r=window_shift_sensitivity(self.w,self.y,self.s,(4,8),(0,4),[0])
        self.assertAlmostEqual(r[0,0],2)
    def test_error_scaling(self):
        x=band_contrast(self.w,self.y,2*self.s,(4,8),(0,4))
        self.assertAlmostEqual(x[1],2*band_contrast(self.w,self.y,self.s,(4,8),(0,4))[1])
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError): band_contrast(self.w,self.y,self.s,(3,6),(0,4))
