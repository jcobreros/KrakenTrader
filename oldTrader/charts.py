import matplotlib.pyplot as plt
from matplotlib import gridspec
from numpy import *
from pylab import *

fig = 0

def prepareCharts():
    fig = plt.figure()
    return fig
    
    
def printCharts(cr, macd, robot, fig):
    markerStyleLow = dict(linestyle='-', color='red', markersize=2)
    markerStyleHigh = dict(linestyle='-', color='green', markersize=2)
    markerStyleOpen = dict(linestyle='-', color='green', markersize=2)
    markerStyleClose = dict(linestyle='-', color='red', markersize=2)

    
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1])
    ax1 = plt.subplot(gs[0])
    plt.grid(True)
    ax2 = plt.subplot(gs[1], sharex=ax1)
    fig.subplots_adjust(hspace=0, left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.grid(True)
    ax3 = plt.subplot(gs[2], sharex=ax1)
    fig.subplots_adjust(hspace=0, left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.grid(True)
    
    ax1.plot(cr.ohcl.dateTime, cr.ohcl.closePrice, marker=' ', c='r', linestyle='-')  # , **markerStyleClose)
    ax1.plot(cr.ohcl.dateTime, cr.ohcl.openPrice, marker=' ', c='g', linestyle='-')  # , **markerStyleOpen)

    ax1.plot(cr.ohcl.dateTime, macd.movingAverage1)
    ax1.plot(cr.ohcl.dateTime, macd.movingAverage2)

    for order in robot.confirmedOrders:
        if order[0] == 'Buy':
            ax1.plot(order[1], order[2], marker='s', markersize=10, linestyle='', c='g')
        elif order[0] == 'Sell':
            ax1.plot(order[1], order[2], marker='s', markersize=10, linestyle='', c='r')
    
    for order in robot.orderTriggers:
        if order[0] == 'Buy':
            ax1.plot(order[1], order[2], marker='s', markersize=5, linestyle='', c='g')
        elif order[0] == 'Sell':
            ax1.plot(order[1], order[2], marker='s', markersize=5, linestyle='', c='r')
            
    ax2.plot(cr.ohcl.dateTime, cr.ohcl.volume, linestyle=' ')
    ax2.fill_between(cr.ohcl.dateTime, cr.ohcl.volume, 0,
                     where=array(cr.ohcl.openPrice) - array(cr.ohcl.closePrice) < 0, facecolor='green',
                     interpolate=True, lw=0)
    ax2.fill_between(cr.ohcl.dateTime, cr.ohcl.volume, 0,
                     where=array(cr.ohcl.openPrice) - array(cr.ohcl.closePrice) >= 0, facecolor='red', interpolate=True,
                     lw=0)

    ax3.plot(macd.dateTime, macd.macd)
    ax3.plot(macd.dateTime, macd.signal)
    ax3.plot(macd.dateTime, macd.histogram, c='k')

    ax3.fill_between(macd.dateTime, macd.histogram, where=array(macd.histogram) > 0, facecolor='green')
    ax3.fill_between(macd.dateTime, macd.histogram, where=array(macd.histogram) < 0, facecolor='red')
    
    plt.draw()
