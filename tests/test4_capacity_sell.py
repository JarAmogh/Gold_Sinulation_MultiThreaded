"""
Test #4: SELL transaction that requires 'capacity' rebalancing in the OUT racks
because no single OUT rack can store the entire amount initially.
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test4CapacitySell(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        # 2 IN racks that have plenty of gold
        self.in_racks = [
            Rack(20, 20),
            Rack(15, 10)
        ]
        # 2 OUT racks that do not have enough free space individually to store 15 gm
        self.out_racks = [
            Rack(10, 5),  # free=5
            Rack(10, 8)   # free=2
        ]

    def test_capacity_sell(self):
        amount = 15.0
        success = sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Should succeed by rebalancing OUT racks capacity into warehouse or among themselves.")

        # Check final sums
        total_in = sum(r.quantity for r in self.in_racks)
        total_out = sum(r.quantity for r in self.out_racks)

        # They should have lost 15 total from IN racks
        prev_in = 30  # (20 + 10)
        self.assertAlmostEqual(total_in, prev_in - 15, places=3,
            msg="IN racks should have 15 less after SELL.")

        # They should have gained 15 total in OUT racks 
        prev_out = 13  # (5 + 8)
        self.assertAlmostEqual(total_out, prev_out + 15, places=3,
            msg="OUT racks should have 15 more after SELL.")

if __name__ == '__main__':
    unittest.main()