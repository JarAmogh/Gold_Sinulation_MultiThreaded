"""
Test #2: Small SELL transaction that should succeed without rebalancing.

We have:
 - 2 IN racks that collectively have enough gold
 - 2 OUT racks with free capacity
 - We do a small SELL (e.g., 3 gm).
Expected: no rebalancing needed, transaction succeeds.
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test2SmallSell(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        self.in_racks = [
            Rack(10, 8),
            Rack(20, 5),
        ]
        self.out_racks = [
            Rack(10, 0),
            Rack(20, 10),
        ]

    def test_small_sell(self):
        amount = 3.0
        success = sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Small SELL should succeed without rebalancing.")

        # Source might be in_racks[0] which had 8 gm, leaving 5
        # Destination might be out_racks[1] or out_racks[0], 
        # but let's guess it chooses out_racks[1] if that has max remaining capacity.
        # We'll just check total correctness:
        total_in = sum(r.quantity for r in self.in_racks)
        total_out = sum(r.quantity for r in self.out_racks)
        self.assertAlmostEqual(total_in, 13.0, places=3, msg="IN racks should have lost 3 gm total.")
        self.assertAlmostEqual(total_out, 13.0, places=3, msg="OUT racks should have gained 3 gm total.")

        # Warehouse stays 50
        self.assertEqual(self.warehouse.quantity, 50)

if __name__ == '__main__':
    unittest.main()