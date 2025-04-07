from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

import numpy as np

class Trader:
    def __init__(self):
        self.history = dict()

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        result = {}

        for product in state.order_depths.keys():
                order_depth: OrderDepth = state.order_depths[product]
                orders: list[Order] = []

                n = 10

                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                mid_price = (best_ask + best_bid) / 2

                hist_data = self.history[product]
                hist_data.append(mid_price)
                hist_date = hist_data[-101:]
                self.history.update({product: hist_data})

                # std = np.std([hist_data[i] / hist_data[i-1] for i in range(1, len(hist_data))])
                up = int(np.sum([(hist_data[i] / hist_data[i-1]) - 1 for i in range(1, len(hist_data))][-10:]) >= 0)
                spread = min(6, max(2, best_ask - best_bid)) / 2
                
                ask = mid_price + spread
                bid = mid_price - spread

                if state.position[product] >= 0:
                    best_ask_volume = n - state.position[product]
                    best_bid_volume = -n
                else:
                    best_ask_volume = n
                    best_bid_volume = -n + state.position[product]

                print("SELL", str(best_ask_volume) + "x", best_ask)
                orders.append(Order(product, best_ask, best_ask_volume))

                print("BUY", str(best_bid_volume) + "x", best_bid)
                orders.append(Order(product, best_bid, best_bid_volume))

                result[product] = orders
                
        traderData = "SAMPLE"
        
        conversions = 1 

                # Return the dict of orders
                # These possibly contain buy or sell orders
                # Depending on the logic above
        
        return result, conversions, traderData
