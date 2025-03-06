"""
Test #8: Attempt a SELL that fails because the IN racks don't have enough gold 
(even after rebalancing among themselves).
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test8InNotEnoughGold(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        self.in_racks = [
            Rack(10, 3),
            Rack(10, 2)
        ]
        self.out_racks = [
            Rack(20, 5),
            Rack(20, 10)
        ]

    def test_in_not_enough_gold(self):
        # We want to SELL 10 gm, but total in racks is only 5 => not enough 
        # and no rebalancing can create more gold out of thin air => should fail
        amount = 10.0
        success = sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertFalse(success, "Should fail because total gold in IN racks is only 5.")

if __name__ == '__main__':
    unittest.main()

    