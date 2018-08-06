#PYTHON 3.4
import requests
import json
import base64
import hashlib
import time
import hmac
from exchanges import *
from decimal import Decimal

#Time functions
import schedule
import time
from datetime import datetime

Global_url = 'https://api.bitfinex.com/v1/pubticker/btcusd' 
bitfinexURL = 'https://api.bitfinex.com/v1/balances'
bitfinexKey = 'LLgjPkJMSIfP0Ih3PW93kDoVTGPN54HEecVP8GsBhQR'
bitfinexSecret = b'XaNP7HqpaS6EdS8MTmwU1uWafv8u2UbvE3ZS0xWnmW7' #the b is deliberate, encodes to bytes
CUR = BTC = 0

def start():
    #Declaire array
    rates = []
    exch_name = []
    """
    print("BitFinex")
    payloadObject = {
            'request':'/v2/balances',
            'nonce':str(time.time() * 100000), #convert to string
            'options':{}
    }

    print("")
    print("---------------------------------------------------------------------")
    print("")

    payload_json = json.dumps(payloadObject)
    print("payload_json: ", payload_json)

    print("")
    print("---------------------------------------------------------------------")
    print("")

    payload = base64.b64encode(bytes(payload_json, "utf-8"))
    print("payload: ", payload)

    print("")
    print("---------------------------------------------------------------------")
    print("")

    m = hmac.new(bitfinexSecret, payload, hashlib.sha384)
    m = m.hexdigest()

    #headers
    headers = {
          'X-BFX-APIKEY' : bitfinexKey,
          'X-BFX-PAYLOAD' : base64.b64encode(bytes(payload_json, "utf-8")),
          'X-BFX-SIGNATURE' : m
    }

    r = requests.get(bitfinexURL, data={}, headers=headers)
    print('Response Code: ' + str(r.status_code))
    print('Response Header: ' + str(r.headers))
    print('Response Content: '+ str(r.content))
"""
    par='ltcbtc'
    value = 0

    #CoinDesk
    if (par[:3] == 'btc'):
        value = CoinDesk().get_current_price()
        rates.append(value)
        exch_name.append('CoinDesk')
        #print(par.upper() + ' in CoinDesk = ' + str(value))
               
    #Coinapult - ONLY BITCOIN
    if (par[:3] == 'btc'):
        parCoin = par[3:] + '_' + par[:3]
        parCoin = parCoin.upper()
        Coinapult().init2('https://api.coinapult.com/api/ticker?market=' + parCoin)
        
        #print(par.upper() + ' in Coinapult = ' + str(Coinapult().get_current_price()))

    #Bravenewcoin
    if (par[:3] == 'btc'):
        try:
            BraveNewCoin().init2('https://api.bravenewcoin.com/ticker/bnc_ticker_' + par[:3] + '.json')
            #print(par.upper() + ' in Bravenewcoin = ' + str(BraveNewCoin().get_current_price()))
        except:
            print('BraveNewCoin get rate error!!!')            
    else:
        try:
            BraveNewCoin().init2('https://api.bravenewcoin.com/ticker/bnc_ticker_' + par[:3] + '.json')
            CUR = BraveNewCoin().get_current_price()
            BTC = BraveNewCoin().init2('https://api.bravenewcoin.com/ticker/bnc_ticker_btc.json')
            BTC = BraveNewCoin().get_current_price()
            #print(par.upper() + ' in Bravenewcoin = ' + str(float(CUR)/float(BTC)))
        except:
            print('BraveNewCoin get rate error!!!')
    
    #Bitstamp
    try:
        Bitstamp().init2('https://www.bitstamp.net/api/v2/ticker/' + par)
        value = Bitstamp().get_current_price()
        rates.append(value)
        exch_name.append('Bitstamp')
        #print(par.upper() + ' in Bitstamp = ' + str(value))
    except:
        print('Bitstamp get rate error!!!')
        
    #Bitfinex
    try:
        Bitfinex().init2('https://api.bitfinex.com/v1/pubticker/' + par)
        value = Bitfinex().get_current_price()
        rates.append(value)
        exch_name.append('Bitfinex')
        #print(par.upper() + ' in Bitfinex = ' + str(value))
    except:
        print('Bitfinex get rate error!!!')
        
    #Kraken
    Kraken_PAIR = ''
    if (par=='ethbtc'):
        Kraken_PAIR = 'XETHXXBT'
    elif (par == 'btcusd'):
        Kraken_PAIR = 'XXBTZUSD'
    elif (par == 'ltcbtc'):
        Kraken_PAIR = 'XLTCXXBT'
    if (Kraken_PAIR != ''):
        try:
            Kraken().init2(Kraken_PAIR)
            value = Kraken().get_current_price()
            rates.append(value)
            exch_name.append('Kraken')
            #print(par.upper() + ' in Kraken   = ' + str(value))
        except:
            print('Kraken get rate error!!!')
    #Poloniex
    Pol_PAIR = ''
    if (par=='ethbtc'):
        Pol_PAIR = 'BTC_ETH'
    elif (par=='btcusd'):
        Pol_PAIR = 'USDT_BTC'
    elif (par=='ltcbtc'):
        Pol_PAIR = 'BTC_LTC'
    if (Pol_PAIR != ''):
        try:
            Poloniex().init2(Pol_PAIR)
            value = Poloniex().get_current_price()
            rates.append(value)
            exch_name.append('Poloniex')
            #print(par.upper() + ' in Poloniex = ' + str(value))
        except:
            print('Poloniex get rate error!!!')

    #Check 1% diference
    rate_dif = 0.006
    try:
        if (max(rates)/min(rates)-1 >= rate_dif):
            print('')
            print('<<<<<<<<<<<<< GREAT THAN ' + str(rate_dif * 100 ) + '% >>>>>>>>>>>>>>')
            print('Exchange difference: ' + format(((max(rates)/min(rates)-1)*100), '.2f') + '%')
            print('')
        
            for i, rat in enumerate(rates):
                if (rates[i] == min(rates)):
                    print(exch_name[i] + ': ' + str(rates[i]) + '   BUY')
                elif (rates[i] == max(rates)):
                    print(exch_name[i] + ': ' + str(rates[i]) + '   SELL')
                else:
                    print(exch_name[i] + ': ' + str(rates[i]))
        
            print('')
            print(datetime.now())
            print('')
    except:
        print('No values to return min and max!!!')    
"""
    #data = get_response('https://api.bitfinex.com/v1/pubticker/btcusd')
    print(bitfinex.get_current_price())
    price = data['ticker']['last']
    print(Decimal(price))
"""


schedule.every(5).seconds.do(start)


while 1:
    schedule.run_pending()
    time.sleep(1)

