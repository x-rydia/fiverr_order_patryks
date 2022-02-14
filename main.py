
from binance import Client
from config import *
from pandas import DataFrame
from time import sleep, time
from datetime import datetime
from ta.volatility import (
    bollinger_hband, 
    bollinger_lband
)
from ta.momentum import (
    rsi
)
from ta.volume import (
    chaikin_money_flow
)
from ta.trend import (
    _sma
)


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
    #APPLY INDICATORS TO THE DATAFRAME
    for d in df_hist:
        #If you would like a detailed explanaiton of what is going on here and why
        #I use the indicators that I use together, please contact me.
        d['HBB'] = bollinger_hband(d[4], fillna=True)
        d['LBB'] = bollinger_lband(d[4], fillna=True)
        d['RSI'] = rsi(d[4], fillna=True)
        d['CMF'] = chaikin_money_flow(d[2], d[3], d[4], d[5], fillna=True)
        d['SMA'] = _sma(d[4], 10, fillna=True)
    
    while True:
        cycle_no = 0
        for p in PAIRS:
            cur_price = CLI.get_avg_price(p)
            b_score = 0
            s_score = 0
            
            if cur_price >= d['HBB'][-1]:
                s_score += 1
            
            if d['RSI'][-1] <= 70:
                s_score += 1
            
            if d['SMA'][-1] >= cur_price * 1.05:
                s_score += 1
            
            if d['CMF'][-1] >= 0:
                s_score += 1
            
            if cur_price >= d['LBB'][-1]:
                b_score += 1
            
            if d['RSI'][-1] <= 30:
                b_score += 1
            
            if d['CMF'][-1] <= 0:
                b_score += 1
            
            if d['SMA'] >= cur_price * 1.05:
                b_score += 1
            
            if b_score >= 3 and s_score == 0:
                try:
                    CLI.order_market_buy(
                        p,
                        QUANTITY_UNIT
                    )
                    print(f'ATTEMPTED BUY {p}')
                except:
                    print(f'FAILED TO BUY {p}')
            
            if s_score >= 3 and b_score == 0:
                try:
                    CLI.order_market_sell(
                        p,
                        QUANTITY_UNIT
                    )
                    print(f'ATTEMPTED SELL {p}')
                except:
                    print(f'FAILED TO SELL {p}')
            print(f'''
                        CYCLE SUMMARY
                ___________________________
                CYCLE SUMMARY NO: {cycle_no}
                FOR TICKER: {p}
                BUY SCORE: {b_score}
                SELL SCORE: {s_score}
                
                *** IF LIMITED ACTIVITY DUE TO LOW 
                VOLATILITY, CHANGE THE loop_frequency 
                TO A LOWER VALUE ***
                ____________________________
            ''')
        sleep(loop_frequency)


if __name__ == '__main__':
    main(.5)