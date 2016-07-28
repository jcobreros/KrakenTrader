"""Ticker model"""

import time

# get all the SA stuff
from models import sa, sao, sasql, sad, hybrid_property

# and the rest
from models import DeclarativeBase, metadata 

__all__ = ['Ticker']


########################################################################
class Ticker(DeclarativeBase):
    """The model for Ticker data"""
    __tablename__ = 'ticker'

    timestamp = sa.Column(sa.Integer, primary_key=True)
    open = sa.Column(sa.Float)
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    vwap = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    numberOfTrades = sa.Column(sa.Float)
    ask = sa.Column(sa.Float)
    bid = sa.Column(sa.Float)

    def parseKrakenToTicker(self, krakenResponse):
        self.timestamp = int(time.time())

        #<pair_name> = pair name
            #a = ask array(<price>, <whole lot volume>, <lot volume>),
            #b = bid array(<price>, <whole lot volume>, <lot volume>),
            #c = last trade closed array(<price>, <lot volume>),
            #v = volume array(<today>, <last 24 hours>),
            #p = volume weighted average price array(<today>, <last 24 hours>),
            #t = number of trades array(<today>, <last 24 hours>),
            #l = low array(<today>, <last 24 hours>),
            #h = high array(<today>, <last 24 hours>),
            #o = today's opening price
        self.open = krakenResponse['result']['XETHZEUR']['o']
        self.high = krakenResponse['result']['XETHZEUR']['h']
        self.low = krakenResponse['result']['XETHZEUR']['l']
        self.close = krakenResponse['result']['XETHZEUR']['c']
        self.vwap = krakenResponse['result']['XETHZEUR']['p']
        self.volume = krakenResponse['result']['XETHZEUR']['v']
        self.numberOfTrades = krakenResponse['result']['XETHZEUR']['t']
        self.ask = krakenResponse['result']['XETHZEUR']['a']
        self.bid = krakenResponse['result']['XETHZEUR']['b']