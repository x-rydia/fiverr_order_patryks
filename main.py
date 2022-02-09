'''
File for the bulk of script execution. Please fill out config fully 
before running, or else it will simply execute the unit tests. 
'''
from binance import Client
from matplotlib.pyplot import fill, hist
from config import *
from pandas import DataFrame
from time import sleep, time
from datetime import datetime
from ta.volatility import bollinger_hband, bollinger_lband

def set_ticks():
    CLI = Client(KEY, SEC)

def main(loop_frequency: float, test: bool=False) -> None:
    '''
    main file to trade off of the bollinger bands. 
    Starts an event loop with period :loop_frequency: 
    which is a number of seconds
    '''
    CLI = Client(KEY, SEC)

    #Step one, get historical data
    hist_df =[]
    for p in PAIRS: 
        hist_df.append(
            CLI.get_klines(
                symbol=p,
                interval=CLI.KLINE_INTERVAL_3MINUTE,
                limit=100
            )
        )
    df_hist = [DataFrame(h) for h in hist_df]
    candle_id = 0
    for j in range(len(hist_df)):
        for i in range(len(hist_df[j])):
            print(f''' 
                TICKER: {PAIRS[j]}
                CANDLE NUMBER: {candle_id}
                OPEN TIME: {datetime.fromtimestamp(hist_df[j][i][0] / 1000)}
                OPEN PRICE: {hist_df[j][i][1]}
                HIGH PRICE: {hist_df[j][i][2]}
                LOW PRICE: {hist_df[j][i][3]}
                CLOSE PRICE: {hist_df[j][i][4]}
                VOLUME: {hist_df[j][i][5]}
            ''')
            candle_id += 1
        candle_id = 0

    for d in df_hist:
        d['HBB'] = bollinger_hband(d[4], fillna=True)
        d['LBB'] = bollinger_lband(d[4], fillna=True)
    
    while True:
        for p in PAIRS:
            cur_price = CLI.get_avg_price(p)
            if cur_price >= d['HBB'][-1]:
                CLI.options_place_order(
                    symbol=p,
                    side=CLI.SIDE_SELL,
                    type=CLI.FUTURE_ORDER_TYPE_MARKET,
                    quantity=QUANTITY_UNIT
                )
                print(f'SOLD {QUANTITY_UNIT} of: {p}')

            elif cur_price <= d['LBB'][-1]:
                CLI.options_place_order(
                    symbol=p,
                    side=CLI.SIDE_BUY,
                    type=CLI.FUTURE_ORDER_TYPE_MARKET,
                    quantity=QUANTITY_UNIT
                )
                print(f'BUY {QUANTITY_UNIT} of: {p}')

            else:
                pass
        
        sleep(loop_frequency)



if __name__ == '__main__':
    # main(60, test=True)
    # main(60, test=False)
    main(1)