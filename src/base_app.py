"""base_app for KrakenTrader"""

import sys
import os
basedir, f = os.path.split(__file__)

# logging
import logging, logging.config
logSQLFile = os.path.join(basedir, 'sqllog.txt')
logConfigFile = os.path.join(basedir, 'logging.conf')
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

class BaseApp():
    def init(self):
        log.debug('start init')
       
        # define the name you want to use for your db
        dbFile = 'data//kraken.sqlite'
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

        #result = session.query(db.Olvlist).first()
        #if not result:
        #    self.createOLVEntries(session)
        #    log.debug('olv entries created')

    #----------------------------------------------------------------------
    def createOLVEntries(self, session):
        """Create entires in Olvlist table for olv.ColumnDefn"""
        olvEntries = {}
        olvEntries[u'Book'] = [
            [u'publisher', 0, 150, u'publisher', u'name',
                    None, None, True, u'', u'left', u'', u''],
            [u'title', 1, 150, None, u'title',
                    None, None, False, u'', u'left', u'', u''],
            [u'author', 2, 150, u'person', u'full_name',
                    None, None, False, u'', u'left', u'', u''],
            [u'isbn', 3, 150, None, u'isbn',
                    None, None, False, u'', u'left', u'', u''],
            [u'published', 4, 50, None, u'published',
                    None, u'published', True, u'', u'left', u'', u''],
                 ]

        olvEntries[u'Person'] = [
            [u'first_name', 0, 150, None, u'first_name',
                    None, None, False, u'', u'left', u'', u''],
            [u'last_name', 1, 150, None, u'last_name',
                    None, None, False, u'', u'left', u'', u'']]

        olvEntries[u'Publisher'] = [
            [u'name', 0, 150, None, u'name',
                    None, None, False, u'', u'left', u'', u'']]

        for k in olvEntries:
            self.doCreateOLVEntry(session, k, olvEntries[k])

    #----------------------------------------------------------------------
    def doCreateOLVEntry(self, session, klass, cols):
        """Do the actual creation in the database"""
        for col in cols:
            olve = db.Olvlist(klassname=klass, colname=col[0],
                           colno=col[1], width=col[2], valuerel=col[3],
                           valuecol=col[4],
                           checkstatrel=col[5], checkstatcol=col[6],
                           colgroup=col[7], groupkeyg=col[8],
                           align=col[9],
                           stringconv=col[10],
                           imageg=col[11])
            if col[2] == 0:
                olve.colshow = False

            session.add(olve)
        session.commit()
    #----------------------------------------------------------------------

if __name__ == "__main__":
    ba = BaseApp()
    ba.init()