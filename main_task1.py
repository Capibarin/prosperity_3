from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

import numpy as np
from collections import deque

class Trader:
    def __init__(self):
        self.history = dict()
        self.sp_match = dict()
        
        self.std_len = 100
        self.mean_len = 10
        self.ladder_volumes = [10, 30, 50]

    def create_ladder_orders(self, symbol, base_price, is_buy=1, current_position=0):
        """
        Create a ladder of orders at different price levels
        
        Args:
            symbol: The trading symbol
            side: 'buy' or 'sell'
            base_price: The best bid or ask price
            total_volume: Total volume to distribute
            is_buy: True for buy orders, False for sell orders
            current_position: Current position in the symbol
            
        Returns:
            List of Order objects
        """
        orders = []

        if current_position * is_buy < 0:
            current_position = 0
        else:
            current_position = abs(current_position)
        
        for i in range(len(self.ladder_volumes)):    
            price = base_price - i * is_buy
            volume = max(0, self.ladder_volumes[i] - current_position)
            orders.append(Order(symbol, price, is_buy * volume))
            current_position += volume
            
        return orders

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

                    if trend > abs(std) and state.timestamp % 1000 == 0:
                        stop = True
                    else:
                        stop = False
                    
                    # Get current position
                    current_position = 0
                    if self.sp_match[symbol] in state.position.keys():
                        current_position = state.position[self.sp_match[symbol]]
                    
                    if stop:
                        if self.sp_match[symbol] in state.position.keys():
                            if state.position[self.sp_match[symbol]] >= 0:
                                best_bid_volume = 0
                                best_ask_volume = -state.position[self.sp_match[symbol]]
                            else:
                                best_bid_volume = -state.position[self.sp_match[symbol]]
                                best_ask_volume = 0
                        else:
                            best_bid_volume = self.stock_limit
                            best_ask_volume = -self.stock_limit
                    
                    else:
                        # if self.sp_match[symbol] in state.position.keys():
                        #     if state.position[self.sp_match[symbol]] >= 0:
                        #         best_bid_volume = self.stock_limit - state.position[self.sp_match[symbol]]
                        #         best_ask_volume = -self.stock_limit
                        #     else:
                        #         best_bid_volume = self.stock_limit
                        #         best_ask_volume = -self.stock_limit - state.position[self.sp_match[symbol]]
                        # else:
                        #     best_bid_volume = self.stock_limit
                        #     best_ask_volume = -self.stock_limit

                        sell_orders = self.create_ladder_orders(symbol, best_ask, is_buy=-1, current_position=current_position)
                        orders.extend(sell_orders)
                        
                        buy_orders = self.create_ladder_orders(symbol, best_bid, is_buy=1, current_position=current_position)
                        orders.extend(buy_orders)

                result[symbol] = orders
                
        traderData = "SAMPLE"
        
        conversions = 1 

        # Return the dict of orders
        # These possibly contain buy or sell orders
        # Depending on the logic above
        
        return result, conversions, traderData
