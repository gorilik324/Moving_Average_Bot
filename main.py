import MetaTrader5 as mt
import pandas as pd

def cal_sma(symbol, period, timeframe):
    bars_d = mt.copy_rates_from_pos(symbol, timeframe, 1, period)
    bars_df = pd.DataFrame(bars_d)

    last_close = bars_df.iloc[-1].close
    last_low = bars_df.iloc[-2].low
    last_high = bars_df.iloc[-2].high
    sma = bars_df.close.mean()

    if last_close > sma:
        direction = "buy"
    elif last_close < sma:
        direction = "sell"

    return direction, sma, last_close, last_low, last_high

def open_order(symbol, direction, volume, deviation, sl, tp_per):
    
    price_tick = mt.symbol_info_tick(symbol)

    if direction == "buy":
        price_tick = price_tick.ask
        type_order = 0
        tp = ((price_tick - sl) * tp_per) + price_tick
    elif direction == "sell":
        price_tick = price_tick.bid
        type_order = 1
        tp = ((sl - price_tick) * tp_per) + price_tick
    
    request = {
        "action": mt.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": type_order,
        "price": price_tick,
        "deviation": deviation,
        "magic": 100,
        "tp"   : tp,
        "sl"   : sl,
        "comment": "Placing Order",
        "type_time": mt.ORDER_TIME_GTC,
        "type_filling": mt.ORDER_FILLING_IOC,
    }
    order_result = mt.order_send(request)
    print(order_result)

    return order_result

SYMBOL = "EURUSD"
TIMEFRAME = mt.TIMEFRAME_M1
VOLUME = 1.0
SMA = 200
DEVIATION = 29
TP_PER = 1.3

Login = 0
Password = ""
Server = ""

mt.initialize(login = Login, password = Password, server = Server)

#while True:
direction, sma, last_close, last_low, last_high = cal_sma(SYMBOL, SMA, TIMEFRAME)

num_positions = mt.positions_total()
if num_positions <=0 :
    open_orders = True
elif num_positions > 0:
    open_orders = False

if open_orders:
    if direction == "buy":
        open_order(SYMBOL, direction, VOLUME, DEVIATION, last_low, TP_PER)
    elif direction == "sell":
        open_order(SYMBOL, direction, VOLUME, DEVIATION, last_high, TP_PER)

print(f"No. of Positions (OPENED): {num_positions}")
print(f"Symbol: {SYMBOL}")
print(f"Direction: {direction}")
print(f"SMA: {sma}")
print(f"Last_close: {last_close}")
print("------------------------------")