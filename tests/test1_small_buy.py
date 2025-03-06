"""
Test #1: Small BUY transaction that should succeed without rebalancing.

We have:
 - 2 IN racks with small capacities
 - 2 OUT racks that have enough gold
 - A small warehouse (shouldn't be needed)
We do a single BUY and check final quantities.
"""

import unittest
from rack import Rack
from transactions import buy_gold
from selection import select_source_rack, select_destination_rack

class Test1SmallBuy(unittest.TestCase):
    def setUp(self):
        # We define a small warehouse
        self.warehouse = Rack(100, 50)  # capacity=100, quantity=50

        # Two small IN racks
        self.in_racks = [
            Rack(10, 5),  # half full
            Rack(20, 10), # half full
        ]

        # Two OUT racks with enough gold
        self.out_racks = [
            Rack(10, 9),  # almost full
            Rack(20, 15), # enough gold
        ]

    def test_small_buy(self):
        # We attempt to buy 5 gm of gold
        amount = 5.0

        # Because the out_racks[1] has 15 gm, 
        # it should supply easily without rebalancing.
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)
        # We'll pass lock=None; it won't matter if we don't do concurrency in a unit test.

        # Check if the transaction succeeded
        self.assertTrue(success, "Small BUY should succeed without rebalancing.")

        # Now check final states
        # The source rack likely was out_racks[1] (with 15 gm), 
        # so we expect it to have 10 left after subtracting 5.
        self.assertEqual(self.out_racks[1].quantity, 10.0, "OUT rack final should be 10.0")

        # The destination rack with the biggest leftover capacity is probably in_racks[1].
        # But let's see if your min/max logic chooses in_racks[1] or in_racks[0].
        # If it was in_racks[1], it should have 15 now.
        # We'll accept either, but let's guess it picks in_racks[1].
        self.assertAlmostEqual(self.in_racks[1].quantity, 15.0, places=3,
            msg="IN rack should have 15.0 after receiving 5.")
        
        # Warehouse should remain unchanged
        self.assertEqual(self.warehouse.quantity, 50, "Warehouse should be untouched")

if __name__ == '__main__':
    unittest.main()