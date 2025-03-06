"""
Test #7: Force a SELL that requires an OUT rack to free space into warehouse.
We have a single OUT rack that is almost full, 
and we want to store more gold than it can hold without pushing existing gold into warehouse.
"""

import unittest
from rack import Rack
from transactions import sell_gold

class Test7WarehouseUsage(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 0)  # empty warehouse for clarity
        self.in_racks = [
            Rack(10, 10),  # fully loaded
        ]
        # One OUT rack with minimal free space
        self.out_racks = [
            Rack(10, 9)  # capacity=10, quantity=9 => free=1
        ]

    def test_warehouse_push(self):
        # We want to SELL 5 gm
        # The out_rack can store only 1 gm as is, so we must push 4 gm to warehouse first.
        success = sell_gold(5.0, self.in_racks, self.out_racks, self.warehouse, lock=None)
        self.assertTrue(success, "Should succeed by pushing existing OUT gold to warehouse first.")

        # Final check
        # The out_racks[0] ended up with 5 gm more, so it has total 14 => but capacity=10, so that can't be
        # Because rebalancing would push 4 gm to warehouse first => 
        # so out_racks[0] might have 9 + ??? Wait, let's see:
        # The logic is "move existing gold from out rack to warehouse if needed to free space, 
        # then store the new 5 gm." 
        # Actually it's simpler: 
        #  - There's only 1 out rack. 
        #  - We want to store 5. 
        #  - There's 1 free => we must move 4 to warehouse => new out rack quantity=5 => free=5 
        # Then add the 5 from the SELL => final is 10. 
        self.assertAlmostEqual(self.out_racks[0].quantity, 10.0, places=3,
            msg="OUT rack final should be 10.0 after storing 5 gm and pushing old gold to warehouse.")
        
        # The warehouse was 0 => gained 4 from that push
        self.assertAlmostEqual(self.warehouse.quantity, 4.0, places=3)

        # The in rack lost 5 => final 5
        self.assertAlmostEqual(self.in_racks[0].quantity, 5.0, places=3)

if __name__ == '__main__':
    unittest.main()