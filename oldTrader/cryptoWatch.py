# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:48:48 2016

@author: jcobr
"""

import requests
import json
import pickle
import os
import datetime
import httplib
import urllib2

#60 180 300 900 1800 3600 7200 14400 21600 43200 86400 259200 604800

#print cryptoWatch.text
class CryptoWatch:
    def __init__(self, timeStep, readFromFile):
        self.timeStep = timeStep
        self.readFromFile = readFromFile
        self.fileName = "CryptoWatch.dat"
        self.responseDict = dict()
        self.ohlc = dict()
        
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
    def load(self):
        with open(self.fileName, 'rb') as f:
            self.ohlcDict = pickle.load(f)
        self.ohlc = OHLC(self.ohlcDict, self.timeStep)
        
    def update(self):
        try:
            response = urllib2.urlopen('https://cryptowat.ch/kraken/etheur.json').read()
            self.responseDict = json.loads(response.text)
            self.responseDict = self.convertFromUnicode(self.responseDict)
            self.ohlcDict = dict()        
            for tS in self.responseDict:
                self.ohlcDict[tS] = []
                for i in self.responseDict[tS]:
                    split = i.split()    
                    if float(split[1]) > 0:
                        self.ohlcDict[tS].append([datetime.datetime.fromtimestamp(float(split[0])), float(split[1]), float(split[2]), float(split[3]), float(split[4]), float(split[5])])
            with open("cryptoWatch.dat", 'wb') as f:
                pickle.dump(self.ohlcDict, f, 2) 
            self.ohlc = OHLC(self.ohlcDict, self.timeStep)
            
        except httplib.IncompleteRead, e:
            response = e.partial
            print "Incomplete read. Loading last OHLC backup"
            self.load()

    
    
        
        

#if os.path.isfile(fileName):
    
#with open(fileName, 'rb') as f:
#    cryptoDB = pickle.load(f)

class OHLC:
    def __init__(self, data, timeStep):
        self.dateTime = list()
        self.openPrice = list()
        self.highPrice = list()
        self.lowPrice = list()
        self.closePrice = list()
        self.volume = list()        
        
        for i in data[timeStep]:
            self.dateTime.append(i[0])
            self.openPrice.append(i[1])
            self.highPrice.append(i[2])
            self.lowPrice.append(i[3])
            self.closePrice.append(i[4])
            self.volume.append(i[5])