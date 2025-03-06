"""
Test #6: Checking 'rebalance_out_for_gold' specifically:
We want a BUY that demands more gold than any single OUT rack has, so we must top up from warehouse.
"""

import unittest
from rack import Rack
from transactions import buy_gold

class Test6RebalanceOut(unittest.TestCase):
    def setUp(self):
        # big enough warehouse so we can top up
        self.warehouse = Rack(100, 80)
        # 2 small OUT racks
        self.out_racks = [
            Rack(10, 2),
            Rack(8, 3)
        ]
        # 2 IN racks with plenty of space
        self.in_racks = [
            Rack(10, 0),
            Rack(20, 0)
        ]

    def test_rebalance_out_for_gold(self):
        amount = 10.0
        success = buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Should succeed by topping up an OUT rack from warehouse.")

        # We expect that final sum of out racks to be (2+3) - 10 = -5 if we didn't top up
        # but we do top up from warehouse. So let's see final out racks total. 
        # The actual source might have ended with 0, or partial. We'll just check final sums:

        total_out = sum(r.quantity for r in self.out_racks)
        # original total in out racks was 5 => after giving away 10 => -5, but we top up from warehouse by 5 
        # so final total_out is 0
        # Let's see if that logic checks out
        # We'll just check total_in and warehouse:

        total_in = sum(r.quantity for r in self.in_racks)
        self.assertAlmostEqual(total_in, 10.0, places=3, 
            msg="IN racks should have gained 10 total from the BUY.")
        
        # warehouse was 80 => it gave some gold to out racks
        # we'd guess it gave 5 so that out racks could supply 10
        # so it might be 75 now
        # Let's check:
        self.assertAlmostEqual(self.warehouse.quantity, 75.0, places=3,
            msg="Warehouse expected to lose 5 in the top-up process.")

if __name__ == '__main__':
    unittest.main()


    