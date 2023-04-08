from typing import Dict, List
from datamodel import OrderDepth, TradingState, Order


class Trader:
    pnl = 0

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        moving_average = []

        # Iterate over all the keys (the available products) contained in the order dephts
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

                print("BUY", str(buy_volume) + "x", 9998)
                orders.append(Order(product, 9998, buy_volume))
                if inventory != inventory1:
                    print("INVENTORY is now: ", str(inventory))
                if inventory < inventory1:
                    pnl += (inventory1 - inventory)
                    print("PNL: ", pnl)
                if inventory == inventory1:
                    print("Not working")

                print("SELL", str(sell_volume) + "x", 10002)
                orders.append(Order(product, 10002, sell_volume))
                if inventory != inventory1:
                    print("INVENTORY is now: ", str(inventory))
                if inventory < inventory1:
                    pnl += (inventory1 - inventory)
                    print("PNL: ", pnl)
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


                mid_price = 0
                #if len(order_depth.sell_orders) > 0 and len(order_depth.buy_orders) != 0:
                    #mid_price = ((best_bid) * (best_bid_volume / (best_bid_volume + best_ask_volume))) + ((best_ask) * (best_ask_volume / (best_bid_volume + best_ask_volume)))
                #buy_price = int(mid_price) - 2.5
                #sell_price = int(mid_price) + 2.5
                buy_price = ((best_bid + best_ask) / 2) - 2
                #buy_volume = int(10 - (0.5 * inventory))
                sell_price = ((best_bid + best_ask) / 2) + 2
                #sell_volume = int(10 + (0.5 * inventory))
                buy_volume = 20 - inventory
                sell_volume = 20 + inventory

                """moving_average.append(best_ask)

                moving_average.append(best_bid)

                if len(moving_average) == 12:
                    moving_average.pop(0)
                    moving_average.pop(0)

                if len(moving_average) == 10:
                    average_price = sum(moving_average) / len(moving_average)
                    buy_price = average_price - 2.5
                    sell_price = average_price + 2.5
                    orders.append(Order(product, buy_price, buy_volume))

                    orders.append(Order(product, sell_price, -sell_volume))"""

                print("BUY", str(buy_volume) + "x", buy_price)
                orders.append(Order(product, buy_price, buy_volume))

                print("SELL", str(-sell_volume) + "x", sell_price)
                orders.append(Order(product, sell_price, -sell_volume))

                # Add all the above the orders to the result dict
                result[product] = orders

            elif product == 'PINA_COLADAS':

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

                buy_price = ((best_bid + best_ask) / 2)
                # buy_volume = int(10 - (0.5 * inventory))
                sell_price = ((best_bid + best_ask) / 2)
                # sell_volume = int(10 + (0.5 * inventory))
                buy_volume = 300 - inventory
                sell_volume = 300 + inventory

                print("BUY", str(buy_volume) + "x", buy_price)
                orders.append(Order(product, buy_price, buy_volume))

                print("SELL", str(-sell_volume) + "x", sell_price)
                orders.append(Order(product, sell_price, -sell_volume))

                # Add all the above the orders to the result dict
                result[product] = orders

            elif product == 'COCONUTS':

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

                buy_price = ((best_bid + best_ask) / 2)
                # buy_volume = int(10 - (0.5 * inventory))
                sell_price = ((best_bid + best_ask) / 2) 
                # sell_volume = int(10 + (0.5 * inventory))
                buy_volume = 600 - inventory
                sell_volume = 600 + inventory

                print("BUY", str(buy_volume) + "x", buy_price)
                orders.append(Order(product, buy_price, buy_volume))

                print("SELL", str(-sell_volume) + "x", sell_price)
                orders.append(Order(product, sell_price, -sell_volume))

                # Add all the above the orders to the result dict
                result[product] = orders


        return result