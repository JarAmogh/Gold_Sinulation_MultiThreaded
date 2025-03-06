"""
Test #3: BUY transaction that requires 'capacity' rebalancing in the IN racks
because no single IN rack can store the entire amount initially.
"""

import unittest
from rack import Rack
from transactions import buy_gold

class Test3CapacityBuy(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        # 2 IN racks that do NOT have enough free space individually to store 10 gm
        self.in_racks = [
            Rack(8, 5),   # capacity=8, quantity=5 => free=3
            Rack(10, 7),  # capacity=10, quantity=7 => free=3
        ]
        # 2 OUT racks with enough gold
        self.out_racks = [
            Rack(10, 10),  # full of gold
            Rack(20, 5),
        ]

    def test_capacity_buy(self):
        # We'll try to buy 10 gm, but neither rack can store 10 alone
        amount = 10.0
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)

        self.assertTrue(success, "Should succeed by rebalancing IN racks capacity.")

        # If rebalancing logic is correct, it moves some gold from one IN rack to the other
        # so one ends up with enough free space to store 10 gm.
        # We'll just check total is correct:
        total_in = sum(r.quantity for r in self.in_racks)
        total_out = sum(r.quantity for r in self.out_racks)
        self.assertAlmostEqual(total_in, 5+7+10, places=3,
            msg="IN racks should have gained 10 total (previous total was 12).")
        # previous total was 12 (5+7), after +10 => 22.

        # So total_in should be 22 => let's confirm
        self.assertAlmostEqual(total_in, 22.0, places=3)

        # The out racks should have lost 10 total
        prev_out = 15  # (10 + 5)
        self.assertAlmostEqual(total_out, prev_out - 10, places=3)

if __name__ == '__main__':
    unittest.main()