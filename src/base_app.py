"""base_app for KrakenTrader"""

import sys
import os
baseDir, f = os.path.split(__file__)
projectDir, projectFolder = os.path.split(baseDir)
dataFolder = os.path.join(projectDir, 'data')

# logging
import logging, logging.config
logSQLFile = os.path.join(baseDir, 'sqllog.txt')
logConfigFile = os.path.join(baseDir, 'logging.conf')
if os.path.exists(logConfigFile):
    # load config from config file, see logging.conf for configuration settings
    logging.config.fileConfig(logConfigFile)
else:
    # or just do a basic config
    format = '%(name)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'
    logging.basicConfig(format=format, level=logging.NOTSET)

log = logging.getLogger(__package__)
log.debug("logging is setup")

import models as db
log.debug("db import")

from sources.s_kraken import *
log.debug("kraken import")

class BaseApp():
    def init(self):
        log.debug('start init')
       
        # define the name you want to use for your db here
        dbFile = os.path.abspath(os.path.join(dataFolder, 'kraken.sqlite'))
        # define the db driver name here or get it from a configuration file
        dbDriver = "sqlite"
        dbUrl = db.sa.engine.url.URL(dbDriver, database=dbFile)
        log.debug("db: %s\n\n" % dbUrl)

        self.session = self.connectToDatabase(dbUrl)
        
        log.debug('end init')
        return True
    #----------------------------------------------------------------------
    def connectToDatabase(self, dburl):
        """
        Connect to our database and return a Session object

        :param dburl: a valid SQLAlchemy URL string
        """

        log.debug("connect db")
        engine = db.sa.create_engine(dburl, echo=False)
        db.init_model(engine)
        session = db.DBSession()
        self.setupDatabase(session, engine)
        return session
    #----------------------------------------------------------------------
    def setupDatabase(self, session, engine):
        """Setup the db, note that this will not upgrade already existing tables"""
        log.debug("setup db")
        db.metadata.create_all(engine)
        log.debug("db created")
    #----------------------------------------------------------------------
    def insertOhlc(self, response):
        ohlc = db.Ohlc()
        ohlc.parseKrakenToOhlc(response)
    #----------------------------------------------------------------------
    def insertTicker(self, response):
        ticker = db.Ticker()
        ticker.parseKrakenToTicker(response)
        self.session.add(ticker)
        self.session.commit()
    #----------------------------------------------------------------------

if __name__ == "__main__":
    ba = BaseApp()
    ba.init()
    

    #krakenKeyPath = os.path.abspath(os.path.join(dataFolder, 'kraken.key'))
    #kraken = Kraken(krakenKeyPath)
    kraken = Kraken()
    response = kraken.QueryPublic('Ticker', {'pair': 'ETHEUR', 'interval' : 5})
    
    #ba.insertOhlc(response)
    ba.insertTicker(response)