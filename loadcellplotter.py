# module for the flask server - returns an image to display

import pandas as pd
import matplotlib as mpl
mpl.use('Agg') # headless!
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

import datetime
from dateutil import tz
from tzlocal import get_localzone
import time

tzl = get_localzone().zone

def loadcellplot():
    df = pd.read_csv('loadcell.xls',sep='\t')
    df.columns=["epoch","mass"]
    df['date'] = pd.to_datetime(df['epoch'],unit='s')
    df.set_index(df['date'],inplace=True)
    df = df.tz_localize(tz=tzl)
    mdates.rcParams['timezone'] = tzl
    lastone = df.epoch[-1] # easier to use the original epoch rather than the internal datetimes!
    lasttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(lastone))
    firstone = df.epoch[0]
    firsttime = time.strftime('%Y%m%d_%H%M%S',time.localtime(firstone))
    imname = 'loadcell%s.png' % (lasttime)
    x = df['date']
    y = df['mass']
    ms = 2
    nrow = df.shape[0]
    if nrow > 1000:
        ms = 1
    if nrow > 10000:
        ms = 0.5
    if nrow > 100000:
        ms = 0.2
    plt.figure(figsize=(10,8))
    plt.plot(x, y, c='blue',linestyle='None', markersize = ms, marker='o')
    plt.title('%d Loadcell values, %s to %s' % (df.shape[0],firsttime,lasttime))
    plt.xlabel('Date/Time (month-day hour for example)')
    plt.ylabel('Reported Mass (g)')
    plt.grid()
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    plt.clf()
    bytes_image.seek(0)
    return bytes_image

