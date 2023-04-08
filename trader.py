from typing import Dict, List
from datamodel import OrderDepth, Trade, TradingState, Order
import numpy as np
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


class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        
        # Initialize the method output dict as an empty dict
        result = {}
        
        # Initialize the list of Orders to be sent as an empty list
        coco_orders: list[Order] = []
        pina_orders: list[Order] = []
        coco_order_depth: OrderDepth = state.order_depths['COCONUTS']
        pina_order_depth: OrderDepth = state.order_depths['PINA_COLADAS']

        randomNums = np.random.seed(1)
        randomInts = np.random.normal(size = 10000, loc = COCO_PINA_DIFF, scale = 30)
        # # Plot:
        # axis = np.arange(start=min(randomInts), stop = max(randomInts) + 1)
        # plt.hist(randomInts, bins = axis)
        # plt.show()
        left_std_half = np.percentile(randomInts, 40)
        right_std_half = np.percentile(randomInts, 60)
        left_std_one = np.percentile(randomInts, 31)
        right_std_one = np.percentile(randomInts, 69)
        left_std_two = np.percentile(randomInts, 16)
        right_std_two = np.percentile(randomInts, 84)

        # left_std_half = np.percentile(randomInts, 31)
        # right_std_half = np.percentile(randomInts, 69)
        # left_std_one = np.percentile(randomInts, 16)
        # right_std_one = np.percentile(randomInts, 84)
        # left_std_two = np.percentile(randomInts, 5)
        # right_std_two = np.percentile(randomInts, 95)

        coco_mid_price = find_price(coco_order_depth, 'COCONUTS')
        pina_mid_price = find_price(pina_order_depth, 'PINA_COLADAS')
        diff = 0
        if coco_mid_price != -1 and pina_mid_price != -1:
            diff = pina_mid_price - coco_mid_price

        # Find coconut position value
        coco_inventory = pos_val(state.position, 'COCONUTS')
        if 'COCONUTS' in state.position:
            coco_inventory = state.position['COCONUTS']
        # coco_buy_vol = 600 - coco_inventory
        
        # Find pina colada position value
        inventory = pos_val(state.position, 'PINA_COLADAS')
        if 'PINA_COLADAS' in state.position:
            inventory = state.position['PINA_COLADAS']

        pina_buy_price = pina_mid_price# - 1
        pina_sell_price = pina_mid_price# + 1
        coco_buy_price = coco_mid_price #- 1
        coco_sell_price = coco_mid_price# + 1
        if diff >= right_std_two and inventory > -300:
            pina_sell_vol = -300 - inventory
            if abs(pina_sell_vol) > 0:
                print("SELL", str(pina_sell_vol) + "x", pina_sell_price)
                print("hi")
                pina_orders.append(Order('PINA_COLADAS', pina_sell_price, pina_sell_vol))
            coco_buy_vol = 600 - coco_inventory
            if abs(coco_buy_vol) > 0 and coco_inventory < 600:
                print("BUY", str(coco_buy_vol) + "x", coco_buy_price)
                coco_orders.append(Order('COCONUTS', coco_buy_price, coco_buy_vol))
        elif diff >= right_std_one and inventory > -300:
            pina_sell_vol = -150 - inventory
            # pina_sell_vol = int(150 + (0.5 * inventory))
            if abs(pina_sell_vol) > 0:
                print("SELL", str(pina_sell_vol) + "x", pina_sell_price)
                pina_orders.append(Order('PINA_COLADAS', pina_sell_price, pina_sell_vol))
            coco_buy_vol = 300 - coco_inventory
            if abs(coco_buy_vol) > 0 and coco_inventory < 600:
                print("BUY", str(coco_buy_vol) + "x", coco_buy_price)
                coco_orders.append(Order('COCONUTS', coco_buy_price, coco_buy_vol))
        elif diff >= right_std_half and inventory > -300:
            pina_sell_vol = -100 - inventory
            # pina_sell_vol = int(150 + (0.5 * inventory))
            if abs(pina_sell_vol) > 0:
                print("SELL", str(pina_sell_vol) + "x", pina_sell_price)
                pina_orders.append(Order('PINA_COLADAS', pina_sell_price, pina_sell_vol))
            coco_buy_vol = 100 - coco_inventory
            if abs(coco_buy_vol) > 0 and coco_inventory < 600:
                print("BUY", str(coco_buy_vol) + "x", coco_buy_price)
                coco_orders.append(Order('COCONUTS', coco_buy_price, coco_buy_vol))

        elif diff <= left_std_two and inventory < 300:
            pina_buy_vol = 300 - inventory
            if abs(pina_buy_vol) > 0:
                print("BUY", str(pina_buy_vol) + "x", pina_buy_price)
                pina_orders.append(Order('PINA_COLADAS', pina_buy_price, pina_buy_vol))
            coco_sell_vol = -600 - coco_inventory
            if abs(coco_sell_vol) > 0 and coco_inventory > -600:
                print("SELL", str(coco_sell_vol) + "x", coco_sell_price)
                coco_orders.append(Order('COCONUTS', coco_sell_price, coco_sell_vol))
        elif diff <= left_std_one and inventory < 300:
            pina_buy_vol = 150 - inventory
            if abs(pina_buy_vol) > 0:
                print("BUY", str(pina_buy_vol) + "x", pina_buy_price)
                pina_orders.append(Order('PINA_COLADAS', pina_buy_price, pina_buy_vol))
            coco_sell_vol = -300 - coco_inventory
            if abs(coco_sell_vol) > 0 and coco_inventory > -600:
                print("SELL", str(coco_sell_vol) + "x", coco_sell_price)
                coco_orders.append(Order('COCONUTS', coco_sell_price, coco_sell_vol))
        elif diff <= left_std_half and inventory < 300:
            pina_buy_vol = 100 - inventory
            if abs(pina_buy_vol) > 0:
                print("BUY", str(pina_buy_vol) + "x", pina_buy_price)
                pina_orders.append(Order('PINA_COLADAS', pina_buy_price, pina_buy_vol))
            coco_sell_vol = -150 - coco_inventory
            if abs(coco_sell_vol) > 0 and coco_inventory > -600:
                print("SELL", str(coco_sell_vol) + "x", coco_sell_price)
                coco_orders.append(Order('COCONUTS', coco_sell_price, coco_sell_vol))
        
        result['COCONUTS'] = coco_orders
        result['PINA_COLADAS'] = pina_orders
        # logger.flush(state, pina_orders)



        return result