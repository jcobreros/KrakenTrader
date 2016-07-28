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
    high_last24 = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    low_last24 = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    close_lotvol = sa.Column(sa.Float)
    vwap = sa.Column(sa.Float)
    vwap_last24 = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    volume_last24 = sa.Column(sa.Float)
    numberOfTrades = sa.Column(sa.Float)
    numberOfTrades_last24 = sa.Column(sa.Float)
    ask = sa.Column(sa.Float)
    ask_wlotvol = sa.Column(sa.Float)
    ask_lotvol = sa.Column(sa.Float)
    bid = sa.Column(sa.Float)
    bid_wlotvol = sa.Column(sa.Float)
    bid_lotvol = sa.Column(sa.Float)

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
        self.high = krakenResponse['result']['XETHZEUR']['h'][0]
        self.high_last24 = krakenResponse['result']['XETHZEUR']['h'][1]
        self.low = krakenResponse['result']['XETHZEUR']['l'][0]
        self.low_last24 = krakenResponse['result']['XETHZEUR']['l'][1]
        self.close = krakenResponse['result']['XETHZEUR']['c'][0]
        self.close_lotvol = krakenResponse['result']['XETHZEUR']['c'][1]
        self.vwap = krakenResponse['result']['XETHZEUR']['p'][0]
        self.vwap_last24 = krakenResponse['result']['XETHZEUR']['p'][1]
        self.volume = krakenResponse['result']['XETHZEUR']['v'][0]
        self.volume_last24 = krakenResponse['result']['XETHZEUR']['v'][1]
        self.numberOfTrades = krakenResponse['result']['XETHZEUR']['t'][0]
        self.numberOfTrades_last24 = krakenResponse['result']['XETHZEUR']['t'][1]
        self.ask = krakenResponse['result']['XETHZEUR']['a'][0]
        self.ask_wlotvol = krakenResponse['result']['XETHZEUR']['a'][1]
        self.ask_lotvol = krakenResponse['result']['XETHZEUR']['a'][2]
        self.bid = krakenResponse['result']['XETHZEUR']['b'][0]
        self.bid_wlotvol = krakenResponse['result']['XETHZEUR']['b'][1]
        self.bid_lotvol = krakenResponse['result']['XETHZEUR']['b'][2]