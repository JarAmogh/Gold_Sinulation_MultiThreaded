"""
Test #9: A large BUY transaction that fails because:
  1) The sum of all OUT racks + warehouse is still < required_amount.
  2) No rebalancing can magically create enough gold.
Expected result: transaction fails.
"""

import unittest
from rack import Rack
from transactions import buy_gold

class Test9BigBuyFails(unittest.TestCase):
    def setUp(self):
        # Warehouse that doesn't have enough gold
        self.warehouse = Rack(50, 30)  # capacity=50, quantity=30

        # OUT racks total only 20 gm
        self.out_racks = [
            Rack(10, 10),
            Rack(10, 10)
        ]

        # IN racks with enough capacity
        self.in_racks = [
            Rack(100, 0),
            Rack(50, 0)
        ]

    def test_big_buy_fails(self):
        # We want to buy 70 gm total
        # sum of out racks = 20, warehouse=30 => total=50 => not enough
        amount = 70.0
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertFalse(success, "Transaction should fail, not enough total gold in OUT + warehouse.")

        # Check that nothing changed
        self.assertEqual(self.out_racks[0].quantity, 10)
        self.assertEqual(self.out_racks[1].quantity, 10)
        self.assertEqual(self.warehouse.quantity, 30)
        self.assertEqual(self.in_racks[0].quantity, 0)
        self.assertEqual(self.in_racks[1].quantity, 0)

if __name__ == '__main__':
    unittest.main()