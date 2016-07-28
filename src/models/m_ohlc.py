"""Ohlc model"""

# get all the SA stuff
from models import sa, sao, sasql, sad, hybrid_property

# and the rest
from models import DeclarativeBase, metadata 

__all__ = ['Ohlc']


########################################################################
class Ohlc(DeclarativeBase):
    """The model for Ohlc data"""
    __tablename__ = 'ohlc'

    timestamp = sa.Column(sa.Integer, primary_key=True)
    open = sa.Column(sa.Float)
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    vwap = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    count = sa.Column(sa.Float)

    def parseKrakenToOhlc(self, krakenResponse):
        return ""