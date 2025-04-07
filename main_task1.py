from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

import numpy as np

class Trader:
    def __init__(self):
        self.history = dict()
        self.sp_match = dict()

        self.stock_limit = 10
        self.std_len = 100
        self.mean_len = 10

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        result = {}

        if len(self.sp_match) == 0:
            for symbol in state.listings.keys():
                self.sp_match[state.listings[symbol].product] = symbol
                self.history[symbol] = []

        if len(self.history) == 0:
            for symbol in state.listings.keys():
                self.history[symbol] = []

        for symbol in state.order_depths.keys():
                order_depth: OrderDepth = state.order_depths[symbol]
                orders: list[Order] = []

                best_ask = min(order_depth.sell_orders.keys())
                best_bid = max(order_depth.buy_orders.keys())
                mid_price = (best_ask + best_bid) / 2
                
                hist_data = self.history[symbol]
                hist_data.append(mid_price)
                hist_date = hist_data[-(self.std_len + 1):]
                self.history[symbol] = hist_data

                if len(hist_date) >= self.std_len + 1:
                    price_dif = [(hist_data[i] / hist_data[i-1]) - 1 for i in range(1, len(hist_data))]
                    std = np.std(price_dif)
                    trend = np.mean(price_dif[-self.mean_len:])

                    if trend > std:
                        best_ask += 1
                        best_bid += 1
                    elif trend < -std:
                        best_ask -= 1
                        best_bid -= 1
                    
                    if self.sp_match[symbol] in state.position.keys():
                        if state.position[self.sp_match[symbol]] >= 0:
                            best_bid_volume = self.stock_limit - state.position[self.sp_match[symbol]]
                            best_ask_volume = -self.stock_limit
                        else:
                            best_bid_volume = self.stock_limit
                            best_ask_volume = -self.stock_limit - state.position[self.sp_match[symbol]]
                    else:
                        best_bid_volume = self.stock_limit
                        best_ask_volume = -self.stock_limit

                    print("SELL", str(best_ask_volume) + "x", best_ask)
                    orders.append(Order(symbol, best_ask, best_ask_volume))

                    print("BUY", str(best_bid_volume) + "x", best_bid)
                    orders.append(Order(symbol, best_bid, best_bid_volume))

                result[symbol] = orders
                
        traderData = "SAMPLE"
        
        conversions = 1 

                # Return the dict of orders
                # These possibly contain buy or sell orders
                # Depending on the logic above
        
        return result, conversions, traderData
