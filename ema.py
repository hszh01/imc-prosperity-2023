from typing import Dict, List
from datamodel import OrderDepth, Trade, TradingState, Order
import pandas as pd 

# EMA cross over bools
dip_cross_up = False
dip_cross_down = False

#dip trade index
dip_index = 0
dip_trades = []
dip_ema_1 = []
dip_ema_2 = []

# EMA cross over bools
bag_cross_up = False
bag_cross_down = False

#dip trade index
bag_index = 0
bag_trades = []
bag_ema_1 = []
bag_ema_2 = []

def ema(ema_lst, length, lst):
    multiplier = (2 / (length + 1))
    if len(lst) == length:
        ema = sum(lst) / length
    else:
        p_ema = ema_lst[len(ema_lst)-1]
        ema = (lst[len(lst)-1] * multiplier) + (p_ema * (1 - multiplier))
    return ema


class Trader:
    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        
        # Initialize the method output dict as an empty dict
        result = {}
        
        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            # Retrieve the Order Depth containing all the market BUY and SELL orders for produc
            order_depth: OrderDepth = state.order_depths[product]

            # Check if the current product is the 'dip' product, only then run the order logic
            if product == 'DIP':
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []                
                
                global dip_trades
                global dip_index
                ask_weight = 0
                ask_orders = 0
                bid_weight = 0
                bid_orders = 0
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    for price in order_depth.sell_orders.keys():
                        ask_weight += price * order_depth.sell_orders[price]
                        ask_orders += order_depth.sell_orders[price]
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    for price in order_depth.buy_orders.keys():
                        bid_weight += price * order_depth.buy_orders[price]
                        bid_orders += order_depth.buy_orders[price]
                avg_ask = ask_weight / ask_orders
                avg_bid = bid_weight / bid_orders
                mid_price = (avg_bid + avg_ask) / 2
                dip_trades.append(mid_price)

                # Setup ema
                global dip_ema_1
                global dip_ema_2
                short_period = 5
                long_period = 50
                if len(dip_trades) >= short_period:
                    dip_ema_1.append(ema(dip_ema_1, short_period, dip_trades))
                if len(dip_trades) >= long_period:
                    dip_ema_2.append(ema(dip_ema_2, long_period, dip_trades))
                
                # Find position value
                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0
                buy_volume = 300 - inventory
                sell_volume = -300 - inventory

                # EMA cross over bools
                global dip_cross_up
                global dip_cross_down
                if len(dip_ema_2) > 0:
                    if dip_ema_1[len(dip_ema_1)-1] > dip_ema_2[len(dip_ema_2)-1] and (not dip_cross_up):
                        dip_cross_up = True
                        dip_cross_down = False
                        
                        buy_price = (best_bid + best_ask) / 2 - 1.5
                        # buy_price = mid_price - 1
                        # buy_price = (dip_ema_1[len(dip_ema_1)-1] + dip_ema_2[len(dip_ema_2)-1]) / 2
                        print("BUY", str(buy_volume) + "x", buy_price)
                        orders.append(Order(product, buy_price, buy_volume))
                    elif dip_ema_1[len(dip_ema_1)-1] < dip_ema_2[len(dip_ema_2)-1] and (not dip_cross_down):
                        dip_cross_up = False
                        dip_cross_down = True

                        sell_price = (best_bid + best_ask) / 2 + 1.5
                        # sell_price = mid_price
                        # sell_price = (dip_ema_1[len(dip_ema_1)-1] + dip_ema_2[len(dip_ema_2)-1]) / 2
                        print("SELL", str(sell_volume) + "x", sell_price)
                        orders.append(Order(product, sell_price, buy_volume))
                result[product] = orders

                # Check if the current product is the 'dip' product, only then run the order logic
            if product == 'BAGUETTE':
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []                
                
                global bag_trades
                global bag_index
                ask_weight = 0
                ask_orders = 0
                bid_weight = 0
                bid_orders = 0
                if len(order_depth.sell_orders) > 0:
                    best_ask = min(order_depth.sell_orders.keys())
                    for price in order_depth.sell_orders.keys():
                        ask_weight += price * order_depth.sell_orders[price]
                        ask_orders += order_depth.sell_orders[price]
                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    for price in order_depth.buy_orders.keys():
                        bid_weight += price * order_depth.buy_orders[price]
                        bid_orders += order_depth.buy_orders[price]
                avg_ask = ask_weight / ask_orders
                avg_bid = bid_weight / bid_orders
                mid_price = (avg_bid + avg_ask) / 2
                bag_trades.append(mid_price)

                # Setup ema
                global bag_ema_1
                global bag_ema_2
                short_period = 5
                long_period = 100
                if len(bag_trades) >= short_period:
                    bag_ema_1.append(ema(bag_ema_1, short_period, bag_trades))
                if len(bag_trades) >= long_period:
                    bag_ema_2.append(ema(bag_ema_2, long_period, bag_trades))
                
                # Find position value
                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0
                buy_volume = 150 - inventory
                sell_volume = -150 - inventory

                # EMA cross over bools
                global bag_cross_up
                global bag_cross_down
                if len(bag_ema_2) > 0:
                    if bag_ema_1[len(bag_ema_1)-1] > bag_ema_2[len(bag_ema_2)-1] and (not bag_cross_up):
                        bag_cross_up = True
                        bag_cross_down = False
                        
                        buy_price = (best_bid + best_ask) / 2 - 1.5
                        # buy_price = mid_price - 1
                        # buy_price = (bag_ema_1[len(bag_ema_1)-1] + bag_ema_2[len(bag_ema_2)-1]) / 2
                        print("BUY", str(buy_volume) + "x", buy_price)
                        orders.append(Order(product, buy_price, buy_volume))
                    elif bag_ema_1[len(bag_ema_1)-1] < bag_ema_2[len(bag_ema_2)-1] and (not bag_cross_down):
                        bag_cross_up = False
                        bag_cross_down = True

                        sell_price = (best_bid + best_ask) / 2 + 1.5
                        # sell_price = mid_price
                        # sell_price = (bag_ema_1[len(bag_ema_1)-1] + bag_ema_2[len(bag_ema_2)-1]) / 2
                        print("SELL", str(sell_volume) + "x", sell_price)
                        orders.append(Order(product, sell_price, buy_volume))
                result[product] = orders
        return result