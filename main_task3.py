from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

import numpy as np
from collections import deque
from statistics import linear_regression

class Trader:
    def __init__(self):
        self.history = dict()
        self.sp_match = dict()
        self.best_ask = dict()
        self.best_bid = dict()
        
        self.std_len = 100
        self.regression_window = 75

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        result = dict()

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

            self.best_ask[symbol] = min(order_depth.sell_orders.keys())
            self.best_bid[symbol] = max(order_depth.buy_orders.keys())
            mid_price = (self.best_ask[symbol] + self.best_bid[symbol]) / 2
            
            hist_data = self.history[symbol]
            hist_data.append(mid_price)
            hist_data = hist_data[-(self.std_len + 1):]
            self.history[symbol] = hist_data

        for symbol in state.order_depths.keys():
            if symbol in state.position.keys():
                position = state.position[self.sp_match[symbol]]
            else:
                position = 0

            if symbol == 'RAINFOREST_RESIN':
                orders = self.rainforest(symbol, position)
            elif symbol == 'CROISSANTS': # 'CROISSANTS' 'PICNIC_BASKET1'
                orders = self.picnic(symbol, position)
            elif symbol == 'VOLCANIC_ROCK': # 'VOLCANIC_ROCK_VOUCHER_XXXX'
                orders = self.vrock(symbol, position)

            result[symbol] = orders
                
        traderData = "SAMPLE"
        conversions = 1
        return result, conversions, traderData
    
    def rainforest(self, symbol, position):
        return [Order(symbol, 9999, max(0, 50 - position)),
                Order(symbol, 10001, min(0, -50 - position))]
    
        # return []
    
    def picnic(self, symbol, position):
        # # Get historical data for both the stock and ETF
        # stock_hist = self.history[symbol]
        # etf_hist = self.history['PICNIC_BASKET1']
        
        # # Ensure we have enough data points
        # if len(stock_hist) < self.regression_window or len(etf_hist) < self.regression_window:
        #     return []
            
        # # Take the most recent data points
        # stock_prices = np.array(stock_hist[-self.regression_window:])
        # etf_prices = np.array(etf_hist[-self.regression_window:])
        
        # # Calculate log returns
        # # stock_log_returns = np.log(stock_prices[1:] / stock_prices[:-1])
        # # etf_log_returns = np.log(etf_prices[1:] / etf_prices[:-1])

        # stock_log_returns = np.log(stock_prices)
        # etf_log_returns = np.log(etf_prices)
        
        # # Perform linear regression
        # slope, intercept = linear_regression(etf_log_returns, stock_log_returns)
        # predicted_stock_returns = slope * etf_log_returns + intercept
        # residuals = stock_log_returns - predicted_stock_returns
        # std_err = np.std(residuals)
        # deviation = residuals[-1] / std_err
        
        # orders = []
        # if abs(deviation) > 3:
        #     if deviation > 0:
        #         orders.append(Order(symbol, self.best_bid[symbol], max(min(0, -250 - position), -250)))
        #     else:
        #         orders.append(Order(symbol, self.best_ask[symbol], min(max(0, 250 - position), 250)))

        # if position != 0:
        #     if position > 0 and deviation > -2:
        #         orders.append(Order(symbol, self.best_bid[symbol], -position))
        #     elif position < 0 and deviation < 2:
        #         orders.append(Order(symbol, self.best_ask[symbol], -position))

        # return orders
    
        return []
    
    def vrock(self, symbol, position):
        return []
