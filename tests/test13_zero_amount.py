"""
Test #13: Attempting a transaction of 0 amount. 
We might allow it to succeed trivially or treat it as invalid. 
We'll see how your logic handles it.
"""

import unittest
from rack import Rack
from transactions import buy_gold, sell_gold

class Test13ZeroAmount(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        self.in_racks = [Rack(10, 5)]
        self.out_racks = [Rack(10, 5)]

    def test_zero_buy(self):
        success = buy_gold(0.0, self.out_racks, self.in_racks, self.warehouse, lock=None)
        # Possibly your code passes or fails. We'll assume it passes trivially:
        self.assertTrue(success, "A 0.0 gm BUY might succeed trivially, or you might want to fail it.")
        # no change in quantity
        self.assertAlmostEqual(self.in_racks[0].quantity, 5.0)
        self.assertAlmostEqual(self.out_racks[0].quantity, 5.0)

    def test_zero_sell(self):
        success = sell_gold(0.0, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(success, "A 0.0 gm SELL might also trivially succeed.")
        self.assertAlmostEqual(self.in_racks[0].quantity, 5.0)
        self.assertAlmostEqual(self.out_racks[0].quantity, 5.0)

if __name__ == '__main__':
    unittest.main()