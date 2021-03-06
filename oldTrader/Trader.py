#!/usr/bin/env python2

# This file is part of krakenex.
# Licensed under the Simplified BSD license. See examples/LICENSE.

# Demonstrates how to use the conditional close functionality; that is,
# placing an order that, once filled, will place another order.
#
# This can be useful for very simple automation, where a bot is not
# needed to constantly monitor execution.

print "Importing"

import ast
import json
import pprint
import numpy as np
from matplotlib.lines import Line2D
import pickle
from kraken import *
from robot import *
import cryptoWatch
from charts import *
from Indicators import MACD
import Indicators

readFromFile = False
fileName = "ohlc.dat"

print "Loading Kraken"
kr = Kraken()

#60 180 300 900 1800 3600 7200 14400 21600 43200 86400 259200 604800
#1  3   5   15  30   60   120  240   360   720   1440  4320   10800
#                    1    2    4     6     12    24    72     168
#                                                1     3      7
timeStep= 300
cr = cryptoWatch.CryptoWatch(timeStep, False)


if readFromFile:
    with open(fileName, 'rb') as f:
        response = pickle.load(f)
else:
    with open(fileName, 'wb') as f:
        response = kr.QueryPublic('OHLC', {'pair': 'ETHEUR', 'interval' : 5})
        pickle.dump(response, f)


ohlc = OHLC('XETHZEUR', response)
#assetResponse = kr.QueryPrivate('Balance', {})
assets = {'ZEUR': 0.0, 'XETH': 1.0038386}
#assets = assetResponse['result']
#response = kr.QueryPublic('Depth', {'pair': 'ETHEUR'})
#response = kr.QueryPrivate('OpenOrders', {})['result']['open']
#print response

#cr.update()

#macd = MACD(26*timeStep, 10*timeStep, 9*timeStep, cr.ohlc)

results = []
balance = []
def backTest(f1, ohlc, assets, kr):            
    macd = MACD(f1*0.26*timeStep, f1*0.10*timeStep, f1*0.09*timeStep, ohlc)
    robot = Robot(ohlc, macd, assets, 'XETH', 'ZEUR', kr, timeStep)
    robot.Backtest()

    return [f1, robot.balance[-1]]

from joblib import Parallel, delayed
import multiprocessing
    
# what are your inputs, and what operation do you want to 
# perform on each input. For example...


def optimize():
    inputs = range(1, 200, 1)
    num_cores = multiprocessing.cpu_count()    
    results = Parallel(n_jobs=num_cores)(delayed(backTest)(i, ohlc, assets, kr) for i in inputs)
    #print results

    maxValue = 0
    maxIndex = 0
    for i in range(len(results)):
        if results[i][1] > maxValue:
            maxIndex = i
            maxValue = results[i][1]
    print "Optimal: " + str(results[maxIndex])
    factor1 = results[maxIndex][0]
    return factor1

if __name__ == '__main__':
    #factor1 = optimize()  
    factor1 = 91
    
    #macd = MACD(0.26*factor1*timeStep, 0.10*factor1*timeStep, 0.09*factor1*timeStep, ohlc)

    #robot = Robot(ohlc, macd, assets, 'XETH', 'ZEUR', kr, timeStep)
    #robot.Backtest()
    #balance = robot.balance
    fig = prepareCharts()
    #printCharts(ohlc, macd, robot, fig)
    #print robot.initialBalance, robot.balance[-1], robot.performance    
    
    #derivative1 = Indicators.Derivative(macd.movingAverage1, macd.dateTime)
    #derivative2 = Indicators.Derivative(macd.movingAverage2, macd.dateTime)
    
    ask = []
    bid = []
    close= []
    
    loopRobot = True
    import time, threading
    def runRobot():
        #cr.update()
        print "Running robot"
        response = kr.QueryPublic('OHLC', {'pair': 'ETHEUR', 'interval' : 5})
        if len(response['error']) == 0:
            ohlc = OHLC('XETHZEUR', response)
            print str(len(ohlc.dateTime)) + " values. Data from " + str(ohlc.dateTime[0]) + " to " + str(ohlc.dateTime[-1])
            ticker = kr.QueryPublic('Ticker', {'pair': 'ETHEUR'})
            if len(ticker['error']) == 0:
                ticker = ticker['result']['XETHZEUR']
                print ticker
                
                ask.append(ticker['a'][0])
                bid.append(ticker['b'][0])
                close.append(ticker['c'][0])
                
                spread = ask[-1] - bid[-1]
                print "Spread " + str(spread)
                with open("ticker.csv", "a") as myfile:
                    line = str(datetime.datetime.now()) + ";" + str(ask[-1]) + ";" + str(bid[-1]) + ";" + str(close[-1]) + "\n"        
                    myfile.write(line)
        
                #print ticker
                
                macd = MACD(0.26*factor1*timeStep, 0.10*factor1*timeStep, 0.09*factor1*timeStep, ohlc)
                robot = Robot(ohlc, macd, assets, 'XETH', 'ZEUR', kr, timeStep)
                robot.Run()
                printCharts(ohlc, macd, robot, fig)
        
        if loopRobot:
            threading.Timer(30, runRobot).start()
    
    runRobot()
    
