"""Ticker model"""

# get all the SA stuff
from models import sa, sao, sasql, sad, hybrid_property

# and the rest
from models import DeclarativeBase, metadata 

__all__ = ['Ticker']


########################################################################
class Ticker(DeclarativeBase):
    """The model for Ticker data"""
    __tablename__ = 'ticker'

    timestamp = sa.Column(sa.DateTime, primary_key=True)
    open = sa.Column(sa.Float)
    high = sa.Column(sa.Float)
    low = sa.Column(sa.Float)
    close = sa.Column(sa.Float)
    vwap = sa.Column(sa.Float)
    volume = sa.Column(sa.Float)
    numberOfTrades = sa.Column(sa.Float)
    ask = sa.Column(sa.Float)
    bid = sa.Column(sa.Float)