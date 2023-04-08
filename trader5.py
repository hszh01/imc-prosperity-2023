from typing import Dict, List
from datamodel import OrderDepth, Trade, TradingState, Order
import numpy as np
import pandas as pd

# import matplotlib.pyplot as plt

COCO_PINA_DIFF = 15000 - 8000


# Find position value
def pos_val(position_lst, product):
    if product in position_lst:
        return position_lst[product]
    else:
        return 0


def find_price(order_depth, product):
    ask_weight = 0
    ask_orders = 0
    bid_weight = 0
    bid_orders = 0
    if len(order_depth.sell_orders) > 0:
        for price in order_depth.sell_orders.keys():
            ask_weight += price * order_depth.sell_orders[price]
            ask_orders += order_depth.sell_orders[price]
    else:
        return -1
    if len(order_depth.buy_orders) != 0:
        for price in order_depth.buy_orders.keys():
            bid_weight += price * order_depth.buy_orders[price]
            bid_orders += order_depth.buy_orders[price]
    else:
        return -1
    avg_ask = ask_weight / ask_orders
    avg_bid = bid_weight / bid_orders
    return (avg_bid + avg_ask) / 2


# EMA cross over bools
dip_cross_up = False
dip_cross_down = False

# dip trade index
dip_index = 0
dip_trades = []
dip_ema_1 = []
dip_ema_2 = []

# EMA cross over bools
bag_cross_up = False
bag_cross_down = False

# dip trade index
bag_index = 0
bag_trades = []
bag_ema_1 = []
bag_ema_2 = []


def ema(ema_lst, length, lst):
    multiplier = (2 / (length + 1))
    if len(lst) == length:
        ema = sum(lst) / length
    else:
        p_ema = ema_lst[len(ema_lst) - 1]
        ema = (lst[len(lst) - 1] * multiplier) + (p_ema * (1 - multiplier))
    return ema


class Trader:
    pnl = 0

    last_dolphins = 0

    running_difference = 0

    coconut_price = 0

    coconut_bid = 0

    coconut_ask = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:

        # Initialize the method output dict as an empty dict
        result = {}

        for product in state.order_depths.keys():
            # Retrieve the Order Depth containing all the market BUY and SELL orders for produc
            order_depth: OrderDepth = state.order_depths[product]

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            if product == 'PEARLS':
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                    inventory1 = state.position[product]
                else:
                    inventory = 0
                    inventory1 = 0

                buy_volume = 20 - inventory
                sell_volume = -20 - inventory

                print("BUY", str(buy_volume) + "x", 9998.5)
                orders.append(Order(product, 9998.5, buy_volume))
                if inventory != inventory1:
                    print("INVENTORY is now: ", str(inventory))
                if inventory < inventory1:
                    self.pnl += (inventory1 - inventory)
                    print("PNL: ", self.pnl)
                if inventory == inventory1:
                    print("Not working")

                print("SELL", str(sell_volume) + "x", 10001.5)
                orders.append(Order(product, 10001.5, sell_volume))
                if inventory != inventory1:
                    print("INVENTORY is now: ", str(inventory))
                if inventory < inventory1:
                    self.pnl += (inventory1 - inventory)
                    print("PNL: ", self.pnl)
                if inventory == inventory1:
                    print("Not working")

                # Add all the above the orders to the result dict
                result[product] = orders

                # Return the dict of orders
                # These possibly contain buy or sell orders for PEARLS
                # Depending on the logic above

            elif product == 'BANANAS':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]  # -- total 1.8k

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0

                best_bid = best_ask = best_bid_volume = best_ask_volume = 0

                # checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # if best_bid > acceptable_price:
                    # print("SELL", str(best_bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -best_bid_volume))

                buy_price = ((best_bid + best_ask) / 2) - 2
                # buy_volume = int(10 - (0.5 * inventory))
                sell_price = ((best_bid + best_ask) / 2) + 2
                # sell_volume = int(10 + (0.5 * inventory))
                buy_volume = 20 - inventory
                sell_volume = 20 + inventory

                orders.append(Order(product, buy_price, buy_volume))

                orders.append(Order(product, sell_price, -sell_volume))

                # Add all the above the orders to the result dict
                result[product] = orders

            elif product == 'BERRIES':

                order_depth: OrderDepth = state.order_depths[product]  # -- total 1.8k

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0

                best_bid = best_ask = best_bid_volume = best_ask_volume = 0

                # checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # if best_bid > acceptable_price:
                    # logger.print("SELL", str(best_bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -best_bid_volume))

                if 399800 < state.timestamp < 400200:
                    buy_price = best_ask + 20
                    buy_volume = 250 - inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    sell_price = ((best_bid + best_ask) / 2)
                    sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, buy_price, buy_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 499800 < state.timestamp < 500200:
                    sell_volume = 250 + inventory
                    sell_price = best_bid - 20
                    # sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, sell_price, -sell_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 749800 < state.timestamp < 750200:
                    buy_price = best_ask + 20
                    buy_volume = -inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    sell_price = ((best_bid + best_ask) / 2)
                    sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, buy_price, buy_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 0 < state.timestamp < 399800 or 750200 < state.timestamp < 999999:
                    buy_price = ((best_bid + best_ask) / 2) - 2
                    buy_volume = int(125 - (0.5 * inventory))
                    sell_price = ((best_bid + best_ask) / 2) + 2
                    sell_volume = int(125 + (0.5 * inventory))
                    # buy_volume = 600 - inventory
                    # sell_volume = 600 + inventory
                    orders.append(Order(product, buy_price, buy_volume))

                    orders.append(Order(product, sell_price, -sell_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

            # Add all the above the orders to the result dict

            elif product == 'PICNIC_BASKET':

                # Retrieve the Order Depth containing all the market BUY and SELL orders for PEARLS
                order_depth: OrderDepth = state.order_depths[product]  # -- total 1.8k

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0

                best_bid = best_ask = best_bid_volume = best_ask_volume = 0

                # checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # if best_bid > acceptable_price:
                    # print("SELL", str(best_bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -best_bid_volume))

                # if ((best_bid + best_ask) / 2) < 73800:
                # buy_volume = 70 - inventory
                # buy_price = best_ask + 20
                buy_price = ((best_bid + best_ask) / 2) - 2
                buy_volume = int(35 - (0.5 * inventory))
                sell_price = ((best_bid + best_ask) / 2) + 2
                sell_volume = int(35 + (0.5 * inventory))
                orders.append(Order(product, buy_price, buy_volume))
                orders.append(Order(product, sell_price, -sell_volume))
                result[product] = orders

            elif product == 'UKULELE':
                order_depth: OrderDepth = state.order_depths[product]  # -- total 1.8k

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0

                best_bid = best_ask = best_bid_volume = best_ask_volume = 0

                # checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # if best_bid > acceptable_price:
                    # print("SELL", str(best_bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -best_bid_volume))

                if 299800 < state.timestamp < 300200:
                    buy_price = best_ask + 20
                    buy_volume = 70 - inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    sell_price = ((best_bid + best_ask) / 2)
                    sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, buy_price, buy_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 599800 < state.timestamp < 600200:
                    sell_volume = 70 + inventory
                    sell_price = best_bid - 20
                    # sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, sell_price, -sell_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 899800 < state.timestamp < 900200:
                    buy_price = best_ask + 20
                    buy_volume = -inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    sell_price = ((best_bid + best_ask) / 2)
                    sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, buy_price, buy_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

            elif product == 'BAGUETTE':

                order_depth: OrderDepth = state.order_depths[product]  # -- total 1.8k

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0

                best_bid = best_ask = best_bid_volume = best_ask_volume = 0

                # checks if there are any SELL orders in the PEARLS market
                if len(order_depth.sell_orders) > 0:
                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = min(order_depth.sell_orders.keys())
                    best_ask_volume = order_depth.sell_orders[best_ask]

                if len(order_depth.buy_orders) != 0:
                    best_bid = max(order_depth.buy_orders.keys())
                    best_bid_volume = order_depth.buy_orders[best_bid]
                    # if best_bid > acceptable_price:
                    # print("SELL", str(best_bid_volume) + "x", best_bid)
                    # orders.append(Order(product, best_bid, -best_bid_volume))

                if 749800 < state.timestamp < 750200:
                    buy_price = best_ask + 20
                    buy_volume = 150 + inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    #sell_price = ((best_bid + best_ask) / 2)
                    #sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, buy_price, buy_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

                elif 899800 < state.timestamp < 900200:
                    sell_price = best_bid - 20
                    sell_volume = inventory
                    # buy_volume = int(125 - (0.5 * inventory))
                    #sell_price = ((best_bid + best_ask) / 2)
                    #sell_volume = int(125 + (0.5 * inventory))

                    orders.append(Order(product, sell_price, -sell_volume))

                    # Add all the above the orders to the result dict
                    result[product] = orders

        return result