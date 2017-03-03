from ryan_tools import *
import json
import urllib
import time
import sqlite3

def get_data( ticker, exchange = 'NSE' ):
    
    request_string = 'http://finance.google.com/finance/info?client=ig&q=' + exchange.upper() + ':' + ticker
    data = urllib.request.urlopen(request_string)
    data = data.read().decode()
    data = json.loads(data[4:-1])
    frame = pd.DataFrame(data, index = ['Values'])
    frame2 = pd.DataFrame( data = frame.loc['Values'], columns = ['Values'], index = frame.columns )
    return frame2

def price(ticker, exchange = 'NSE' ):
    data = get_data(ticker, exchange )
    return data.loc['l'][0]

def ah_price(ticker, exchange = 'NSE' ):
    data = get_data(ticker, exchange )
    return data.loc['el'][0]

def dividend_count(ticker, exchange = 'NSE'):
    data = get_data(ticker, exchange )
    if data.loc['yld'][0] == '':
        return 0
    percent = float(data.loc['yld'][0])
    price = float(data.loc['l'][0])
    amount = float(data.loc['div'][0])
    ratio = (amount/price) * 100.00
    return percent/ratio

def divident_ratio(ticker, exchange ):
    
    return 0

def get_connections():
    conn = sqlite3.connect('main.db')
    c = conn.cursor()
    return conn, c

def get_table_names():
    conn, c = get_connections()
    tables = pd.read_sql('SELECT name FROM sqlite_master where type = \'table\'', conn )
    conn.close()
    return tables


def save_data( data ):
    conn, c = get_connections()

    ticker = str(data.loc['t'][0])
    date = str(data.loc['lt'][0])
    price = str(data.loc['l'][0])
    try:
        ah_price = str(data.loc['el'][0])
    except KeyError:
        ah_price = price
    print(ticker,' ', date,' ', price,' ', ah_price )
    tables = pd.read_sql('SELECT name FROM sqlite_master where type = \'table\'', conn )
    if ticker not in tables['name'].values:
        command = 'CREATE TABLE ' + ticker + ' ( date, price, ah_price )'
        c.execute(command)
    
    command = 'INSERT INTO ' + ticker + ' VALUES (\'' + date + '\',' + price  + ' , ' + ah_price + ' ) '
    
    c.execute( command )

    conn.commit()
    conn.close()

def monitor_stock(ticker):
    while True:
        data = get_data(ticker)
        save_data(data)
        time.sleep(60)


    
print('What stock should I monitor?')
ticker = input()
monitor_stock( ticker )

