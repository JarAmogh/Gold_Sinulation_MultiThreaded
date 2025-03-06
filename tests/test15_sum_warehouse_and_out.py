"""
Test #15: A big BUY that requires partial from out racks + partial from warehouse, 
and it DOES succeed if sum is enough.
"""

import unittest
from rack import Rack
from transactions import buy_gold

class Test15SumWarehouseAndOut(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(50, 20)  # capacity=50, quantity=20
        # 2 out racks with total 10 gm
        self.out_racks = [
            Rack(10, 6),
            Rack(10, 4)
        ]
        # 1 in rack with plenty of capacity
        self.in_racks = [
            Rack(50, 0)
        ]

    def test_sum_warehouse_and_out(self):
        # total out racks = 10, warehouse=20 => total=30
        # we want 25 => should succeed
        amount = 25.0
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Should succeed by combining out racks + warehouse")

        # final checks
        total_in = sum(r.quantity for r in self.in_racks)
        self.assertAlmostEqual(total_in, 25.0, places=3, 
            msg="IN racks gained 25 total.")
        total_out = sum(r.quantity for r in self.out_racks)
        # originally 10 => after giving 25 => -15 => but we top up from warehouse by 15 => final 0
        self.assertAlmostEqual(total_out, 0.0, places=3)
        # warehouse was 20 => gave 15 => final 5
        self.assertAlmostEqual(self.warehouse.quantity, 5.0, places=3)

if __name__ == '__main__':
    unittest.main()