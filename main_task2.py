from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        result = {}
        orders: List[Order] = []

        product = "RAINFOREST_RESIN"
        order_depth: OrderDepth = state.order_depths[product]
        position = state.position.get(product, 0)
        
        # Get previous price from traderData
        try:
            previous_price = int(state.traderData)
        except:
            previous_price = None

        # Determine current market price as mid-price if available
        best_ask = min(order_depth.sell_orders.keys()) if order_depth.sell_orders else None
        best_bid = max(order_depth.buy_orders.keys()) if order_depth.buy_orders else None
        mid_price = (best_ask + best_bid) / 2 if best_ask and best_bid else None

        if previous_price <= 9997:
            # Go long if portfolio allows
            if position == 0 and best_ask is not None:
                orders.append(Order(product, best_ask, 50))
            elif position == -50 and best_ask is not None:
                orders.append(Order(product, best_ask, 100))

        elif previous_price >= 10003:
            # Go short if portfolio allows
            if position == 0 and best_bid is not None:
                orders.append(Order(product, best_bid, -50))
            elif position == 50 and best_bid is not None:
                orders.append(Order(product, best_bid, -100))

        # Store current mid-price as next tick's "previous price"
        traderData = str(int(mid_price)) if mid_price is not None else str(previous_price)

        result[product] = orders
        conversions = 0

        return result, conversions, traderData
