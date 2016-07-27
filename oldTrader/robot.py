# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:15:06 2016

@author: jcobreros
"""
from numpy import *
import datetime

        
class Robot:
    def __init__(self, ohlc, macd, assets, asset1Name, asset2Name, kr, timeStep):
        self.assets = assets        
        self.asset1 = self.assets[asset1Name]
        self.asset2 = self.assets[asset2Name]
        self.asset1Name = asset1Name        
        self.asset2Name = asset2Name
        self.ohlc = ohlc
        self.macd = macd
        self.orderTriggers = list()
        self.makerFee = 0.26 / 100
        self.takerFee = 0.16 / 100
        self.lastOperation = []
        self.confirmedOrders = list()
        self.kr = kr
        self.balance = []
        self.timeStep = timeStep
        
    def Run(self):
        self.macdMaximumTriggers()
        
        self.assets = self.kr.QueryPrivate('Balance', {})['result']   
        self.asset1 = self.assets[self.asset1Name]
        self.asset2 = self.assets[self.asset2Name]
        print "Assets: " + str(self.assets)
        
        self.orders = self.kr.QueryPrivate('OpenOrders', {})['result']['open']
        print "Open Orders: " + str(self.orders)
        
        lastTrigger = self.orderTriggers[-1]
        dT = datetime.timedelta.total_seconds(self.macd.dateTime[-1] - lastTrigger[1])
        print datetime.datetime.now(), str(dT) + "s since " + str(lastTrigger)
        
        if (dT < 3*self.timeStep):
            if lastTrigger[0] == 'Sell':
                if self.asset1 > 0:                   
                    for txid in self.orders:
                        print txid
                        print "Clearing orders"
                        response = self.kr.QueryPrivate('CancelOrder', {'txid' : txid})
                        print response
                    print "Place sell order"
                    print self.kr.QueryPrivate('AddOrder', {'pair': 'ETHEUR',
                             'type': 'sell',
                             'ordertype': 'market',
                             'price': str(lastTrigger[2]),
                             'volume': str(self.asset1)})
                else:
                    print "Can't sell. Have nothing"
            
            if lastTrigger[0] == 'Buy':
                if self.asset2 > 0:                   
                    for txid in self.orders:
                        print txid
                        print "Clearing orders"
                        response = self.kr.QueryPrivate('CancelOrder', {'txid' : txid})
                        print response
                    print "Place buy order"
                    print self.kr.QueryPrivate('AddOrder', {'pair': 'ETHEUR',
                             'type': 'buy',
                             'ordertype': 'market',
                             'price': str(lastTrigger[2]),
                             'volume': str(self.asset2 / lastTrigger[2])})
                else:
                    print "Can't buy. Have no money"
                    
        
    def Backtest(self): 
        self.macdMaximumTriggers()
        
        self.confirmedOrders = list()
        self.initialBalance = self.asset1 * self.ohlc.closePrice[0] + self.asset2
        for order in self.orderTriggers:
            if order[0] == 'Sell':
                if self.asset1 > 0:
                    ammountToSell = self.asset1# / 2
                    fee = (ammountToSell * order[2]) * self.makerFee
                    if True:#order[2] > self.lastOperation[1] + self.makerFee:
                        gain = (ammountToSell * order[2]) - fee
                        self.asset2 = self.asset2 + gain
                        self.lastOperation = ['Sell', order[1], order[2], ammountToSell]
                        self.confirmedOrders.append(self.lastOperation)
                        #print str(order[1]) + " Sold " + str(ammountToSell) + self.asset1Name + \
                        " at " + str(order[2]) +  self.asset2Name + \
                        " Got: " + str(gain) + self.asset2Name + \
                        " Paid: " + str(fee) + self.asset2Name + " fee"
                        self.asset1 = self.asset1 - ammountToSell
            if order[0] == 'Buy':
                if self.asset2 > 0:
                    ammountToBuy = self.asset2# / 2
                    fee = (ammountToBuy / order[2]) * self.takerFee
                    if True:#order[2] + self.makerFee< self.lastOperation[1]:
                        gain = (ammountToBuy / order[2]) - fee
                        self.asset1 = self.asset1 + gain
                        self.lastOperation = ['Buy', order[1], order[2], ammountToBuy]
                        self.confirmedOrders.append(self.lastOperation)
                        #print str(order[1]) + " Bought " + str(gain) + self.asset1Name + \
                        " at " + str(order[2]) +  self.asset2Name + \
                        " Paid: " + str(ammountToBuy) + self.asset2Name + \
                        " Paid: " + str(fee) + self.asset1Name + " fee"
                        self.asset2 = self.asset2 - ammountToBuy
            #print "Balance: " + str(self.asset1) + self.asset1Name + ", " + str(self.asset2) + self.asset2Name
        #print len(self.orderTriggers)
            self.balance.append(self.asset1 * self.ohlc.closePrice[-1] + self.asset2)
        self.totalBackTestTime = (datetime.timedelta.total_seconds(self.macd.dateTime[-1] - self.macd.dateTime[0])) / (24 * 3600)
        #self.performance = (((self.balance[-1] / self.initialBalance) - 1) / self.totalBackTestTime ) * 100;
        self.performance = (self.balance[-1] / self.initialBalance)
            #print self.balance
    
        
    def macdMaximumTriggers(self):
        startAt = 10
        from scipy.signal import argrelmax
        
        triggerIndices = argrelmax(absolute(array(self.macd.filteredHistogram)))[0]
        minimumMax = 0.0  
        for i in triggerIndices:
            if i > startAt:
                if self.macd.histogram[i] > 0 and self.macd.histogram[i] > minimumMax:
                    self.orderTriggers.append(['Sell', self.ohlc.dateTime[i], self.ohlc.closePrice[i]])  
                elif self.macd.histogram[i] < 0 and self.macd.histogram[i] < - minimumMax:
                    self.orderTriggers.append(['Buy', self.ohlc.dateTime[i], self.ohlc.closePrice[i]])
        
    def macdCrossoverTriggers(self):
        startAt = 10
        if self.macd.histogram[startAt] >= 0:
            histogramSign = 1
        else:
            histogramSign = -1
        for i in range(startAt+1, len(self.macd.histogram)):
            if self.macd.histogram[i] > 0 and histogramSign < 0:
                histogramSign = 1
                self.orderTriggers.append(['Buy', self.ohlc.dateTime[i], self.ohlc.closePrice[i]])            
            elif self.macd.histogram[i] < 0 and histogramSign > 0:
                histogramSign = -1
                self.orderTriggers.append(['Sell', self.ohlc.dateTime[i], self.ohlc.closePrice[i]])
        
