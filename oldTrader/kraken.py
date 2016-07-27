# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 20:39:16 2016

@author: jcobreros
"""
import krakenex
import datetime
import math

class Kraken:
    def __init__(self):
        self.k = krakenex.API()
        self.k.load_key('kraken.key')
        
    def convertFromUnicode(self, input):
        if isinstance(input, dict):
            return {self.convertFromUnicode(key): self.convertFromUnicode(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.convertFromUnicode(element) for element in input]
        elif isinstance(input, unicode):
            val = input.encode('utf-8')
            try:
                return float(val)
            except:
                return val
        else:
            return input
            
    def QueryPublic(self, method, parameters):
        unicodeJson = self.k.query_public(method, parameters)
        response = self.convertFromUnicode(unicodeJson)
        return response
        
    def QueryPrivate(self, method, parameters):
        unicodeJson = self.k.query_private(method, parameters)
        response = self.convertFromUnicode(unicodeJson)
        return response
        
    
        
class OHLC:
    def __init__(self, currency, data):
        self.dateTime = list()
        self.openPrice = list()
        self.highPrice = list()
        self.lowPrice = list()
        self.closePrice = list()
        self.volume = list()
        
        if len(data['error']) > 0:
            print data['error']
            self.dateTime = [0]
            self.openPrice = [0]
            self.highPrice = [0]
            self.lowPrice = [0]
            self.closePrice = [0]
            self.volume = [0]
        else:
            for i in data["result"][currency]:
                self.dateTime.append(datetime.datetime.fromtimestamp(i[0]))
                self.openPrice.append(i[1])
                self.highPrice.append(i[2])
                self.lowPrice.append(i[3])
                self.closePrice.append(i[4])
                self.volume.append(i[6])
            


def tickerTest():
    import time
    print "Hello"
    kr = Kraken()
    
    ask = []
    bid = []
    close= []
    
    while True:
        ticker = kr.QueryPublic('Ticker', {'pair': 'ETHEUR'})['result']['XETHZEUR']
        ask.append(ticker['a'][0])
        bid.append(ticker['b'][0])
        close.append(ticker['c'][0])    
        time.sleep(3)

         
#k.query_private('AddOrder', {'pair': 'XXBTZEUR',
#                             'type': 'buy',
#                             'ordertype': 'limit',
#                             'price': '1',
#                             'volume': '1',
#                             'close[pair]': 'XXBTZEUR',
#                             'close[type]': 'sell',
#                             'close[ordertype]': 'limit',
#                             'close[price]': '9001',
#                             'close[volume]': '1'})
            