"""
Test #5: Checking 'rebalance_in_for_gold' specifically:
We want a SELL that demands more gold than any single IN rack has, so we gather from multiple racks.
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test5RebalanceIn(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        # 3 small IN racks
        self.in_racks = [
            Rack(5, 4),
            Rack(6, 3),
            Rack(10, 2)
        ]
        # 2 OUT racks that have enough capacity
        self.out_racks = [
            Rack(20, 0),
            Rack(20, 5)
        ]

    def test_rebalance_in_for_gold(self):
        # We want to sell 8 gm total. 
        # No single IN rack has 8, so we must gather from multiple racks.
        amount = 8.0
        success = sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Should succeed by gathering from multiple IN racks.")

        # Check final sums
        # original total_in was 4+3+2=9 => after selling 8 => 1 left total
        total_in = sum(r.quantity for r in self.in_racks)
        self.assertAlmostEqual(total_in, 1.0, places=3)

        # out racks gained 8 total
        total_out = sum(r.quantity for r in self.out_racks)
        # original was 0+5=5 => now 13
        self.assertAlmostEqual(total_out, 13.0, places=3)

if __name__ == '__main__':
    unittest.main()