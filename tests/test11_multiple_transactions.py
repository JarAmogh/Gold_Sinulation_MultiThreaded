"""
Test #11: Multiple consecutive transactions in one test.
We do a sequence of buys/sells and check final totals.
"""

import unittest
from rack import Rack
from transactions import buy_gold, sell_gold

class Test11MultipleTransactions(unittest.TestCase):
    def setUp(self):
        # Enough warehouse
        self.warehouse = Rack(100, 50)
        # A few racks
        self.in_racks = [
            Rack(20, 5),
            Rack(10, 2)
        ]
        self.out_racks = [
            Rack(15, 10),
            Rack(15, 5)
        ]

    def test_multiple_txs(self):
        # 1) BUY 5
        s1 = buy_gold(5, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertTrue(s1, "1st transaction (BUY 5) should succeed.")
        # 2) SELL 3
        s2 = sell_gold(3, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(s2, "2nd transaction (SELL 3) should succeed.")
        # 3) BUY 8
        s3 = buy_gold(8, self.out_racks, self.in_racks, self.warehouse, lock=None)
        self.assertTrue(s3, "3rd transaction (BUY 8) should succeed.")
        # 4) SELL 10
        s4 = sell_gold(10, self.in_racks, self.out_racks, self.warehouse, lock=None)
        # Could fail or succeed depending on racks. Let's assert it passes:
        self.assertTrue(s4, "4th transaction (SELL 10) hopefully should succeed.")

        # final check
        total_in = sum(r.quantity for r in self.in_racks)
        total_out = sum(r.quantity for r in self.out_racks)
        total_all = total_in + total_out + self.warehouse.quantity
        # The total gold in the system never changes:
        init_total = 5+2 + 10+5 + 50 # => 72
        self.assertAlmostEqual(total_all, init_total, places=3, 
            msg="Total gold remains the same across multiple transactions.")

if __name__ == '__main__':
    unittest.main()