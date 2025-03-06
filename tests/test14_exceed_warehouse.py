"""
Test #14: Attempt a BUY that partially uses warehouse, 
but the warehouse doesn't have quite enough to top it up fully => fails.
"""

import unittest
from rack import Rack
from transactions import buy_gold

class Test14ExceedWarehouse(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(20, 5)  # capacity=20, quantity=5
        # 2 small out racks
        self.out_racks = [
            Rack(10, 3),
            Rack(8, 4)
        ]
        # in racks with enough capacity
        self.in_racks = [
            Rack(20, 10)
        ]

    def test_exceed_warehouse(self):
        # total out racks have 7 gm => warehouse has 5 => total 12
        # we want 15 => not enough => fail
        amount = 15.0
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertFalse(success, "Should fail because out racks + warehouse total only 12 gm.")

if __name__ == '__main__':
    unittest.main()