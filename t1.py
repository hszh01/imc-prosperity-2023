from typing import Dict, List
from datamodel import OrderDepth, Trade, TradingState, Order
import pandas as pd 

# EMA cross over bools
cross_up = False
cross_down = False

#timestamp
prev_t = 0

#count
count = 1

df = pd.DataFrame({'price' : []})

class Trader:
   

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # EMA cross over bools
        global cross_up
        global cross_down
        #prev timestamp
        global prev_t

        global df
        global count

        # Tight EMA
        ema_1000 = pd.DataFrame()
        # Loose EMA
        ema_5000 = pd.DataFrame()
        

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            # Retrieve the Order Depth containing all the market BUY and SELL orders for produc
            order_depth: OrderDepth = state.order_depths[product]

            # Check if the current product is the 'PEARLS' product, only then run the order logic
            # if product == 'PEARLS':
                # # Initialize the list of Orders to be sent as an empty list
                # orders: list[Order] = []

                # if product in state.position:
                #     inventory = state.position[product]
                # else:
                #     inventory = 0

                # buy_volume = 20 - inventory
                # sell_volume = -20 - inventory

                # print("BUY", product, str(buy_volume) + "x", 9999.5)
                # orders.append(Order(product, 9999.5, buy_volume))

                # print("SELL", product, str(sell_volume) + "x", 10000.5)
                # orders.append(Order(product, 10000.5, sell_volume))


                # # Add all the above the orders to the result dict
                # result[product] = orders

                # # Return the dict of orders
                # # These possibly contain buy or sell orders for PEARLS
                # # Depending on the logic above





            # Check if the current product is the 'BANANAS' product, only then run the order logic
            if product == 'BANANAS':
                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Find position value
                if product in state.position:
                    inventory = state.position[product]
                else:
                    inventory = 0
                buy_volume = 20 - inventory
                sell_volume = -20 - inventory
                
                
                if 'BANANAS' in state.market_trades:
                    if len(state.market_trades['BANANAS']) > 0:
                        trades: Trade = state.market_trades['BANANAS']

                        # best_bid = -1
                        # best_ask = -1
                        # if len(order_depth.sell_orders) > 0:
                        #             tot = 0
                        #             buy_weight_sum = 0
                        #             for key in order_depth.buy_orders.keys():
                        #                  buy_weight_sum += key * order_depth.buy_orders[key]
                        #                  tot += order_depth.buy_orders[key]
                        #             best_bid = buy_weight_sum / tot

                        #             tot = 0
                        #             sell_weight_sum = 0
                        #             for key in order_depth.sell_orders.keys():
                        #                  sell_weight_sum += key * order_depth.sell_orders[key]
                        #                  tot += order_depth.sell_orders[key]
                        #             best_ask = sell_weight_sum / tot

                        # if len(order_depth.buy_orders) != 0:
                        #     best_bid = max(order_depth.buy_orders.keys())
                        # mid_price = (best_bid + best_ask) / 2
                        # new_row = {'price' : mid_price}
                        # df.loc[len(df)] = new_row
                        # df
                        for i in range(len(trades)):
                            if trades[i].timestamp != prev_t:
                                new_row = {'price' : trades[i].price}
                                df.loc[len(df)] = new_row
                                prev_t = trades[i].timestamp
                            else:
                                if i < len(trades)-1 and trades[i+1].timestamp == prev_t:
                                    new_row = {'price' : df.loc[len(df)-1] + trades[i].price}
                                    df.loc[len(df)-1] = new_row
                                    count += 1
                                else:
                                    new_row = {'price' : df.loc[len(df)-1] / count}
                                    df.loc[len(df)-1] = new_row
                                    count = 1
                        
                        ema_1000 = df['price'].ewm(span = 10).mean()
                        ema_5000 = df['price'].ewm(span = 50).mean()

                        if len(ema_1000) > 0:
                            best_bid = max(order_depth.buy_orders.keys())
                            best_ask = min(order_depth.sell_orders.keys())
                            if ema_1000[len(ema_1000)-1] > ema_5000[len(ema_5000)-1] and (not cross_up):
                                cross_up = True
                                cross_down = False
                                
                                buy_price = best_ask
                                print("BUY", str(buy_volume) + "x", buy_price)
                                orders.append(Order(product, buy_price, buy_volume))
                            elif ema_1000[len(ema_1000)-1] < ema_5000[len(ema_5000)-1] and (not cross_down):
                                cross_up = False
                                cross_down = True

                                sell_price = best_bid
                                print("SELL", str(sell_volume) + "x", sell_price)
                                orders.append(Order(product, sell_price, buy_volume))

        return result