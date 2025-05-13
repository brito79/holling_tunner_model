import unittest
import numpy as np
from models.holling_tanner import HollingTannerModel

class TestHollingTannerModel(unittest.TestCase):
    def setUp(self):
        """Set up test model with default parameters"""
        self.model = HollingTannerModel()
        self.t = np.linspace(0, 10, 100)
        self.initial_conditions = [5.0, 2.0]
    
    def test_initialization(self):
        """Test model initialization with parameters"""
        params = {
            'r': 1.5,
            'K': 15.0,
            'a': 2.0,
            'h': 0.2,
            'm': 0.6,
            'c': 0.4,
            'd': 0.2
        }
        model = HollingTannerModel(**params)
        
        for param, value in params.items():
            self.assertEqual(getattr(model, param), value)
    
    def test_simulation_shape(self):
        """Test that simulation returns correct shape"""
        solution = self.model.simulate(self.initial_conditions, self.t)
        self.assertEqual(solution.shape, (len(self.t), 2))
    
    def test_zero_predator(self):
        """Test that with zero predators, prey grows logistically"""
        solution = self.model.simulate([5.0, 0.0], self.t)
        # Prey population should increase (at least initially)
        self.assertTrue(solution[1, 0] > solution[0, 0])
        # Predator population should stay zero
        self.assertTrue(np.all(solution[:, 1] == 0.0))
    
    def test_zero_prey(self):
        """Test that with zero prey, predators die out"""
        solution = self.model.simulate([0.0, 2.0], self.t)
        # Prey population should stay zero
        self.assertTrue(np.all(solution[:, 0] == 0.0))
        # Predator population should decrease
        self.assertTrue(solution[-1, 1] < solution[0, 1])

if __name__ == "__main__":
    unittest.main()