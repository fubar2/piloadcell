import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

import datetime
from dateutil import tz
from tzlocal import get_localzone

tzl = get_localzone().zone

def loadcellplot():
    df = pd.read_csv('loadcell.xls',sep='\t')
    df.columns=["epoch","mass"]
    df['timestamp'] = pd.to_datetime(list(df['epoch']),unit='s')
    df['date'] = pd.to_datetime(df['epoch'],unit='s',utc=True)
    df.set_index(df['date'],inplace=True)
    df = df.tz_localize(tz=tzl)
    mdates.rcParams['timezone'] = tzl
    lastone = df.iloc[-1].tolist()
    lasttime = lastone[2].strftime('%Y%d%M_%H%M%S')
    firstone = df.iloc[1].tolist()
    firsttime = firstone[2].strftime('%Y%d%M_%H%M%S')
    imname = 'loadcell%s.png' % (lasttime)
    x = df['date']
    y = df['mass']
    plt.close('all')
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

