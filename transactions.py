"""
transactions.py
Multi-threaded buy_gold and sell_gold functions,
with a default NoOpLock for tests that pass lock=None.
"""

from selection import select_source_rack, select_destination_rack
from rebalancing import (
    rebalance_out_for_gold,
    rebalance_out_for_capacity,
    rebalance_in_for_gold,
    rebalance_in_for_capacity
)

class NoOpLock:
    """
    A do-nothing lock that satisfies the 'with' context manager protocol.
    Used if a real lock isn't provided.
    """
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def buy_gold(amount, out_racks, in_racks, warehouse, lock=None):
    """
    BUY = Move 'amount' FROM OUT racks TO IN racks.

    If lock=None, we default to NoOpLock so tests won't crash.
    In a real multi-threaded scenario, pass a threading.Lock() or similar.
    """
    if lock is None:
        lock = NoOpLock()

    with lock:
        # 1) Need an OUT rack that can supply 'amount'
        source = select_source_rack(out_racks, amount)
        if not source:
            # attempt rebalancing for gold supply
            success = rebalance_out_for_gold(out_racks, amount, warehouse)
            if not success:
                print("[BUY] FAILED: Not enough gold in OUT racks or warehouse.")
                return False
            source = select_source_rack(out_racks, amount)
            if not source:
                print("[BUY] STILL FAILED after rebalancing OUT racks.")
                return False

        # 2) Need an IN rack that can store 'amount'
        destination = select_destination_rack(in_racks, amount)
        if not destination:
            # attempt rebalancing for capacity in IN racks
            success = rebalance_in_for_capacity(in_racks, amount)
            if not success:
                print("[BUY] FAILED: Not enough capacity in IN racks, rebalancing failed.")
                return False
            destination = select_destination_rack(in_racks, amount)
            if not destination:
                print("[BUY] STILL FAILED after rebalancing IN racks.")
                return False

        # 3) Perform the transaction
        source.quantity -= amount
        destination.quantity += amount
        print(f"[BUY] Moved {amount} gm from OUT rack {source} to IN rack {destination}")
        return True


def sell_gold(amount, in_racks, out_racks, warehouse, lock=None):
    """
    SELL = Move 'amount' FROM IN racks TO OUT racks.

    If lock=None, we default to NoOpLock so tests won't crash.
    In a real multi-threaded scenario, pass a threading.Lock() or similar.
    """
    if lock is None:
        lock = NoOpLock()

    with lock:
        # 1) Need an IN rack that can supply 'amount'
        source = select_source_rack(in_racks, amount)
        if not source:
            # gather from multiple IN racks
            success = rebalance_in_for_gold(in_racks, amount)
            if not success:
                print("[SELL] FAILED: Not enough gold in IN racks (rebalance_in_for_gold).")
                return False
            source = select_source_rack(in_racks, amount)
            if not source:
                print("[SELL] STILL FAILED after rebalancing IN racks.")
                return False

        # 2) Need an OUT rack that can store 'amount'
        destination = select_destination_rack(out_racks, amount)
        if not destination:
            # free space in an OUT rack => warehouse
            success = rebalance_out_for_capacity(out_racks, amount, warehouse)
            if not success:
                print("[SELL] FAILED: Not enough capacity in OUT racks (rebalance_out_for_capacity).")
                return False
            destination = select_destination_rack(out_racks, amount)
            if not destination:
                print("[SELL] STILL FAILED after rebalancing OUT racks.")
                return False

        # 3) Perform the transaction
        source.quantity -= amount
        destination.quantity += amount
        print(f"[SELL] Moved {amount} gm from IN rack {source} to OUT rack {destination}")
        return True