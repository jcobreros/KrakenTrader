# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 18:34:34 2016

@author: jcobreros
"""
import time
from Kraken import Kraken
import sys
import sqlite3

class Ohlc:
    def __init__(self, pair):
        self.pair = pair#'ETHEUR'
        self.interval = 1
        self.kraken = Kraken()
        self.fileName = self.pair + "_OHLC.db"
        self.db = sqlite3.connect(self.fileName)
        self.c = self.db.cursor()
        
        # Create table
        self.c.execute('''CREATE TABLE IF NOT EXISTS ohlc
                     (time real, open real, high real, low real, close real, vwap real, volume real, count real)''')
        self.db.commit()
        
        self.update()

       #<time>, <open>, <high>, <low>, <close>, <vwap>, <volume>, <count>
    def update(self):    
        response = self.kraken.QueryPublic('OHLC', {'pair': self.pair, 'interval' : self.interval})

        if len(response['error']) > 0:
            print response['error']
        else:               
            data = response['result'][self.pair]
            last = response['result']['last']
            #print data, dateTime
            
            self.c.executemany('INSERT INTO ohlc VALUES (?,?,?,?,?,?,?,?)', data)
            self.db.commit()
            
            self.c.execute("SELECT open FROM ohlc")
            data = self.c.fetchall()
            print len(data)
            
            self.c.execute('SELECT MIN(time) time FROM ohlc GROUP BY time')
            self.c.execute('SELECT time FROM ohlc WHERE time<1000000000')
            data = self.c.fetchall()
            print len(data)
                  
            #self.c.execute('DELETE FROM ohlc\
            #                 WHERE time NOT IN\
            #                (\
            #                  SELECT MIN(time) time\
            #                    FROM ohlc\
            #                   GROUP BY time\
            #                )')
                            
            #self.c.execute("SELECT open FROM ohlc")
            #data = self.c.fetchall()
            #print len(data)
                
        #except:
        #    e = sys.exc_info()[0]
        #    print e
        
ohlc = Ohlc('XETHZEUR')