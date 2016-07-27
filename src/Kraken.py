# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 18:22:27 2016

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