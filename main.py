"""
Main script that runs multi-threaded transactions with your selection logic 
and the new rebalancing approach.
"""

import threading
from concurrent.futures import ThreadPoolExecutor

from rack import in_config, out_config, warehouse
from display import display_racks
from transactions import buy_gold, sell_gold
from controller import create_transaction_requests

def run_simulation_multithreaded():
    # Define ratio and total
    ratio_buy = 0
    ratio_sell = 1
    total_transactions = 1

    # Generate requests
    transaction_requests = create_transaction_requests(ratio_buy, ratio_sell, total_transactions)

    # Print initial state
    print("Initial State:")
    display_racks("IN Racks", in_config["racks"])
    display_racks("OUT Racks", out_config["racks"])
    print(f"Warehouse: {warehouse}\n")

    # Create a global lock
    global_lock = threading.Lock()

    # Use a thread pool
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for (tx_type, amount) in transaction_requests:
            if tx_type == "BUY":
                fut = executor.submit(
                    buy_gold, amount, out_config["racks"], in_config["racks"], warehouse, global_lock
                )
            else:  # SELL
                fut = executor.submit(
                    sell_gold, amount, in_config["racks"], out_config["racks"], warehouse, global_lock
                )
            futures.append((tx_type, amount, fut))

        # Gather results
        for (tx_type, amount, fut) in futures:
            success = fut.result()
            if success:
                print(f"[{tx_type}] {amount} gm SUCCESS.")
            else:
                print(f"[{tx_type}] {amount} gm FAILED.")

    # Final state
    print("\nFinal State:")
    display_racks("IN Racks", in_config["racks"])
    display_racks("OUT Racks", out_config["racks"])
    print(f"Warehouse: {warehouse}\n")


if __name__ == "__main__":
    run_simulation_multithreaded()