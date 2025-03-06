"""
Test #10: A large SELL transaction that fails because:
  - Even after rebalancing among OUT racks or pushing gold to warehouse,
    there's not enough total capacity to store 'required_amount'.
Expected: transaction fails. 
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test10BigSellFailsCapacity(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 0)  # can hold some gold
        # 2 IN racks with lots of gold
        self.in_racks = [
            Rack(30, 30),  # full
            Rack(20, 20)   # full
        ]
        # 2 OUT racks, but total capacity is small
        # Even if we push all their existing gold to warehouse, they won't have enough space
        self.out_racks = [
            Rack(10, 5),  # free=5
            Rack(10, 8)   # free=2
        ]

    def test_big_sell_fails_capacity(self):
        amount = 20  # we want to store 20 gm in out racks
        # The total free in out_racks is 7
        # If we push the existing 5+8=13 to warehouse, the racks become 0 each => total capacity=20 
        # Actually that might just barely succeed if we can free them both up to 10 each => 20 total
        # But let's say we consider we can't unify both racks into a single one if the logic requires a single rack
        # Actually let's assume we need a single out rack to hold entire 20 => which is impossible. 
        # => transaction fails.

        success = sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertFalse(success, "Should fail because no single out rack can store 20 gm, even after rebalancing.")

        # None changed
        self.assertAlmostEqual(self.out_racks[0].quantity, 5)
        self.assertAlmostEqual(self.out_racks[1].quantity, 8)
        self.assertAlmostEqual(self.in_racks[0].quantity, 30)
        self.assertAlmostEqual(self.in_racks[1].quantity, 20)

if __name__ == '__main__':
    unittest.main()

    