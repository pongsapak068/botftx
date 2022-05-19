from re import X
import ccxt
import pandas as pd
import numpy as np
from urllib3 import Retry
import time

pair  = 'SRM-PERP'
asset = 360
hedgratio = 0.1


ftx = ccxt.ftx({
    'api_key' : '',
    'secret' : ''})
ftx.headers = {'FTX-SUBACCOUNT':'Rb'}


def get_price ():
    price = ftx.fetch_ticker(pair)['last']
    return price
def get_myorder():
    myorder = float("{0:.2f}".format(ftx.fetch_my_trades(pair)[-1]['price']))
    return myorder
def get_assetvalue():
    assetvalue = (asset*get_price())
    return assetvalue 
def get_x ():
    x = hedgratio*get_assetvalue()
    return x
def get_minsize():
    minsize = ftx.fetch_ticker(pair)['info']['minProvideSize']
    return minsize
def get_order():
    x_myorder = float((get_myorder()*asset)*hedgratio)
    price_sell = get_myorder()+0.04
    price_buy = get_myorder()-0.04
    assetvalue_buy = (price_buy*asset)*hedgratio
    assetvalue_sell = (price_sell*asset)*hedgratio
    x_buy = float("{0:.2f}".format((x_myorder-assetvalue_buy)/price_buy))
    x_sell = float("{0:.2f}".format((assetvalue_sell-x_myorder)/price_sell))
    return x_buy,x_sell,price_buy,price_sell,x_myorder

def get_count_order():
    open_order = ftx.fetch_open_orders(pair)
    count_order = len(open_order)
    return count_order

def get_fundingrate():
    funding = pd.DataFrame(ftx.fetch_funding_rate_history(pair),
                           columns=['symbol','timestamp','info','fundingRate'])
    funding['timestamp'] = pd.to_datetime(funding['timestamp'],unit='ms')
    future = []
    for i in range(len(funding)):
        future.append((funding['info'][i]['future']))
    funding['info'] = future
    return funding
def history():
    my_order = pd.DataFrame(ftx.fetch_my_trades(pair),
                            columns=['id','timestamp','symbol','side','amount','price'])
    my_order['timestamp'] = pd.to_datetime(my_order['timestamp'],unit='ms')
    return my_order
def trade():
    trade = pd.DataFrame(ftx.fetch_open_orders(pair),
                         columns=['id','timestamp','symbol','type','side','amount','price','status'])
    trade['timestamp'] = pd.to_datetime(trade['timestamp'],unit='ms')
    return trade

while True:
    x_buy,x_sell,price_buy,price_sell,x_myorder = get_order()
    count_order = get_count_order()
    my_order = get_myorder()
    if count_order >0 and count_order !=2 :
            ftx.cancel_all_orders(pair)
            ftx.create_limit_buy_order(pair,x_buy,price_buy)
            ftx.create_limit_sell_order(pair,x_sell,price_sell)
            print("11111")
    elif count_order == 0:   
        ftx.create_limit_buy_order(pair,x_buy,price_buy)
        ftx.create_limit_sell_order(pair,x_sell,price_sell)
        print("22222")
    else:
        print("--------")
    time.sleep(10)
