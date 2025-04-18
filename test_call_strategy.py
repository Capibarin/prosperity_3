from datamodel import OrderDepth, TradingState, Order, Symbol
from typing import List, Dict


# In the Call credit spread there are 6 adjustments available (see [TO ADJUST])
class Trader:
    def __init__(self):
        self.volcanic_data = []  # Historical data for VOLCANIC ROCK
        self.option1_position = 0
        self.option2_position = 0
        self.entry_value = 0.0
        self.a = 10150  # Lower bound for local maxima [TO ADJUST]
        self.b = 10250  # Upper bound for local maxima [TO ADJUST]
        self.position_size = 100  # Number of contracts to trade [TO ADJUST]

    def get_mid_price(self, state: TradingState, product: Symbol) -> float:
        order_depth = state.order_depths.get(product, OrderDepth())
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else 0
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else 0
        return (best_bid + best_ask) / 2 if best_bid and best_ask else 0.0

    def check_conditions(self, data, a, b):  # remove inputs and self.
        window_size = 75  # [TO ADJUST]
        required_maxima = 3  # [TO ADJUST]

        if len(data) < window_size:
            return False

        i = len(data) - window_size + 1
        window = data[i:i + window_size]
        local_maxima = []
        for j in range(1, len(window) - 1):
            if window[j] > window[j - 1] and window[j] > window[j + 1]:
                if a <= window[j] <= b:
                    local_maxima.append(window[j])
        if len(local_maxima) >= required_maxima and all(m <= b for m in window):
            return True
        return False

    def run(self, state: TradingState):
        result = {}
        conversions = 1
        trader_data = "SAMPLE"

        # Main product and its options
        volcanic = 'VOLCANIC_ROCK'
        option1 = 'VOLCANIC_ROCK_VOUCHER_10250'
        option2 = 'VOLCANIC_ROCK_VOUCHER_10500'

        # Get current prices
        volcanic_price = self.get_mid_price(state, volcanic)

        order_depth_option1 = state.order_depths.get(option1, OrderDepth())
        # Best bid
        option1_price = max(order_depth_option1.buy_orders.keys()) if order_depth_option1.buy_orders else 0

        order_depth_option2 = state.order_depths.get(option1, OrderDepth())
        # Best ask
        option2_price = min(order_depth_option2.sell_orders.keys()) if order_depth_option2.sell_orders else 0

        # Update volcanic rock data
        if volcanic_price > 0:
            self.volcanic_data.append(volcanic_price)

        # Check trading conditions
        condition_met = self.check_conditions(self.volcanic_data, self.a, self.b)

        # Enter positions if condition met and not in position
        if condition_met and self.option1_position == 0 and self.option2_position == 0:
            # Short OPTION 1
            if option1_price > 0:
                result[option1] = [Order(option1, option1_price, -self.position_size)]

            # Long OPTION 2
            if option2_price > 0:
                result[option2] = [Order(option2, option2_price, self.position_size)]

            # Record positions and entry value
            self.option1_position = -self.position_size
            self.option2_position = self.position_size
            self.entry_value = (-option1_price + option2_price) * self.position_size

        # Monitor existing positions
        if self.option1_position != 0 or self.option2_position != 0:
            # Get current executable prices for exit

            # New exit condition based on volcanic price
            if volcanic_price >= 10375 or volcanic_price <= 10150:
                # Close OPTION 1 short position (buy back)
                if option1_price and self.option1_position < 0:
                    result[option1] = [Order(option1, option1_price, abs(self.option1_position))]

                # Close OPTION 2 long position (sell)
                if option2_price and self.option2_position > 0:
                    result[option2] = [Order(option2, option2_price, -self.option2_position)]

                # Reset positions only if both legs executed
                if option1 in result and option2 in result:
                    self.option1_position = 0
                    self.option2_position = 0
                    self.entry_value = 0.0

        return result, conversions, trader_data
