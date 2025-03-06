"""
Test #12: A concurrency test with small transactions. 
We mock concurrency by calling buy/sell in a loop with lock=None 
or a fake lock. Typically concurrency is tested end-to-end, 
but we'll show a simple example.
"""

import unittest
import threading
from rack import Rack
from transactions import buy_gold, sell_gold

class DummyLock:
    """A no-op lock that doesn't actually lock."""
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class Test12ConcurrentSmall(unittest.TestCase):
    def setUp(self):
        self.warehouse = Rack(100, 50)
        self.in_racks = [Rack(20, 10), Rack(20, 10)]
        self.out_racks = [Rack(20, 15), Rack(20, 0)]
        self.lock = DummyLock()  # won't actually enforce concurrency

    def worker_buy(self, amount):
        buy_gold(amount, self.out_racks, self.in_racks, self.warehouse, lock=self.lock)

    def worker_sell(self, amount):
        sell_gold(amount, self.in_racks, self.out_racks, self.warehouse, lock=self.lock)

    def test_concurrent(self):
        # We'll create 2 threads for BUYS, 2 threads for SELLS
        threads = []
        # spawn 2 buy threads
        for _ in range(2):
            t = threading.Thread(target=self.worker_buy, args=(5,))
            threads.append(t)
        # spawn 2 sell threads
        for _ in range(2):
            t = threading.Thread(target=self.worker_sell, args=(3,))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Check final sums
        # We did 2 buys (total 10) and 2 sells (total 6).
        # Net +4 gm to the IN racks. 
        total_in = sum(r.quantity for r in self.in_racks)
        # originally 20 total => expect 24 now
        self.assertAlmostEqual(total_in, 24.0, places=3)

if __name__ == '__main__':
    unittest.main()