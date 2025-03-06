

"""
Controller logic to create transaction requests in certain ratios,
with amounts in [buy_min, buy_max] for BUY and [sell_min, sell_max] for SELL.
"""

import random
import config

def create_transaction_requests(ratio_buy, ratio_sell, total_transactions=50):
   
    requests = []
    while len(requests) < total_transactions:
       # add buy multiple time
        for _ in range(ratio_buy):
            if len(requests) >= total_transactions:
                break
            amt = round(random.uniform(config.buy_min, config.buy_max), 3)
            requests.append(("BUY", amt))

        # Add sell multiuple times
        for _ in range(ratio_sell):
            if len(requests) >= total_transactions:
                break
            amt = round(random.uniform(config.sell_min, config.sell_max), 3)
            requests.append(("SELL", amt))

    return requests

