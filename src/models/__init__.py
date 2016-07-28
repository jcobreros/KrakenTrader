"""SQLAlchemy models for the application

In a smaller application you could have all models in this file, but we 
assumed this will grow and have there split things up, in which case you 
should import your sub model at the bottom of this module.
"""

import sys
import sqlalchemy as sa
import sqlalchemy.orm as sao
import sqlalchemy.sql as sasql
import sqlalchemy.ext.declarative as sad
from sqlalchemy.ext.hybrid import hybrid_property

maker = sao.sessionmaker(autoflush=True, autocommit=False)
DBSession = sao.scoped_session(maker)
DeclarativeBase = sad.declarative_base()
metadata = DeclarativeBase.metadata

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine)

# you could have your models defined within this module, for larger applications it is
# probably nicer to have them in separate modules and import them as shown below.
#
# remember to define __ALL__ in each module

# Import your model modules here.
from models.m_ohlc import *
from models.m_ticker import *