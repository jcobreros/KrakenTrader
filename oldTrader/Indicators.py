# -*- coding: utf-8 -*-
"""
Created on Thu Jul 07 15:17:01 2016

@author: jcobr
"""
import datetime
from pylab import *

    
class MACD:
    def __init__(self, period1, period2, period3, data):
        self.dateTime = data.dateTime        
        self.movingAverage1 = DEMA(data.closePrice, data.dateTime, period1)
        self.movingAverage2 = DEMA(data.closePrice, data.dateTime, period2)
        
        self.macd = list()        
        self.signal = list()
        self.histogram = list()
        
        self.macd = [a-b for a,b in zip(self.movingAverage2,self.movingAverage1)]
        self.signal = DEMA(self.macd, data.dateTime, period3)
        
        self.histogram = [a-b for a,b in zip(self.macd,self.signal)]
        self.filteredHistogram = DEMA(self.histogram, self.dateTime, 5)

def Derivative(data, dtime):
    derivative = list()
    derivative.append(0)
    for i in range(1, len(data)):
        delta = data[i] - data[i-1]
        dT = datetime.timedelta.total_seconds(dtime[i] - dtime[i-1])       
        derivative.append(delta/dT)  
    return derivative
        
def MovingAverage(data, dtime, period):
    movingAverage = list()
    movingAverage.append(data[0])
    for i in range(1, len(data)):
        dT = datetime.timedelta.total_seconds(dtime[i] - dtime[i-1])
        factor = 1 - math.exp(- dT / period)
        movingAverage.append((1-factor) * movingAverage[i-1] + factor * data[i])
    return movingAverage

def DEMA(data, dtime, period):
    movingAverage = MovingAverage(data, dtime, period)
    secondMovingAverage = MovingAverage(movingAverage, dtime, period)
    dema = [2*a-b for a,b in zip(movingAverage,secondMovingAverage)]
    return dema